from flask import request
import time
import os
import easyapi
import uuid

ALLOWED_EXTENSIONS = ['rm', 'rmvb', 'mpeg', 'mpeg2', 'mpeg3', 'mpeg4', 'mp4', 'mov', 'mtv', 'wmv', 'avi', '3gp', 'amv', 'dmv', 'flv']


def allowed_file(filename: str):
    filename_array = os.path.splitext(filename)
    tag = filename_array[1] #文件后缀
    file_title = filename_array[0] #文件名
    tag = tag.replace('.','')
    #tag = filename.split('.')[0]
    if tag in ALLOWED_EXTENSIONS:
        return file_title, tag
    else:
        return None, None

'''
return 
    uuid,   文件生成的uuid，同时也是存储文件名，使用  uuid1()
    title,  源文件名
    original_file_size  原始文件大小；字节为单位
'''
def upload_file(file_dir):  #file_dir = "files/origin/"
    f = request.files['file']
    title, tag = allowed_file(f.filename)
    original_file_size = 0
    if f and tag:
        uuid_1 = str( uuid.uuid1() )
        save_file_name = uuid_1 + '.' + tag  #存储文件名称
        file_path = os.path.join(file_dir, save_file_name) #文件存储路径

        # 判断文件夹是否存在，如果不存在则创建
        if not os.path.exists(file_dir):
            try:
                os.makedirs(file_dir)
            except Exception as e:
                raise easyapi.BusinessError(code=500, http_code=200, err_info=str(e))
        else:
            pass

        #存储文件
        try:
            f.save(file_path)
            original_file_size +=  os.path.getsize(file_path)
        except Exception as e:
            raise easyapi.BusinessError(code=500, http_code=200, err_info=str(e))
        return uuid, title, original_file_size
    else:
        raise easyapi.BusinessError(code=500, http_code=200, err_info="不支持的视频文件格式")
