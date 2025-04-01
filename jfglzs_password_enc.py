import base64
from Crypto.Cipher import DES
import re

class PasswordDecryptor:
    def __init__(self):
        # 修正的DES密钥和IV（处理原始代码的硬编码值）
        self.key = b'7]F8H]&g'  # 取自代码中第一段固定字符串前8字节
        self.iv = b'd9*fCAd('   # 取自代码中第一段固定字符串第9-16字节

    def decrypt_password(self, encrypted_str):
        try:
            # 处理原始密文中的特殊字符（如\P\N）
            encrypted_str = encrypted_str.replace('\\', '\\\\')  # 双重转义
            
            # Base64解码（原始代码可能有自定义编码）
            decoded = base64.b64decode(encrypted_str.encode('latin1'))
            
            # DES解密
            cipher = DES.new(self.key, DES.MODE_CBC, self.iv)
            decrypted = cipher.decrypt(decoded)
            
            # 去除填充（PKCS7）
            pad_len = decrypted[-1]
            return decrypted[:-pad_len].decode('latin1')
        except Exception as e:
            print(f"解密失败: {str(e)}")
            return None

# 使用示例
if __name__ == "__main__":
    decryptor = PasswordDecryptor()
    
    # 原始密文示例
    encrypted_password = r"fBG;(&P9n<\P\N+%anM^73"  # 注意使用原始字符串(r前缀)
    
    # 解密流程
    print(f"原始密文: {encrypted_password}")
    result = decryptor.decrypt_password(encrypted_password)
    
    if result:
        print(f"解密结果: {result}")
    else:
        print("解密失败，请检查输入格式")