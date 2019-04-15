#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2019-1-29 17:56
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : threeWord.py
# @Software: PyCharm
#爬取并整理规范机场三字码信息

import requests
from bs4 import BeautifulSoup
import time

url_1 = 'https://airport.supfree.net/index.asp?page='
for i in range(1,285):
    url = url_1 + str(i)
    html = requests.get(url)
    html.encoding = 'gbk'
    soup = BeautifulSoup(html.text, 'lxml')
    data_list = soup.find_all('tr')[1:]
    for i in data_list:
        td_data = []
        for td in i:
            if(td.string is None):
                td_data.append('')
            else:
                td_data.append(td.string)

        line_data = ','.join(td_data).replace('\n,','')[:-2] + '\n'

        file = open('f:/airport_code.csv', 'a', encoding='UTF-8')
        file.write(line_data)
        file.close()
        print(td_data)
        print(line_data)
    time.sleep(3)