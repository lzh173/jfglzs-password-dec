# -*- coding: GBK -*-
from getopt import getopt
import getopt
from math import log
import sys
import loguru
import requests
from datetime import datetime, timedelta
from loguru import logger
logo = '''

�������������[ �����[   �����[    �����[     ���������������[�����[  �����[ �����[���������������[�������������[ 
�����X�T�T�����[�^�����[ �����X�a    �����U     �^�T�T�������X�a�����U  �����U�������U�^�T�T�T�T�����U�^�T�T�T�T�����[
�������������X�a �^���������X�a     �����U       �������X�a ���������������U�^�����U    �����X�a �����������X�a
�����X�T�T�����[  �^�����X�a      �����U      �������X�a  �����X�T�T�����U �����U   �����X�a  �^�T�T�T�����[
�������������X�a   �����U       ���������������[���������������[�����U  �����U �����U   �����U  �������������X�a
�^�T�T�T�T�T�a    �^�T�a       �^�T�T�T�T�T�T�a�^�T�T�T�T�T�T�a�^�T�a  �^�T�a �^�T�a   �^�T�a  �^�T�T�T�T�T�a 
                                                                                                                                                   
'''


def print_help():
    """��ӡ������Ϣ"""
    print("�÷�: script.py YYYYMMDD")
    print("ѡ��:")
    print(" -h, --help  ��ʾ������Ϣ")
    print("\nʾ��:")
    print(" script.py 20250401   #����2025��4��1�յ���ʱ����")




def flush_issuer(date_str):
    
    if date_str == "":
        logger.warning("û������ʱ�䣬Ĭ�ϼ��������ʱ����")
        date_time = datetime.utcnow()
        return date_time + timedelta(hours=8)
    
    date_obj = datetime.strptime(date_str, "%Y%m%d")
    ret = date_obj + timedelta(hours=8)

    return ret
    

def sort_issuer(date_str):
    date_time = flush_issuer(date_str)
    # ���ʱ��Ϊ�����ʹ�õ�ǰʱ�䣨�ݴ��߼���
    if date_time.time() == datetime.min.time():
        date_time = datetime.utcnow() + timedelta(hours=8)
    
    month_part = date_time.month * 13
    day_part = date_time.day * 57
    year_part = date_time.year * 91
    total = (month_part + day_part + year_part) * 16 + 11
    return str(total)

def disable_issuer(pd_old_text):
    valid_code = sort_issuer().strip()
    
    if not pd_old_text:
        return False, "error", ""
    
    first_char = pd_old_text[0] if pd_old_text else ""
    remaining = pd_old_text[1:].strip() if len(pd_old_text) > 1 else ""
    
    if first_char != "8" or remaining != valid_code:
        return False, "error", ""
    else:
        # �˴�ִ����֤ͨ����Ĳ�����ԭC#�е�NewIssuer��QueryIssuer��
        return True, "", valid_code


# ʹ��ʾ��
if __name__ == "__main__":
    print(logo)
    logger.info("������YYYYMMDD��ʽ��ʱ��:")
    date_str = input()
    logger.info("����ʱ�䣺" + str(flush_issuer(date_str)))
    logger.info("���ڼ�����ʱ���룡")
    # ���ɺϷ����Դ��루���赱ǰʱ����Ч��
    valid_code = "8" + sort_issuer(date_str).strip()
    print(f"���ɵĺϷ�����: {valid_code}")
    logger.info("�밴�س����˳�")
    input()

