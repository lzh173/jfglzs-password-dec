# -*- coding: GBK -*-
from math import log
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

def flush_issuer():
    try:
        response = requests.head(
            'http://www.baidu.com',
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=5
        )
        response.raise_for_status()
        date_str = response.headers.get('Date', '')
        # �������ڸ�ʽʾ��: 'Wed, 21 Oct 2015 07:28:00 GMT'
        parsed_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        beijing_time = parsed_date + timedelta(hours=8)
        return beijing_time
    except Exception:
        # ʧ��ʱ���ص�ǰ����ʱ��
        return datetime.utcnow() + timedelta(hours=8)

def sort_issuer():
    date_time = flush_issuer()
    # ���ʱ��Ϊ�����ʹ�õ�ǰʱ�䣨�ݴ��߼���
    if date_time.time() == datetime.min.time():
        date_time = datetime.utcnow() + timedelta(hours=8)
    
    month_part = date_time.month * 13
    day_part = date_time.day * 57
    year_part = date_time.year * 91
    total = (month_part + day_part + year_part) * 16
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
    nowday = str(datetime.now().strftime('%Y-%m-%d'))
    logger.info("����ʱ�䣺" + nowday)
    logger.info("���ڼ�����ʱ���룡")
    # ���ɺϷ����Դ��루���赱ǰʱ����Ч��
    valid_code = "8" + sort_issuer().strip()
    print(f"���ɵĺϷ�����: {valid_code}")
    
    # ������֤����
    test_cases = [
        valid_code,          # ��ȷ����

    ]
    
    for code in test_cases:
        is_valid, msg, _ = disable_issuer(code)
        if msg == "":
            msg = "��"
        print(f"����: {code}\n��֤���: {'ͨ��' if is_valid else 'ʧ��'}\n������Ϣ: {msg}\n")
        logger.info("�밴�س����˳�")
        input()