#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2019-1-29 15:26
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : distance.py
# @Software: PyCharm
#通过url特性人为构造url并访问爬取数据

import requests
from bs4 import BeautifulSoup
import re
import time


url_1 = 'http://www.china6636.com/from/29-27080364-01'
html = requests.get(url_1)
html.encoding = 'utf-8'
soup = BeautifulSoup(html.text, 'lxml')
province = str(soup.select('#fromstate')[0]).replace(' ','').split('><')
province_rese1 = re.compile('([0-9]){2}')
province_dict = {}
for i in province:
    if province_rese1.search(i):
        province_value = i[i.index('>')-3:i.index('>')-1]
        province_name = i[i.index('>')+1:i.index('<')]
        province_dict[province_name] = province_value
print(province_dict)



yn_city = str(soup.select('#fromcity')[0]).replace(' ','').split('><')
yn_city_rese1 = re.compile('([0-9]){8}')
yn_city_dict = {}
for i in yn_city:
    if (yn_city_rese1.search(i)):
        city_name = i[i.index('>')+1:i.index('<')]
        city_value = str(yn_city_rese1.search(i))[-10:-2]
        yn_city_dict[city_name] = city_value
        print(city_name)
        print(city_value)
print(yn_city_dict)

url_s = 'http://www.china6636.com/from/29-'

all = []


def openURL(url):
    url_00 = 'http://www.china6636.com'
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    city_list = soup.select('#tocity > a')
    url_list = []
    for i in city_list:
        a = str(i)
        url_suffix = url_00 + a[a.index('"') + 1:a.index('>') - 1]
        url_list.append(url_suffix)



    for i in url_list:
        html1 = requests.get(i)
        html1.encoding = 'utf-8'
        soup1 = BeautifulSoup(html1.text, 'lxml')
        city1 = soup1.select('div.col-md-8 > div.bread > a')[1].find_all(text=True)[0]
        city2 = soup1.select('div.col-md-8 > div.bread > span')[2].find_all(text=True)[0]
        distance = str(soup1.select('body > div.container > div > div.col-md-8 > div > p > b')[0]).replace('<b>','').replace( '</b>', '')

        data = []

        print(city1)
        print(city2)
        print(distance)

        data.append(city1 + ',' + city2 + ',' + distance + '\n')

        file = open('f:/hangju1.csv', 'a', encoding='UTF-8')
        file.write(''.join(data))
        file.close()

        time.sleep(2)



for i in yn_city_dict:
    for j in province_dict:
        url = url_s + yn_city_dict[i] + '-' + province_dict[j]
        print(i,j)
        openURL(url)





