def rate_issuer(input_str):
    """安全的加密函数"""
    result = []
    for char in input_str:
        original = ord(char)
        if 32 <= original <= 126:  # 可打印ASCII范围
            new_code = (original - 10 - 32) % 95 + 32
            result.append(chr(new_code))
        else:
            result.append(char)
    return ''.join(result)

def view_issuer(encrypted_str):
    """对应的解密函数"""
    result = []
    for char in encrypted_str:
        original = ord(char)
        if 32 <= original <= 126:
            new_code = (original + 10 - 32) % 95 + 32
            result.append(chr(new_code))
        else:
            result.append(char)
    return ''.join(result)

# 测试
test_cases = [
    "Hello World!",
    "Python 3.9",
    "ABCabc123",
    "Special@Chars#",
    "低码点字符: \x01\x02",
    "高码点字符: 你好"
]

for text in test_cases:
    print(f"原始: {text!r}")
    encrypted = rate_issuer(text)
    print(f"加密: {encrypted!r}")
    decrypted = view_issuer(encrypted)
    print(f"解密: {decrypted!r}")
    print("-" * 40)