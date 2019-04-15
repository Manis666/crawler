#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2019-1-30 12:08
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : distance1.py
# @Software: PyCharm
#通过url特性人为构造url并访问爬取数据，distance的补充，distance未爬完报错的重新在字典里循环

import requests
from bs4 import BeautifulSoup
import re
import time
import random
# '文山市': '27081606','威远镇': '27090629',
# yn_city_dict = {'镇雄县': '27108396'}
# province_dict = {'安徽省': '01', '浙江省': '02', '江西省': '03', '江苏省': '04', '吉林省': '05', '青海省': '06', '福建省': '07', '黑龙江省': '08', '河南省': '09', '河北省': '10', '湖南省': '11', '湖北省': '12', '新疆省': '13', '西藏省': '14', '甘肃省': '15', '广西省': '16', '贵州省': '18', '辽宁省': '19', '内蒙古省': '20', '宁夏省': '21', '北京直辖市': '22', '上海直辖市': '23', '山西省': '24', '山东省': '25', '陕西省': '26', '天津直辖市': '28', '云南省': '29', '广东省': '30', '海南省': '31', '四川省': '32', '重庆直辖市': '33'}
yn_city_dict = {'昭通市': '27077382'}
province_dict = {'北京直辖市': '22', '上海直辖市': '23', '山西省': '24', '山东省': '25', '陕西省': '26', '天津直辖市': '28', '云南省': '29', '广东省': '30', '海南省': '31', '四川省': '32', '重庆直辖市': '33'}

url_s = 'http://www.china6636.com/from/29-'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
proxy_list = ['35.232.44.140:3128', '142.93.73.92:8080', '159.65.224.231:8080', '104.248.126.17:8080', '157.230.91.214:80', '104.248.118.217:8080', '68.183.62.255:8080', '167.99.52.107:8888', '67.205.143.4:8080', '18.234.38.192:8080', '168.11.14.250:8009', '167.114.65.232:3128', '168.216.24.246:8080', '206.125.41.135:80', '35.185.201.225:8080', '142.93.243.115:8080', '51.75.65.79:8080', '5.135.164.72:3128', '187.217.188.153:8080', '46.101.138.229:8080', '62.7.85.234:8080', '142.93.133.37:8080', '5.189.177.94:10010', '200.255.122.174:8080', '140.227.207.211:60088', '185.80.130.26:8080', '94.242.58.142:1448', '94.242.59.135:10010', '5.2.140.152:3128', '140.227.209.210:60088']
proxy = random.sample(proxy_list, 1)

all = []



def openURL(url):
    url_00 = 'http://www.china6636.com'
    while True:
        try:
            proxy = random.sample(proxy_list, 1)[0]
            html = requests.get(url, headers=headers, proxies={'https': 'https://' + proxy})
            break
        except Exception as e:
            print(str(e))
            print(proxy)
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



for i in yn_city_dict:
    for j in province_dict:
        url = url_s + yn_city_dict[i] + '-' + province_dict[j]
        print(i,j)
        openURL(url)