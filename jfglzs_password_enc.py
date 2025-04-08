from Crypto.Cipher import DES
import base64
import re

def reverse_destroy_adapter(encoded_str):
    """逆向DestroyAdapter的ASCII位移操作"""
    return ''.join([chr(ord(c) + 10) for c in encoded_str])

def decrypt_insert_adapter(encrypted_data):
    """解密InsertAdapter方法加密的数据"""
    # 修正后的密钥和IV (确保8字节长度)
    key = "C:\\WIND".ljust(8, '\0')[:8].encode('utf-8')
    iv = "\\WINDOW".ljust(8, '\0')[:8].encode('utf-8')
    
    try:
        # 清理可能的非Base64字符
        encrypted_data = re.sub(r'[^a-zA-Z0-9+/=]', '', encrypted_data)
        
        # 添加必要的Base64填充
        pad_len = len(encrypted_data) % 4
        if pad_len:
            encrypted_data += '=' * (4 - pad_len)
        
        # 解码Base64
        encrypted_bytes = base64.b64decode(encrypted_data)
        
        # 检查数据长度是否为8的倍数
        if len(encrypted_bytes) % 8 != 0:
            # 填充到8字节边界
            encrypted_bytes += b'\0' * (8 - len(encrypted_bytes) % 8)
        
        # 初始化DES解密器
        cipher = DES.new(key, DES.MODE_CBC, iv)
        
        # 解密
        decrypted = cipher.decrypt(encrypted_bytes)
        
        # 移除可能的填充 (PKCS5/PKCS7)
        try:
            padding_length = decrypted[-1]
            if padding_length <= 8:  # 合理的填充长度
                decrypted = decrypted[:-padding_length]
        except:
            pass  # 如果移除填充失败，保留原数据
        
        return decrypted.decode('utf-8', errors='ignore').strip()
    except Exception as e:
        raise ValueError(f"解密失败: {str(e)}")

def full_decrypt(processed_data):
    """完整解密流程"""
    # 1. 逆向DestroyAdapter的ASCII变换
    ascii_fixed = reverse_destroy_adapter(processed_data)
    
    # 2. DES解密
    return decrypt_insert_adapter(ascii_fixed)

if __name__ == "__main__":
    print("=== DestroyAdapter单独解密测试 ===")
    destroyed_data = "j]ij"  # "test"经过DestroyAdapter后的结果
    print(f"原始数据: 'test' → DestroyAdapter处理后: {destroyed_data}")
    print(f"逆向解密结果: {reverse_destroy_adapter(destroyed_data)}")
    
    print("\n=== 完整解密流程测试 ===")
    test_cases = [
        "d4158ce43c3944953bb8",  # 您的第一个测试数据
        "a1b2c3d4e5f6=",         # 您的第二个测试数据
        "k3F5j7s2aXo="           # 之前的示例数据
    ]
    
    for encrypted in test_cases:
        try:
            print(f"\n尝试解密: {encrypted}")
            result = full_decrypt(encrypted)
            print(f"解密结果: {result!r}")  # 使用!r显示原始格式
            print(f"十六进制表示: {result.encode('utf-8').hex()}")
        except Exception as e:
            print(f"解密出错: {e}")