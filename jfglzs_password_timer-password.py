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

██████╗ ██╗   ██╗    ██╗     ███████╗██╗  ██╗ ██╗███████╗██████╗ 
██╔══██╗╚██╗ ██╔╝    ██║     ╚══███╔╝██║  ██║███║╚════██║╚════██╗
██████╔╝ ╚████╔╝     ██║       ███╔╝ ███████║╚██║    ██╔╝ █████╔╝
██╔══██╗  ╚██╔╝      ██║      ███╔╝  ██╔══██║ ██║   ██╔╝  ╚═══██╗
██████╔╝   ██║       ███████╗███████╗██║  ██║ ██║   ██║  ██████╔╝
╚═════╝    ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═╝   ╚═╝  ╚═════╝ 
                                                                                                                                                   
'''


def print_help():
    """打印帮助信息"""
    print("用法: script.py YYYYMMDD")
    print("选项:")
    print(" -h, --help  显示帮助信息")
    print("\n示例:")
    print(" script.py 20250401   #计算2025年4月1日的临时密码")




def flush_issuer(date_str):
    
    if date_str == "":
        logger.warning("没有输入时间，默认计算今日临时密码")
        date_time = datetime.utcnow()
        return date_time + timedelta(hours=8)
    
    date_obj = datetime.strptime(date_str, "%Y%m%d")
    ret = date_obj + timedelta(hours=8)

    return ret
    

def sort_issuer(date_str):
    date_time = flush_issuer(date_str)
    # 如果时间为零点则使用当前时间（容错逻辑）
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
        # 此处执行验证通过后的操作（原C#中的NewIssuer和QueryIssuer）
        return True, "", valid_code


# 使用示例
if __name__ == "__main__":
    print(logo)
    logger.info("请输入YYYYMMDD格式的时间:")
    date_str = input()
    logger.info("输入时间：" + str(flush_issuer(date_str)))
    logger.info("正在计算临时密码！")
    # 生成合法测试代码（假设当前时间有效）
    valid_code = "8" + sort_issuer(date_str).strip()
    print(f"生成的合法代码: {valid_code}")
    logger.info("请按回车键退出")
    input()

