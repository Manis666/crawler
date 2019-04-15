#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2018-9-19 14:22
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : ProxyIp.py
# @Software: PyCharm
#获取代理

import urllib
import requests
from bs4 import BeautifulSoup
import urllib
import socket

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

'''
获取所有代理IP地址
'''


def getProxyIp():
    proxy = []
    for i in range(1,3):
        try:
            url1 = 'http://www.xicidaili.com/nn/' + str(i)
            resq = requests.get(url1, headers=header)
            res = resq.text
            soup = BeautifulSoup(res, 'lxml')
            ips = soup.findAll('tr')
            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
                proxy.append(ip_temp)
        except:
            continue
    return proxy


'''
验证获得的代理IP地址是否可用
'''


def validateIp(proxy):
    url = "https://www.ipip.net/"
    f = open("E:\ip.txt", "w")
    for i in proxy:
        try:
            ip = i.strip()
            proxy_host = "http://" + ip
            proxy_temp = {"http": proxy_host}
            res = requests.get(url, proxies=proxy_temp, timeout = 2 )
            #f.write(proxy[i] + '\n')
            print(i)
        except Exception as e:
            print(str(i) + '失败！' + str(e))
    f.close()


if __name__ == '__main__':
    proxy = getProxyIp()
    print(proxy)
    validateIp(proxy)