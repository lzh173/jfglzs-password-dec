# -*- coding: GBK -*-
from math import log
import loguru
import requests
from datetime import datetime, timedelta
from loguru import logger
logo = '''

██████╗ ██╗   ██╗    ██╗     ███████╗██╗  ██╗ ██╗███████╗██████╗ 
██╔══██╗╚██╗ ██╔╝    ██║     ╚══███╔╝██║  ██║███║╚════██║╚════██╗
██████╔╝ ╚████╔╝     ██║       ███╔╝ ███████║╚██║    ██╔╝ █████╔╝
██╔══██╗  ╚██╔╝      ██║      ███╔╝  ██╔══██║ ██║   ██╔╝  ╚═══██╗
██████╔╝   ██║       ███████╗███████╗██║  ██║ ██║   ██║  ██████╔╝
╚═════╝    ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═╝   ╚═╝  ╚═════╝ 
                                                                                                                                                   
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
        # 解析日期格式示例: 'Wed, 21 Oct 2015 07:28:00 GMT'
        parsed_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        beijing_time = parsed_date + timedelta(hours=8)
        return beijing_time
    except Exception:
        # 失败时返回当前北京时间
        return datetime.utcnow() + timedelta(hours=8)

def sort_issuer():
    date_time = flush_issuer()
    # 如果时间为零点则使用当前时间（容错逻辑）
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
        # 此处执行验证通过后的操作（原C#中的NewIssuer和QueryIssuer）
        return True, "", valid_code

# 使用示例
if __name__ == "__main__":
    print(logo)
    nowday = str(datetime.now().strftime('%Y-%m-%d'))
    logger.info("现在时间：" + nowday)
    logger.info("正在计算临时密码！")
    # 生成合法测试代码（假设当前时间有效）
    valid_code = "8" + sort_issuer().strip()
    print(f"生成的合法代码: {valid_code}")
    
    # 测试验证函数
    test_cases = [
        valid_code,          # 正确代码

    ]
    
    for code in test_cases:
        is_valid, msg, _ = disable_issuer(code)
        if msg == "":
            msg = "无"
        print(f"输入: {code}\n验证结果: {'通过' if is_valid else '失败'}\n错误信息: {msg}\n")
        logger.info("请按回车键退出")
        input()