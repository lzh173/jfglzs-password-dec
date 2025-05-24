def rate_issuer(input_str):
    """��ȫ�ļ��ܺ���"""
    result = []
    for char in input_str:
        original = ord(char)
        if 32 <= original <= 126:  # �ɴ�ӡASCII��Χ
            new_code = (original - 10 - 32) % 95 + 32
            result.append(chr(new_code))
        else:
            result.append(char)
    return ''.join(result)

def view_issuer(encrypted_str):
    """��Ӧ�Ľ��ܺ���"""
    result = []
    for char in encrypted_str:
        original = ord(char)
        if 32 <= original <= 126:
            new_code = (original + 10 - 32) % 95 + 32
            result.append(chr(new_code))
        else:
            result.append(char)
    return ''.join(result)

# ����
test_cases = [
    "Hello World!",
    "Python 3.9",
    "ABCabc123",
    "Special@Chars#",
    "������ַ�: \x01\x02",
    "������ַ�: ���"
]

for text in test_cases:
    print(f"ԭʼ: {text!r}")
    encrypted = rate_issuer(text)
    print(f"����: {encrypted!r}")
    decrypted = view_issuer(encrypted)
    print(f"����: {decrypted!r}")
    print("-" * 40)