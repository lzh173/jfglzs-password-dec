# -*- coding: GBK -*-
import sys
import getopt
from datetime import datetime

def parse_arguments(argv):
    """
    解析命令行参数
    返回: datetime对象
    """
    date_str = None
    
    try:
        # 只解析-h和日期参数（非选项参数）
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError as err:
        print(f"参数错误: {err}")
        print_help()
        sys.exit(2)
    
    # 处理选项
    for opt, _ in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
    
    # 获取日期参数（非选项参数）
    if len(args) == 1:
        date_str = args[0]
    elif len(args) > 1:
        print("错误: 只能指定一个日期参数")
        print_help()
        sys.exit(2)
    else:
        print("错误: 必须指定日期参数")
        print_help()
        sys.exit(2)
    
    # 转换日期格式
    try:
        date_obj = datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        print(f"错误: 无效的日期格式 '{date_str}'，请使用YYYYMMDD格式")
        print_help()
        sys.exit(2)
    
    return date_obj

def print_help():
    """打印帮助信息"""
    print("用法: script.py [选项] YYYYMMDD")
    print("选项:")
    print(" -h, --help  显示帮助信息")
    print("\n示例:")
    print(" script.py 20250401   # 处理2025年4月1日")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_help()
        sys.exit()
    
    date = parse_arguments(sys.argv[1:])
    print(f"成功解析日期: {date.strftime('%Y-%m-%d')}")