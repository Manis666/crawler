#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2018-9-21 10:09
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : ProxyIP20.py
# @Software: PyCharm
#获取代理，与另一个网址不同所以解析不同



import requests
from bs4 import BeautifulSoup
import json


def getProxy():
    url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
    header = {'User_Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    resq = requests.get(url, headers=header)
    _text_list = resq.text
    _json_str = '[' + _text_list.replace('}\n{','},{') + ']'
    _s = json.loads(_json_str)
    ips = []
    a = 0
    for i in _s:
        if i['type'] == 'https':
            ip = str(i['host']) + ':' + str(i['port'])
            url = "https://www.ipip.net/"
            try:
                proxy_host = "https://" + ip
                proxy_temp = {"https": proxy_host}
                res = requests.get(url, proxies=proxy_temp, timeout=2)
                ips.append(ip)
                a += 1
                if a == 30:
                    break
                print(ip + '\n ')
            except Exception as e:
                print(str(i) + '失败！' + str(e))
    print(ips)
    print(len(ips))


getProxy()
