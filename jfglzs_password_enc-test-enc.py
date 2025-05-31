import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad

def decrypt_newpage(encrypted_b64: str) -> str:
    """
    解密被NewPage加密的字符串
    Args:
        encrypted_b64: Base64编码的加密字符串
    Returns:
        解密后的原始字符串
    """
    # 固定密钥和IV（必须与加密时一致）
    KEY = b"zm2025jf"  # 取硬编码字符串前8字节
    IV = b"m2025jfg"   # 从第2字符开始取8字节

    try:
        # 1. Base64解码
        encrypted_data = base64.b64decode(encrypted_b64)
        
        # 2. 初始化DES解密器
        cipher = DES.new(KEY, DES.MODE_CBC, IV)
        
        # 3. 解密并移除填充
        decrypted_data = cipher.decrypt(encrypted_data)
        plaintext = unpad(decrypted_data, DES.block_size).decode('utf-8')
        
        return plaintext
    except Exception as e:
        raise ValueError(f"解密失败: {str(e)}")
    
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import base64

def encrypt_newpage(plaintext: str) -> str:
    """与原始VB.NET的NewPage完全等效的加密函数"""
    KEY = b"zm2025jf"
    IV = b"m2025jfg"
    
    cipher = DES.new(KEY, DES.MODE_CBC, IV)
    padded_data = pad(plaintext.encode('utf-8'), DES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    return base64.b64encode(encrypted_data).decode('utf-8')

test_cases = [
    "1",
    "1qaz2wss",

]

# 完整测试
for text in test_cases:
    print(f"原始字符串: {text}")
    
    # 加密
    encrypted = encrypt_newpage(text)
    print(f"加密结果(Base64): {encrypted}")
    
    # 解密
    decrypted = decrypt_newpage(encrypted)
    print(f"解密结果: {decrypted}")
    print("-" * 40)