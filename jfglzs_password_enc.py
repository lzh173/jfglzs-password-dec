import hashlib
from Crypto.Cipher import DES
import base64
import winreg
from typing import Optional

class JfglzsPasswordSystem:
    def __init__(self):
        # 硬编码密钥 (从原始代码中提取)
        self.base_key = "7]F8H]&gd9*fCAd(B9(Z9PEIl+"
        self.key_extension = "P::9mnJ8,@b'I?I%.3"
        
        # DES加密配置
        self.des_key = "C:\\WIND"[:8].ljust(8, '\0').encode('utf-8')
        self.des_iv = "\\WINDOW"[:8].ljust(8, '\0').encode('utf-8')

    # ------------------------- 核心逆向方法 -------------------------
    
    def _reverse_destroy_adapter(self, encoded_str: str) -> str:
        """逆向DestroyAdapter的ASCII位移操作"""
        return ''.join([chr(ord(c) + 10) for c in encoded_str])

    def _decrypt_insert_adapter(self, encrypted_data: str) -> str:
        """逆向InsertAdapter的DES解密"""
        try:
            # Base64解码
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            # DES解密
            cipher = DES.new(self.des_key, DES.MODE_CBC, self.des_iv)
            decrypted = cipher.decrypt(encrypted_bytes)
            
            # 移除PKCS7填充
            padding_length = decrypted[-1]
            return decrypted[:-padding_length].decode('gbk', errors='ignore')
        except Exception as e:
            raise ValueError(f"DES解密失败: {str(e)}")

    def _search_adapter(self, input_str: str) -> str:
        """逆向SearchAdapter的MD5哈希截断"""
        md5 = hashlib.md5()
        md5.update(input_str.encode('gbk'))
        return md5.hexdigest()[10:30]  # 取第11-30位

    def _instantiate_adapter(self, key: str) -> str:
        """逆向InstantiateAdapter的路径生成(模拟)"""
        # 注意：这是推测实现，实际需要根据原始代码调整
        rotated = ''.join([chr(ord(c) - 1) for c in key])  # 简单位移
        return rotated.replace('@', '\\')  # 转换为注册表路径格式

    # ------------------------- 注册表操作 -------------------------

    def _read_registry(self, path: str) -> Optional[str]:
        """读取注册表值"""
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                value, _ = winreg.QueryValueEx(key, "")
                return str(value)
        except WindowsError:
            return None

    def check_antivirus_installed(self) -> bool:
        """检查杀毒软件注册表项"""
        locations = [
            r"Software\360m",
            r"Software\pd",
            r"Software\jfglzs\usb_jianche"
        ]
        return any(self._read_registry(loc) for loc in locations)

    # ------------------------- 完整验证流程 -------------------------

    def validate_password_change(
        self, 
        old_password: str, 
        new_password: str,
        check_antivirus: bool = True
    ) -> dict:
        """
        完整密码修改验证流程
        返回: {
            "success": bool,
            "message": str,
            "requires_antivirus_uninstall": bool
        }
        """
        # 1. 新密码检查
        if len(new_password) < 6:
            return {"success": False, "message": "新密码需≥6位"}
        if new_password == "123456":
            return {"success": False, "message": "密码太简单"}

        # 2. 原密码验证
        try:
            # 加密流程: InsertAdapter → SearchAdapter
            encrypted = self._encrypt_password(old_password)
            input_hash = self._search_adapter(encrypted)
            
            # 获取注册表存储值
            reg_path = self._instantiate_adapter(self.base_key + self.key_extension)
            stored_hash = self._read_registry(reg_path)
            
            if not stored_hash or input_hash != stored_hash:
                return {"success": False, "message": "原密码不正确"}
        except Exception as e:
            return {"success": False, "message": f"密码验证异常: {str(e)}"}

        # 3. 杀毒软件检查
        if check_antivirus and self.check_antivirus_installed():
            return {
                "success": False,
                "message": "请卸载安全软件",
                "requires_antivirus_uninstall": True
            }

        return {"success": True, "message": "验证通过"}

    # ------------------------- 辅助方法 -------------------------

    def _encrypt_password(self, password: str) -> str:
        """模拟InsertAdapter加密流程"""
        cipher = DES.new(self.des_key, DES.MODE_CBC, self.des_iv)
        padded = password.encode('gbk') + bytes([8 - len(password) % 8] * (8 - len(password) % 8))
        encrypted = cipher.encrypt(padded)
        return base64.b64encode(encrypted).decode()

    def generate_registry_hash(self, password: str) -> str:
        """生成应存储在注册表中的哈希值"""
        encrypted = self._encrypt_password(password)
        return self._search_adapter(encrypted)


if __name__ == "__main__":
    system = JfglzsPasswordSystem()
    
    # 示例1: 密码验证测试
    print("=== 密码验证测试 ===")
    result = system.validate_password_change(
        old_password="correct_password",
        new_password="new_secure_pwd"
    )
    print(result)

    # 示例2: 生成注册表哈希
    print("\n=== 注册表哈希生成 ===")
    hash_value = system.generate_registry_hash("my_password")
    print(f"应存储在注册表中的哈希: {hash_value}")

    # 示例3: 完整逆向测试
    print("\n=== 完整逆向测试 ===")
    test_password = "test123"
    encrypted = system._encrypt_password(test_password)
    print(f"加密结果: {encrypted}")
    
    decrypted = system._decrypt_insert_adapter(
        system._reverse_destroy_adapter(encrypted)
    )
    print(f"解密结果: {decrypted}")