import PIL
from PIL import Image
import os
import cv2
import numpy as np
import sys
import threading
import subprocess
import win32api,win32con
from moviepy.video.io.VideoFileClip import VideoFileClip
from . import aes
import traceback
baae_path = os.getcwd()
if getattr(sys, 'frozen', False):
    baae_path = os.path.abspath(sys._MEIPASS)

ffmepg_path = os.path.abspath(os.path.join(baae_path,  'ffmpeg.exe'))

#用线程的方式来限制函数执行时间
class Dispacher(threading.Thread):
    def __init__(self, fun, args1, args2,args3):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.result = None
        self.error = None
        self.fun = fun
        self.args1 = args1
        self.args2 = args2
        self.args3= args3

        self.start()

    def run(self):
        try:
            self.result = self.fun(self.args1, self.args2, self.args3)
        except:
            self.error = sys.exc_info()


def readColorImage(filename):
    '''
    读一张彩色图片
    :param filename: 图片（帧）名称
    :return: opencv格式矩阵
    '''
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    return img


def writeImage(filename, img):
    '''
    根据路径保存图片
    :param filename: 路径+图片名称
    :param img: 图片
    :return: 无
    '''
    cv2.imwrite(filename, img)


def rgb2ycc(img):
    '''
    把图片从RGB模式变成YCbCr模式
    :param img: RGB模式图片
    :return: YCbCr模式图片
    '''
    height = img.shape[0]
    width = img.shape[1]
    ycc_data = np.empty([height, width, 3])
    for i in np.arange(height):
        for j in np.arange(width):
            ycc_data[i][j][0] = 0.299 * img[i][j][2] + 0.587 * img[i][j][1] + 0.114 * img[i][j][0]  # Y
            ycc_data[i][j][1] = -0.169 * img[i][j][2] - 0.331 * img[i][j][1] + 0.500 * img[i][j][0]  # Cb
            ycc_data[i][j][2] = 0.500 * img[i][j][2] - 0.419 * img[i][j][1] - 0.081 * img[i][j][0]  # Cr
    return ycc_data


def ycc2rgb(img):
    '''
    把图片从YCbCr模式变成RGB模式
    :param img: YCbCr模式图片
    :return:  RGB模式图片
    '''
    height = img.shape[0]
    width = img.shape[1]
    rgb_data = np.empty([height, width, 3])
    for i in np.arange(height):
        for j in np.arange(width):
            rgb_data[i][j][0] = img[i][j][0] + 1.772 * img[i][j][1]  # B
            rgb_data[i][j][1] = img[i][j][0] - 0.344 * img[i][j][1] - 0.714 * img[i][j][2]  # G
            rgb_data[i][j][2] = img[i][j][0] + 1.402 * img[i][j][2]  # R
    return rgb_data


def get_y(img):
    '''
    获取图片的Y分量
    :param img: YCbCr模式图片
    :return: Y分量
    '''
    height = img.shape[0]
    width = img.shape[1]
    y_data = np.empty([height, width])
    for i in np.arange(height):
        for j in np.arange(width):
            y_data[i][j] = img[i][j][0]
    return y_data


def extract_image_from_clip(path,  num):#加水印时调用
    #根据帧所在的帧数命名帧
    file_name = os.path.dirname(path) + "/frame" + str(num) + ".png"
    # 保存该帧（中间过程需要，后面会统一销毁），保存路径为输入视频的目录
    #clip.save_frame(file_name, t, withmask=True)
    cap = cv2.VideoCapture(path)  # 读入文件
    cap.set(cv2.CAP_PROP_POS_FRAMES, num)
    success, frame = cap.read()
    cv2.imwrite(file_name,frame)
    return file_name

def extract_image(path, num):#解水印时调用

    file_name = os.getcwd()+ "/frame" + str(num) + ".png"
    # 保存该帧（中间过程需要，后面会统一销毁），保存路径为输入视频的目录
    #clip.save_frame(file_name, t, withmask=True)
    cap = cv2.VideoCapture(path)  # 读入文件
    cap.set(cv2.CAP_PROP_POS_FRAMES, num)
    success, frame = cap.read()
    cv2.imwrite(file_name,frame)
    return file_name

def atoi(s):
    s = s[::-1]
    num = 0
    for i, v in enumerate(s):
        for j in range(0, 10):
            if v == str(j):
                num += j * (10 ** i)
    return num

def add_watermark(path, message):
    '''
    均匀的从视频中抽取帧加水印
    :param path: 输入视频的目录
    :param video: moviepy读取的视频格式
    :param message: 编码后的水印
    :return:返回保存帧名称的数组
    '''
    frames_dict = {}


    # f = open('C:/Users/Liyefan/Desktop/test_video/frame_index.txt', 'rb')
    #
    # line = f.readline()  # 调用文件的 readline()方法
    # while line:
    #     end = line.decode('utf8').find(':')
    #     n=line.decode('utf8')[0:end]
    #     time=atoi(n)/video_fps
    #     image_file = extract_image_from_clip(path, video, time)  # 用帧所在的时间给其命名
    #     frames_dict[time] = image_file  # 把帧名称保存在数组里，数组索引为帧在原视频的时间
    #     encode_image(path, image_file, message)  # 加水印
    #     line = f.readline()
    #
    # f.close()
    keyframe_path = os.path.dirname(path)+"/keyframe_list.txt"
    if os.path.exists(keyframe_path) == 1:
        os.remove(keyframe_path)
    strcmd = ffmepg_path+" -i " + path + " -vf select='eq(pict_type\,I)' -vsync 2 -s 1920*1080 -f " \
                                   "image2 keyframe-%02d.jpeg -loglevel debug 2>&1| for /f \"tokens=4  delims=. \" %d " \
                                   "in ('findstr \"pict_type:I\" ') do echo %d>> " + keyframe_path

    subprocess.call(strcmd, shell=True)
    f = open(keyframe_path, 'rb')
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        if line.decode('utf8').startswith('n') == 0:
            line = f.readline()
            continue
        begin = line.decode('utf8').find(':')
        n = line.decode('utf8')[begin:]
        num = int(atoi(n) / 1000)
        image_file = extract_image_from_clip(path, num)  # 用帧所在的时间给其命名
        frames_dict[num] = image_file  # 把帧名称保存在数组里，数组索引为帧在原视频的帧数
        encode_image(path, image_file, message)  # 加水印
        line = f.readline()

    f.close()



    return frames_dict


def encode_image(path, image_file, message):
    '''
    给一个视频帧加水印，取256*256大小的区域做8*8的DCT变换
    :param path: 读入视频的路径
    :param image_file: 加水印的帧名称
    :param message: 水印
    :return: 无
    '''
    size = 256#水印块大小为256*256
    alfa = 10  # 尺度因子,控制水印添加的强度,决定了频域系数被修改的幅度
    K = 8
    Key1 = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    Key2 = np.array([8, 7, 6, 5, 4, 3, 2, 1])
    length = len(message)
    for i in range(0, 32 * 32 - length):
        message.append(0)
    message = np.array(message)
    mark = message.reshape((32, 32))#水印编码后最长为32*32个01字符串，不够后面补0

    rgb_data = readColorImage(image_file)
    rgb_data_height = rgb_data.shape[0]
    rgb_data_width = rgb_data.shape[1]#获取视频帧的尺寸

    # screen_width=win32api.GetSystemMetrics(win32con.SM_CXSCREEN)#获取屏幕的X方向大小
    # screen_height=win32api.GetSystemMetrics(win32con.SM_CYSCREEN)#Y方向
    #
    # #让原视频按照原比例适应屏幕尺寸，
    # if rgb_data_width/rgb_data_height >screen_width/screen_height:
    #     rgb_data = cv2.resize(rgb_data, (int(screen_width), int(screen_width / (rgb_data_width/rgb_data_height))),
    #                       interpolation=cv2.INTER_CUBIC)
    # else:
    #     rgb_data=cv2.resize(rgb_data, (int(screen_height* (rgb_data_width/rgb_data_height)), int(screen_height )),
    #                       interpolation=cv2.INTER_CUBIC)

    start_h=int((rgb_data.shape[0]-256)/2)#加水印的起始像素点，从该点横向纵向256个像素取一个正方形
    start_w=int((rgb_data.shape[1]-256)/2)#水印正方形中心对应整个帧的中心

    crop = rgb_data[start_h:start_h+256, start_w:start_w+256]#从视频帧中取出正方形
    ycc_data = rgb2ycc(crop)
    y_data = get_y(ycc_data)
    image = PIL.Image.fromarray(y_data)
    D = image.copy()#拷贝一份原正方形图
    D = np.array(D)#变成np数组

    for p in range(int(size / K)):
        for q in range(int(size / K)):
            x = p * K
            y = q * K
            img_B = np.float32(D[x:x + K, y:y + K])  # 把图片分成8*8的子块
            I_dct1 = cv2.dct(img_B)

            if mark[p, q] < 1:#水印编码为0
                Key = Key1
            else:             #水印编码为1
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
    for i in np.arange(height):#把取出来做dct变换的Y分量放回YCbCr格式的图
        for j in np.arange(width):
            ycc_data[i][j][0] = E[i][j]
    embeded_rgb_data = ycc2rgb(ycc_data)

    # 这里要先保存下来再读，不然取出来的正方形放回原图的时候有的像素颜色会改变，没找出来为什么（滑稽）
    writeImage(os.path.dirname(path) + '/temp.jpg', embeded_rgb_data)

    if os.path.exists(os.path.dirname(path) + '/temp.jpg') == 0:
        raise Exception("添加水印不成功")

    img = readColorImage(os.path.dirname(path) + '/temp.jpg')
    for i in range(start_h,start_h+256):#取出来的正方形放回原图
        for j in range(start_w,start_w+256):
            rgb_data[i][j] = img[i-start_h][j-start_w]
    writeImage(image_file, rgb_data)


def reconstruct_video(path, frames_dict):
    '''
    重构视频，把加了水印的帧写回原视频位置
    :param path: 读入视频的路径
    :param frames_dict: 保存帧名称的数组
    :return: 无
    '''
    videoCapture = cv2.VideoCapture(path)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)#获取帧率
    # fourcc = int(videoCapture.get(cv2.CAP_PROP_FOURCC))
    fourcc = cv2.VideoWriter_fourcc(*'X264')#选择编码方式

    # screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)#获取屏幕尺寸
    # screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    #
    # frame_width=videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
    # frame_heigth=videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)#获取视频帧尺寸
    #
    # if frame_width / frame_heigth > screen_width / screen_height:#生成的视频适应屏幕尺寸
    #     size = (int(screen_width), int(screen_width/(frame_width/frame_heigth) ))
    # else:
    #     size=(int(screen_height*(frame_width/frame_heigth)),int(screen_height ))
    size=(1920,750)

    vw = cv2.VideoWriter(os.path.dirname(path) + '/temp.mp4', fourcc, fps, size)

    frame_num = []
    frame_file = []

    for num in frames_dict:#这样做是因为frames_dict数组的索引不是连续的，让frame_num和frame_file一一对应
        frame_num.append(num)
        frame_file.append(frames_dict[num])

    j = 0
    success, frame = videoCapture.read()
    while success:
        flag = 0
        for k in range(len(frames_dict)):#如果此时帧数正好是加了水印的帧数
            if (j == int(frame_num[k])):
                img = cv2.imread(frame_file[k])
                vw.write(img)#把加了水印的帧写进去替代原来的帧
                flag = 1
        if flag == 0:#没有加水印的帧正常写进去
            # screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            # screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
            # if frame.shape[1]/frame.shape[0]>screen_width / screen_height:
            #     frame = cv2.resize(frame, (int(screen_width), int(screen_width/(frame.shape[1]/frame.shape[0]))),
            #                    interpolation=cv2.INTER_CUBIC)
            # else:
            #     frame=cv2.resize(frame, (int(screen_height*(frame.shape[1]/frame.shape[0])), int(screen_height)),
            #                    interpolation=cv2.INTER_CUBIC)

            vw.write(frame)

        # 读取视频下一帧的内容
        j += 1
        success, frame = videoCapture.read()
    vw.release()


def apply_watermarking(path, message, outpath):
    frames_dict = add_watermark(path,  message)#加水印
    reconstruct_video(path, frames_dict)#重构视频



def de_watermark(rgb_img,i,j):
    '''
    从某一帧中解水印
    :param rgb_img:帧
    :param i:
    :param j: （i,j）为要取正方形的起始像素点
    :return: 带有开头标记的水印
    '''
    #这里解水印是加水印的逆过程
    size = 256
    K = 8
    Key1 = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    Key2 = np.array([8, 7, 6, 5, 4, 3, 2, 1])
    rgb_cover = rgb_img[i:i + 256, j:j + 256]
    #print(i, j)

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

    msg = Pmark.flatten()#把二维数组变成一维数组

    #解码
    secret_msg = ''
    k = 0
    while k < len(msg):
        arr = msg[k:(k + 8)]
        k += 8
        s = ''.join(str(l) for l in arr)
        if s=='00000000':continue#不对应任何有价值内容
        s = chr(int(s, 2))

        secret_msg += s
    return secret_msg

def extract_message_from_video(path,frame_number,frame_totalnum):
    while(frame_number<frame_totalnum):

        image = extract_image(path,frame_number )
        print(frame_number)
        frame_number += 1

        rgb_img = readColorImage(image)
        height = rgb_img.shape[0]
        width = rgb_img.shape[1]
        if width / height > 1920 / 750:
            rgb_img = cv2.resize(rgb_img, (int(750 * (width / height)), 750))
        else:
            rgb_img = cv2.resize(rgb_img, (1920, int(1920 / (width / height))))


        indexi = int(rgb_img.shape[0] / 2)
        indexj = int(rgb_img.shape[1] / 2)  # 中心像素
        secret_msg = de_watermark(rgb_img, indexi - 128, indexj - 128)

        sum = 0
        match = 'bjfu'
        if len(secret_msg) > 4:
            for i in range(4):
                for j in range(4):
                    if secret_msg[i] == match[j]:
                        sum = sum + 1
            # print(sum)
            if sum >= 2:
                secret_msg = secret_msg[4:]
                secret_match = secret_msg.strip()
                word=''
                for i in range(len(secret_match)):
                    if ord(secret_match[i])>31 and ord(secret_match[i])<127:
                        word+=secret_match[i]
                    else:
                        word+='?'
                #print(word)

                dict={'contents':word,
                      'next_frame':frame_number}

                return dict    

#     for (time, frame) in video.iter_frames(with_times=True):

#             print("切换到复杂模式寻找")  # 裁剪后中心点变了，所以从裁剪后的中心向外螺旋查找
#             image = extract_image(path, video, time-15)
#             rgb_img = readColorImage(image)
#             print(time)

#             length= rgb_img.shape[0] * rgb_img.shape[1]
#             indexi = int(rgb_img.shape[0] / 2)
#             indexj = int(rgb_img.shape[1] / 2)
#             secret_msg = de_watermark(rgb_img, indexi - 128, indexj - 128)
#             sum = 0
#             word = 'bjfu'
#             if len(secret_msg) > 4:
#                 for i in range(4):
#                     for j in range(4):
#                         if secret_msg[i] == word[j]:
#                             sum = sum + 1
#                 # print(sum)
#                 if sum >= 2:
#                     secret_msg = secret_msg[4:]
#                     return (secret_msg.strip())

#             count = 1
#             num = 1
#             while (num < length):
#                 n = count
#                 while (n > 0):
#                     indexi = indexi - 1  # 向上走
#                     if indexi - 128 >= 0 and indexj < rgb_img.shape[1]:
#                         secret_msg = de_watermark(rgb_img, indexi - 128, indexj - 128)
#                         sum = 0
#                         word = 'bjfu'
#                         if len(secret_msg) > 4:
#                             for i in range(4):
#                                 for j in range(4):
#                                     if secret_msg[i] == word[j]:
#                                         sum = sum + 1
#                             # print(sum)
#                             if sum >= 2:
#                                 secret_msg = secret_msg[4:]
#                                 return (secret_msg.strip())

#                         n = n - 1
#                         num = num + 1
#                 if num >= length: break

#                 n = count
#                 while (n > 0):
#                     indexj = indexj - 1  # 向左走
#                     if indexj - 128 >= 0 and indexi - 128 >= 0:
#                         secret_msg = de_watermark(rgb_img, indexi - 128, indexj - 128)
#                         sum = 0
#                         word = 'bjfu'
#                         if len(secret_msg) > 4:
#                             for i in range(4):
#                                 for j in range(4):
#                                     if secret_msg[i] == word[j]:
#                                         sum = sum + 1
#                             # print(sum)
#                             if sum >= 2:
#                                 secret_msg = secret_msg[4:]
#                                 return (secret_msg.strip())

#                         n = n - 1
#                         num = num + 1
#                 if num >= length: break

#                 count = count + 1

#                 n = count
#                 while (n > 0):
#                     indexi = indexi + 1  # 向下走
#                     if indexi < rgb_img.shape[0] and indexj - 128 >= 0:
#                         secret_msg = de_watermark(rgb_img, indexi - 128, indexj - 128)
#                         sum = 0
#                         word = 'bjfu'
#                         if len(secret_msg) > 4:
#                             for i in range(4):
#                                 for j in range(4):
#                                     if secret_msg[i] == word[j]:
#                                         sum = sum + 1
#                             # print(sum)
#                             if sum >= 2:
#                                 secret_msg = secret_msg[4:]
#                                 return (secret_msg.strip())

#                         n = n - 1
#                         num = num + 1
#                 if num >= length: break

#                 n = count
#                 while (n > 0):
#                     indexj = indexj + 1  # 向右走
#                     if indexi < rgb_img.shape[0] and indexj < rgb_img.shape[1]:
#                         secret_msg = de_watermark(rgb_img, indexi - 128, indexj - 128)
#                         sum = 0
#                         word = 'bjfu'
#                         if len(secret_msg) > 4:
#                             for i in range(4):
#                                 for j in range(4):
#                                     if secret_msg[i] == word[j]:
#                                         sum = sum + 1
#                             # print(sum)
#                             if sum >= 2:
#                                 secret_msg = secret_msg[4:]
#                                 return (secret_msg.strip())

#                         n = n - 1
#                         num = num + 1
#                 if num >= length: break

#                 count = count + 1

