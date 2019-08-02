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
    datain = ctypes.create_string_buffer(raw)
    keyin = ctypes.create_string_buffer(key)
    buffer = ctypes.create_string_buffer(len(raw))
    LIB_MYAES.Encrypt(datain, keyin, buffer)
    return buffer.value

def aes_decrypt(en, key): 
    datain = ctypes.create_string_buffer(en)
    keyin = ctypes.create_string_buffer(key)
    buffer = ctypes.create_string_buffer(len(en))
    LIB_MYAES.Encrypt(datain, keyin, buffer)
    return buffer.value

if __name__ == "__main__":
    raw = bytes([0xdc, 0x95, 0xc0, 0x78, 0xa2, 0x40, 0x89, 0x89, 0xad, 0x48, 0xa2, 0x14, 0x92, 0x84, 0x20, 0x87,
    0x08, 0xc3, 0x74, 0x84, 0x8c, 0x22, 0x82, 0x33, 0xc2, 0xb3, 0x4f, 0x33, 0x2b, 0xd2, 0xe9, 0xd3])
    key =  bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ])
    res = aes_encrypt(raw, key)
    print("明文 {}, 长度 {}".format(raw, len(raw)))
    print("密文 {}, 长度 {}".format(res, len(raw)))
    print("密钥 {}, 长度 {}".format(key, len(raw)))
    print("解密 {}, 长度 {}".format(aes_decrypt(res, key), len(res)))


    