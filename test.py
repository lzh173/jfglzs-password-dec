# -*- coding: gbk -*-
import argparse
import base64
from Crypto.Cipher import DES
import random

def forgot_issuer(string_0):
    # 第一阶段：DES 加密
    s = "C:\\WINDOWS"[0:8]  # 取前8个字符
    s2 = "C:\\WINDOWS"[1:9]  # 从第2个字符开始取8个
    
    # 生成随机数组（虽然代码中有这部分，但实际上没有使用）
    array7 = [0] * 11
    for i in range(1, 11):
        array7[i] = int(10 + random.random() * 100)
    
    # 排序数组（同样没有实际使用）
    for i in range(1, 10):
        for j in range(i + 1, 11):
            if array7[i] < array7[j]:
                array7[i], array7[j] = array7[j], array7[i]
    
    # DES 加密
    cipher = DES.new(s.encode('utf-8'), DES.MODE_CBC, s2.encode('utf-8'))
    
    # 填充数据以满足8字节倍数
    pad_len = 8 - (len(string_0) % 8)
    padded_data = string_0.encode('utf-8') + bytes([pad_len] * pad_len)
    
    encrypted = cipher.encrypt(padded_data)
    base64_str = base64.b64encode(encrypted).decode('utf-8')
    
    # 第二阶段：简单的字符位移
    return rate_issuer(base64_str)

def rate_issuer(string_0):
    result = ""
    for c in string_0:
        # 每个字符的ASCII码减10
        new_char = chr(ord(c) - 10)
        result += new_char
    return result

def reverse_rate_issuer(encrypted_str):
   
    result = ""
    for c in encrypted_str:
        # 每个字符的ASCII码加10（逆向操作）
        new_char = chr(ord(c) + 10)
        result += new_char
    return result

def decrypt_forgot_issuer(encrypted_str):
    """尝试修复并解密被截断的密文"""
    # 尝试补全缺失的首尾字符（各1个）
    possible_chars = [chr(i) for i in range(32, 127)]  # 可打印ASCII字符范围
    
    for first_char in possible_chars:
        for last_char in possible_chars:
            repaired_str = first_char + encrypted_str + last_char
            try:
                # 逆向 RateIssuer
                base64_str = reverse_rate_issuer(repaired_str)
                # DES 解密
                s = "C:\\WINDOWS"[0:8].encode('utf-8')  # 密钥
                s2 = "C:\\WINDOWS"[1:9].encode('utf-8')  # IV
                cipher = DES.new(s, DES.MODE_CBC, s2)
                decrypted = cipher.decrypt(base64.b64decode(base64_str))
                # 去除填充
                pad_len = decrypted[-1]
                if 0 < pad_len <= 8:
                    decrypted = decrypted[:-pad_len]
                return decrypted.decode('utf-8')
            except:
                continue  # 当前组合失败，尝试下一个
    
    raise ValueError("e1")


# 示例使用
if __name__ == "__main__":
    

    parser = argparse.ArgumentParser(description='加密/解密工具')
    
    # 创建互斥组，required=True表示必须提供其中一个参数
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--enc', type=str, help='要加密的字符串')
    group.add_argument('--dec', type=str, help='要解密的字符串')
    
    args = parser.parse_args()
    
    if args.enc:
 
        print(decrypt_forgot_issuer(args.enc))
    elif args.dec:

        print(forgot_issuer(args.dec))

