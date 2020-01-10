import cv2
"""输入视频路径和截图输出路径，输出截图"""
def GetScreen(path, outpath):
    try:
        cap = cv2.VideoCapture(path)        #打开摄像头
        if not cap.isOpened():
            raise Exception({
                "error" : "无法打开视频文件"
            })
        ret, frame = cap.read()
        cv2.imwrite(outpath, frame)
    finally:
        cap.release()

"""测试用"""
if __name__=="__main__":
    GetScreen("D:/temp.mp4","D:/test.png")