# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018/10/8
"""

import os
import re
import numpy as np
import pandas as pd
import requests
from pprint import pprint
from bs4 import BeautifulSoup

from crawler_myTools.requests_tools.common_config import MyRequestsConfig
from crawler_myTools.common.UserAgent import get_random_UA

from crawler_myTools.selenium_tools.webdriver import MyWebDriver


def selenium_main():
    driver = MyWebDriver(driver_type=2)
    # url = "http://www.baidu.com"
    url = 'https://blog.csdn.net/ratsniper/article/details/78954852#class-names-%E7%B1%BB%E5%90%8D'
    driver.get(url)
    driver.slide_down()


def main():
    # 1. 设置请求参数
    proxies = {
        'http': 'http://127.0.0.1:54422',
        'https': 'https://127.0.0.1:54422',
    }
    headers = {'Connection': 'Keep-Alive'
               # ,'host': 'zhannei.baidu.com'
               # ,'ref??': ''
                , 'User-Agent': get_random_UA()
    }
    params = {

    }

    # 2. 发送请求并解析回复
    url = "http://www.baidu.com"
    # requests.get(url, headers=headers, proxies=proxies, params=params)
    response = requests.get(url, headers=headers)
    page_source = response.content.decode('utf8')
    # 将页面源代码写到临时html文件
    # with open('temp.html', 'r', encoding='utf8') as fout:
    #     fout.write(page_source)
    # or 直接输出页面源代码
    pprint(page_source)


if __name__ == "__main__":
    # main()
    selenium_main()