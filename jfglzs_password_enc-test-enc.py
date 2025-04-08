import base64
from Crypto.Cipher import DES

def decrypt_password(encrypted_text):
    # 将每个字符的ASCII码加10，还原Base64字符串
    base64_str = ''.join([chr(ord(c) + 10) for c in encrypted_text])
    # Base64解码
    encrypted_data = base64.b64decode(base64_str)
    
    # 定义DES的密钥和IV（根据C#代码中的逻辑）
    key = b'C:\\WINDOW'  # 密钥对应C#中的Mid(value, 1, 8)
    iv = b':\\WINDOW'    # IV对应C#中的Mid(value, 2, 8)
    
    # 创建DES解密器，使用CBC模式
    cipher = DES.new(key, DES.MODE_CBC, iv)
    
    # 解密数据
    decrypted_data = cipher.decrypt(encrypted_data)
    
    # 去除PKCS7填充
    padding_length = decrypted_data[-1]
    plaintext = decrypted_data[:-padding_length]
    
    return plaintext.decode('utf-8')

# 示例用法
encrypted_password = "fBG;(&P9n<\P\N+%anM^73"

password = decrypt_password(encrypted_password)
print("解密后的密码:", password)