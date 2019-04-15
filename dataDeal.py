#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2019-2-12 10:56
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : dataDeal.py
# @Software: PyCharm
#通过url特性人为构造url并访问爬取数据

import pandas
import requests
from bs4 import BeautifulSoup
import re
import time
# http://www.gcmap.com/dist?P=AHJ-LXA
names = ['code1','city1','code2','city2']
pd_excel = pandas.read_excel('f:/001.xls', names = names, header=None)
print(pd_excel)

tabele = pd_excel['code1'] + '-' + pd_excel['code2']
url_suffix = tabele.values.tolist()


def getDistance(string):
    url_first = 'http://www.gcmap.com/dist?P='
    url = url_first + string
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    distance = str(soup.select('#mdist > tfoot > tr > td')[0].find_all(text=True)[0])
    return distance

data = []
data_a = []
for i in url_suffix:
    try:
        d = getDistance(i)
        data.append(d)
        data_a.append(i + ',' + d)
        print(d)
        time.sleep(20)
    except Exception as e:
        print(i + d)
        print(str(e))

file = open('f:/zhiding_distance.csv', 'a', encoding='UTF-8')
file.write('\n'.join(data))
file.close()