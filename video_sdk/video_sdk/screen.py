import cv2
"""输入视频路径和截图输出路径，输出截图"""
def GetScreen(path, outpath):
    cap = cv2.VideoCapture(path)        #打开摄像头
    frames_num=cap.get(7)
    i = int(frames_num / 10)
    while(i!=0):
    # get a frame
        ret, frame = cap.read()
    # show a frame
        i=i-1     #生成摄像头窗口
    cv2.imwrite(outpath, frame)
    cap.release()
"""测试用"""
if __name__=="__main__":
    GetScreen("D:/temp.mp4","D:/test.png")