# -*- coding: gbk -*-
import argparse
import base64
from Crypto.Cipher import DES
import random

def forgot_issuer(string_0):
    # ��һ�׶Σ�DES ����
    s = "C:\\WINDOWS"[0:8]  # ȡǰ8���ַ�
    s2 = "C:\\WINDOWS"[1:9]  # �ӵ�2���ַ���ʼȡ8��
    
    # ����������飨��Ȼ���������ⲿ�֣���ʵ����û��ʹ�ã�
    array7 = [0] * 11
    for i in range(1, 11):
        array7[i] = int(10 + random.random() * 100)
    
    # �������飨ͬ��û��ʵ��ʹ�ã�
    for i in range(1, 10):
        for j in range(i + 1, 11):
            if array7[i] < array7[j]:
                array7[i], array7[j] = array7[j], array7[i]
    
    # DES ����
    cipher = DES.new(s.encode('utf-8'), DES.MODE_CBC, s2.encode('utf-8'))
    
    # �������������8�ֽڱ���
    pad_len = 8 - (len(string_0) % 8)
    padded_data = string_0.encode('utf-8') + bytes([pad_len] * pad_len)
    
    encrypted = cipher.encrypt(padded_data)
    base64_str = base64.b64encode(encrypted).decode('utf-8')
    
    # �ڶ��׶Σ��򵥵��ַ�λ��
    return rate_issuer(base64_str)

def rate_issuer(string_0):
    result = ""
    for c in string_0:
        # ÿ���ַ���ASCII���10
        new_char = chr(ord(c) - 10)
        result += new_char
    return result

def reverse_rate_issuer(encrypted_str):
   
    result = ""
    for c in encrypted_str:
        # ÿ���ַ���ASCII���10�����������
        new_char = chr(ord(c) + 10)
        result += new_char
    return result

def decrypt_forgot_issuer(encrypted_str):
    """�����޸������ܱ��ضϵ�����"""
    # ���Բ�ȫȱʧ����β�ַ�����1����
    possible_chars = [chr(i) for i in range(32, 127)]  # �ɴ�ӡASCII�ַ���Χ
    
    for first_char in possible_chars:
        for last_char in possible_chars:
            repaired_str = first_char + encrypted_str + last_char
            try:
                # ���� RateIssuer
                base64_str = reverse_rate_issuer(repaired_str)
                # DES ����
                s = "C:\\WINDOWS"[0:8].encode('utf-8')  # ��Կ
                s2 = "C:\\WINDOWS"[1:9].encode('utf-8')  # IV
                cipher = DES.new(s, DES.MODE_CBC, s2)
                decrypted = cipher.decrypt(base64.b64decode(base64_str))
                # ȥ�����
                pad_len = decrypted[-1]
                if 0 < pad_len <= 8:
                    decrypted = decrypted[:-pad_len]
                return decrypted.decode('utf-8')
            except:
                continue  # ��ǰ���ʧ�ܣ�������һ��
    
    raise ValueError("e1")


# ʾ��ʹ��
if __name__ == "__main__":
    

    parser = argparse.ArgumentParser(description='����/���ܹ���')
    
    # ���������飬required=True��ʾ�����ṩ����һ������
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--enc', type=str, help='Ҫ���ܵ��ַ���')
    group.add_argument('--dec', type=str, help='Ҫ���ܵ��ַ���')
    
    args = parser.parse_args()
    
    if args.enc:
 
        print(decrypt_forgot_issuer(args.enc))
    elif args.dec:

        print(forgot_issuer(args.dec))

