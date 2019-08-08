
#ifdef _MSC_VER
    #define DLL_EXPORT __declspec( dllexport ) 
#else
    #define DLL_EXPORT
#endif
extern "C" {
void SubBytes(unsigned char *state, const unsigned char box[256]);                                         /*字节代换函数原型*/
void ShiftRows(unsigned char *state);                                                                      /*行移位函数原型*/
void InvShiftRows(unsigned char *state);                                                                   /*逆行移位函数原型*/
void AddRoundKey(unsigned char *state, unsigned char *RndKey, int round);                                  /*轮密钥加函数原型*/
void MixColumn(unsigned char *state);                                                                      /*列混淆函数原型*/
void InvMixColumn(unsigned char *state);                                                                   /*逆向列混淆函数原型*/
void KeyExpansion(unsigned char *key, unsigned char *RndKey);                                              /*密钥扩展函数原型*/
void Encrypt(unsigned char *datain, unsigned char *RndKey, unsigned char *dataout);                        /*加密函数原型*/
void Decrypt(unsigned char *datain, unsigned char *RndKey, unsigned char *dataout);                        /*解密函数原型*/
DLL_EXPORT int AESCBCEnc(unsigned char *datain, unsigned long int length, unsigned char *key, unsigned char *dataout);/*CBC加密函数原型*/
DLL_EXPORT int AESCBCDec(unsigned char *datain, unsigned long int length, unsigned char *key, unsigned char *dataout);/*CBC加密函数原型*/
int SelfCheck();    
DLL_EXPORT int EnFileByPath(char* path, unsigned char* key, char* outpath);                                        /*文件读取填充加密函数原型*/
DLL_EXPORT int DeFileByPath(char* path, unsigned char* key, char* outpath);                                        /*文件读取填充加密函数原型*/
}
