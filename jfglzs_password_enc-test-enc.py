# -*- coding: utf-8 -*-
from Crypto.Cipher import DES
from base64 import b64decode, b64encode
import re

def decrypt_forgot_issuer(encrypted_str: str) -> str:
    """
    DES-CBC解密函数
    对应C#原函数：public static string ForgotIssuer(string string_0)
    """
    # 密钥生成逻辑（与原C#代码一致）
    win_dir = r"C:\WINDOWS"  # 硬编码Windows路径
    
    # 截取密钥和IV（注意Python字符串索引从0开始）
    key_str = win_dir[:8]    # 取前8字符 -> "C:\\WIND"
    iv_str = win_dir[1:9]    # 从第2字符取8字符 -> ":\\WINDO"
    
    # 转换为DES需要的8字节（UTF-8编码）
    key = key_str.encode('utf-8')[:8]
    iv = iv_str.encode('utf-8')[:8]

    try:
        # Base64解码
        encrypted_data = b64decode(encrypted_str)
        
        # 创建DES解密器
        cipher = DES.new(key, DES.MODE_CBC, iv)
        
        # 执行解密
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # 去除PKCS7填充
        padding_len = decrypted_data[-1]
        decrypted = decrypted_data[:-padding_len]
        
        # 清理不可打印字符（应对可能的解码残留）
        clean_str = re.sub(r'[\x00-\x1F]+', '', decrypted.decode('utf-8', errors='ignore'))
        return clean_str.strip()
    
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

def encrypt_forgot_issuer(plaintext: str) -> str:
    """
    逆向实现的加密函数（用于验证）
    """
    win_dir = r"C:\WINDOWS"
    key_str = win_dir[:8]
    iv_str = win_dir[1:9]
    
    key = key_str.encode('utf-8')[:8]
    iv = iv_str.encode('utf-8')[:8]

    cipher = DES.new(key, DES.MODE_CBC, iv)
    
    # PKCS7填充
    pad_len = 8 - (len(plaintext) % 8)
    padded_data = plaintext.encode('utf-8') + bytes([pad_len] * pad_len)
    
    encrypted_data = cipher.encrypt(padded_data)
    return b64encode(encrypted_data).decode('utf-8')

if __name__ == "__main__":
    # 验证示例
    test_str = "asdf1234"
    print("by lzh")
    # 加密测试
    encrypted = encrypt_forgot_issuer(test_str)
    print(f"Encrypted: {encrypted}")
    decrypted = ""
    # 解密测试
    #decrypted = decrypt_forgot_issuer("K!b+mc<P.Xb:G._?M9@E73")
    #print(f"Decrypted: {decrypted}")
#    print(f"Match: {decrypted == test_str}")  # 应输出True