import platform
import os
import ctypes

SYS_PLATFORM = platform.system()
SYS_ARCHITECTURE = platform.architecture()[0]
LIBMYAES_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'aesc', 'target')

if SYS_PLATFORM == 'Linux'  and SYS_ARCHITECTURE == '64bit':
    LIBMYAES_PATH = os.path.join(LIBMYAES_PATH, 'linux', 'libmyaes.so')
elif SYS_PLATFORM == 'Windows'  and SYS_ARCHITECTURE == '64bit':
    LIBMYAES_PATH = os.path.join(LIBMYAES_PATH, 'windows', 'libmyaes.so')
elif SYS_PLATFORM == 'Darwin'  and SYS_ARCHITECTURE == '64bit':
    LIBMYAES_PATH = os.path.join(LIBMYAES_PATH, 'macos', 'libmyaes.so')
else:
    raise ImportError("不支持的平台")

LIB_MYAES = ctypes.cdll.LoadLibrary(LIBMYAES_PATH)

def aes_encrypt(raw, key):
    raw_b =bytes(raw,encoding='utf-8') 
    datain = ctypes.create_string_buffer(raw_b)
    keyin = ctypes.create_string_buffer(bytes(key,encoding='utf-8'),32)
    buffer = ctypes.create_string_buffer(len(raw_b))
    LIB_MYAES.AESCBCEnc(datain,len(raw) , keyin, buffer)
    return buffer.value

def aes_decrypt(en, key): 
    en_b =bytes(en,encoding='utf-8') 
    datain = ctypes.create_string_buffer(en_b)
    keyin = ctypes.create_string_buffer(bytes(key,encoding='utf-8'), 32)
    buffer = ctypes.create_string_buffer(len(en_b))
    LIB_MYAES.AESCBCDec(datain, len(en), keyin, buffer)
    return buffer.value

def aes_encrypt_by_path(path, key, outpath):
    key_buf =  ctypes.create_string_buffer(bytes(key,encoding='utf-8'),32)
    path_buf = ctypes.create_string_buffer(bytes(path, encoding='utf-8'))
    outpath_buf = ctypes.create_string_buffer(bytes(outpath, encoding='utf-8'))
    return LIB_MYAES.EnFileByPath(path_buf, key_buf, outpath_buf)

def aes_decrypt_by_path(path, key, outpath):
    key_buf =  ctypes.create_string_buffer(bytes(key,encoding='utf-8'),32)
    path_buf = ctypes.create_string_buffer(bytes(path, encoding='utf-8'))
    outpath_buf = ctypes.create_string_buffer(bytes(outpath, encoding='utf-8'))
    return LIB_MYAES.DeFileByPath(path_buf, key_buf, outpath_buf)
