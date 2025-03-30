
from Crypto.Cipher import DES
from base64 import b64decode
import re

def decrypt_forgot_issuer(encrypted_str: str) -> str:
    # 生成与C#代码一致的密钥和IV
    win_path = "C:\\WINDOWS"  # 硬编码路径
    key_str = win_path[:8]    # 取前8字符 "C:\\WIND"
    iv_str = win_path[1:9]    # 从第2字符取8字符 ":\\WINDO"
    
    # 转换为DES所需的8字节
    key = key_str.encode('utf-8')[:8]
    iv = iv_str.encode('utf-8')[:8]

    # Base64解码
    encrypted_data = b64decode(encrypted_str)
    
    # DES-CBC解密
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    
    # 去除PKCS7填充
    padding_len = decrypted_data[-1]
    decrypted = decrypted_data[:-padding_len]
    
    # 处理可能的编码残留（匹配原VB代码行为）
    clean_str = re.sub(r'[\x00-\x1F]+', '', decrypted.decode('utf-8', errors='ignore'))
    return clean_str.strip()

# 使用示例
encrypted = "+7IOcdaerrorg78cs"  # 替换为实际加密字符串
print(decrypt_forgot_issuer(encrypted))