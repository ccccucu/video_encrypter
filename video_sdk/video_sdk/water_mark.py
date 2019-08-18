
import PIL
from PIL import Image
import os
import cv2
import numpy as np
import sys
import threading
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip

class Dispacher(threading.Thread):
    def __init__(self, fun, args1,args2):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.result = None
        self.error = None
        self.fun = fun
        self.args1 = args1
        self.args2= args2

        self.start()

    def run(self):
        try:
            self.result = self.fun(self.args1,self.args2)
        except:
            self.error = sys.exc_info()


def readColorImage(filename):
	img = cv2.imread(filename, cv2.IMREAD_COLOR)
	return img

def writeImage(filename, img):
	cv2.imwrite(filename, img)

    
def rgb2ycc(img):
	height = img.shape[0]
	width  = img.shape[1]
	ycc_data = np.empty([height,width,3])
	for i in np.arange(height):
		for j in np.arange(width):
			ycc_data[i][j][0] =  0.299*img[i][j][2] + 0.587*img[i][j][1] + 0.114*img[i][j][0] #Y
			ycc_data[i][j][1] = -0.169*img[i][j][2] - 0.331*img[i][j][1] + 0.500*img[i][j][0] #Cb
			ycc_data[i][j][2] =  0.500*img[i][j][2] - 0.419*img[i][j][1] - 0.081*img[i][j][0] #Cr
	return ycc_data

def ycc2rgb(img):
	height = img.shape[0]
	width  = img.shape[1]
	rgb_data = np.empty([height,width,3])
	for i in np.arange(height):
		for j in np.arange(width):
			rgb_data[i][j][0] = img[i][j][0] + 1.772*img[i][j][1] #B
			rgb_data[i][j][1] = img[i][j][0] - 0.344*img[i][j][1] - 0.714*img[i][j][2] #G
			rgb_data[i][j][2] = img[i][j][0] + 1.402*img[i][j][2] #R
	return rgb_data

def get_y(img):
	height = img.shape[0]
	width  = img.shape[1]
	y_data = np.empty([height,width])
	for i in np.arange(height):
		for j in np.arange(width):
			y_data[i][j] = img[i][j][0]
	return y_data

def extract_image_from_clip(path,clip, t):
    file_name =os.path.dirname(path)+ "/frame" + str(t) + ".png"
    clip.save_frame(file_name, t, withmask=True)
    return file_name

def add_watermark(path,video,message):
    frames_dict = {}
    time = 1.0
    for i in range(2):
        image_file = extract_image_from_clip(path,video, time)
        frames_dict[time] = image_file
        encode_image(path,image_file, message)
        time += 2.0
    return frames_dict

def encode_image(path,image_file, message):
        size = 256
        alfa = 10  # 尺度因子,控制水印添加的强度,决定了频域系数被修改的幅度

        K = 8
        Key1 = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        Key2 = np.array([8, 7, 6, 5, 4, 3, 2, 1])
        length = len(message)
        for i in range(0, 32 * 32 - length):
            message.append(0)
        message = np.array(message)
        mark = message.reshape((32, 32))

        rgb_data = readColorImage(image_file)
        rgb_data=cv2.resize(rgb_data,(1344,525),interpolation=cv2.INTER_CUBIC)
        crop = rgb_data[0:256, 0:256]
        ycc_data = rgb2ycc(crop)
        y_data = get_y(ycc_data)
        image = PIL.Image.fromarray(y_data)
        D = image.copy()
        D = np.array(D)

        for p in range(int(size / K)):
            for q in range(int(size / K)):
                x = p * K
                y = q * K
                img_B = np.float32(D[x:x + K, y:y + K])  # 把图片分成8*8的子块
                I_dct1 = cv2.dct(img_B)

                if mark[p, q] < 1:
                    Key = Key1
                else:
                    Key = Key2

                I_dct_A = I_dct1.copy()  # 在中频段嵌入水印
                I_dct_A[0, 7] = I_dct1[0, 7] + alfa * Key[0]
                I_dct_A[1, 6] = I_dct1[1, 6] + alfa * Key[1]
                I_dct_A[2, 5] = I_dct1[2, 5] + alfa * Key[2]
                I_dct_A[3, 4] = I_dct1[3, 4] + alfa * Key[3]
                I_dct_A[4, 3] = I_dct1[4, 3] + alfa * Key[4]
                I_dct_A[5, 2] = I_dct1[5, 2] + alfa * Key[5]
                I_dct_A[6, 1] = I_dct1[6, 1] + alfa * Key[6]
                I_dct_A[7, 0] = I_dct1[7, 0] + alfa * Key[7]
                I_dct_A = np.array(I_dct_A)
                I_dct_a = cv2.idct(I_dct_A)
                D[x:x + K, y:y + K] = I_dct_a

        E = D.copy()
        height = ycc_data.shape[0]
        width = ycc_data.shape[1]
        for i in np.arange(height):
            for j in np.arange(width):
                ycc_data[i][j][0] = E[i][j]
        embeded_rgb_data = ycc2rgb(ycc_data)
        writeImage(os.path.dirname(path)+'/temp.jpg', embeded_rgb_data)
        img = readColorImage(os.path.dirname(path)+'/temp.jpg')
        for i in range(256):
           for j in range(256):
              rgb_data[i][j] = img[i][j]
        writeImage(image_file, rgb_data)

def reconstruct_video(path,  frames_dict):
    videoCapture = cv2.VideoCapture(path)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    #fourcc = int(videoCapture.get(cv2.CAP_PROP_FOURCC))
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    size = (int(1344), int(525))
    vw = cv2.VideoWriter(os.path.dirname(path)+'/temp.mp4', fourcc, fps, size)
    frame_num=[]
    frame_file=[]

    for time in frames_dict:
        frame_num.append(time*fps)
        frame_file.append(frames_dict[time])

    j=0
    success, frame = videoCapture.read()
    while success:
        flag=0
        for k in range(len(frames_dict)):
            if(j==int(frame_num[k])):
                img=cv2.imread(frame_file[k])
                vw.write(img)
                flag=1
        if flag==0:
            frame = cv2.resize(frame, (1344, 525), interpolation=cv2.INTER_CUBIC)
            vw.write(frame)

        # 读取视频下一帧的内容
        j+=1
        success, frame = videoCapture.read()
    vw.release()

def apply_watermarking(path,message, outpath):
    video = VideoFileClip(path)
    frames_dict = add_watermark(path,video, message)
    reconstruct_video(path,  frames_dict)

def extract_message_from_video(path,video):

    for (time, frame) in video.iter_frames(with_times=True):
        if time>=1.0:
            image = extract_image_from_clip(path,video, time)
            rgb_img = readColorImage(image)
            print(rgb_img.shape)
            for i in range(0, rgb_img.shape[0] - 256 - 260):
                for j in range(0, rgb_img.shape[1] - 256 - 1078):

                    size = 256
                    K = 8
                    Key1 = np.array([1, 2, 3, 4, 5, 6, 7, 8])
                    Key2 = np.array([8, 7, 6, 5, 4, 3, 2, 1])
                    rgb_cover = rgb_img[i:i + 256, j:j + 256]
                    print(i, j)

                    ycc_cover = rgb2ycc(rgb_cover)
                    y_cover = get_y(ycc_cover)
                    picture = np.array(y_cover)

                    Pmark = np.zeros([32, 32], dtype=int)
                    pp = np.zeros(8)
                    for p in range(int(size / K)):
                        for q in range(int(size / K)):
                            x = p * K
                            y = q * K
                            img_B = np.float32(picture[x:x + K, y:y + K])

                            I_dct1 = cv2.dct(img_B)

                            pp[0] = I_dct1[0, 7]
                            pp[1] = I_dct1[1, 6]
                            pp[2] = I_dct1[2, 5]
                            pp[3] = I_dct1[3, 4]
                            pp[4] = I_dct1[4, 3]
                            pp[5] = I_dct1[5, 2]
                            pp[6] = I_dct1[6, 1]
                            pp[7] = I_dct1[7, 0]

                            # %计算两个矩阵的相似度，越接近1相似度越大
                            if np.corrcoef(pp, Key1)[0][1] <= np.corrcoef(pp, Key2)[0][1]:
                                Pmark[p, q] = 1

                    msg = Pmark.flatten()
                    #print(list(map(int, msg)))
                    secret_msg = ''
                    k = 0
                    while k < len(msg):
                        arr = msg[k:(k + 8)]
                        k += 8
                        s = ''.join(str(l) for l in arr)
                        s = chr(int(s, 2))

                        secret_msg += s

                    if (secret_msg.startswith('bjfu')):
                        return (secret_msg[4:])

