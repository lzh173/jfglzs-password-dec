# -*- coding: GBK -*-
import sys
import getopt
from datetime import datetime

def parse_arguments(argv):
    """
    ���������в���
    ����: datetime����
    """
    date_str = None
    
    try:
        # ֻ����-h�����ڲ�������ѡ�������
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError as err:
        print(f"��������: {err}")
        print_help()
        sys.exit(2)
    
    # ����ѡ��
    for opt, _ in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
    
    # ��ȡ���ڲ�������ѡ�������
    if len(args) == 1:
        date_str = args[0]
    elif len(args) > 1:
        print("����: ֻ��ָ��һ�����ڲ���")
        print_help()
        sys.exit(2)
    else:
        print("����: ����ָ�����ڲ���")
        print_help()
        sys.exit(2)
    
    # ת�����ڸ�ʽ
    try:
        date_obj = datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        print(f"����: ��Ч�����ڸ�ʽ '{date_str}'����ʹ��YYYYMMDD��ʽ")
        print_help()
        sys.exit(2)
    
    return date_obj

def print_help():
    """��ӡ������Ϣ"""
    print("�÷�: script.py [ѡ��] YYYYMMDD")
    print("ѡ��:")
    print(" -h, --help  ��ʾ������Ϣ")
    print("\nʾ��:")
    print(" script.py 20250401   # ����2025��4��1��")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_help()
        sys.exit()
    
    date = parse_arguments(sys.argv[1:])
    print(f"�ɹ���������: {date.strftime('%Y-%m-%d')}")