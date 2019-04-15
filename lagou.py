#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2018-9-19 9:50
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : lagou.py
# @Software: PyCharm
#拉勾网职位信息爬取，实现动态更新代理池有效代理，并剔除无效代理

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from multiprocessing import Pool
import random
import json
import time


def getProxyIp():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    proxy = []
    try:
        url1 = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
        url2 = 'https://www.ipip.net/'
        resq = requests.get(url1, headers=header)
        res = '[' + resq.replace('}\n{','},{') + ']'

        _s = json.loads(res)
        ips = []
        for i in _s:
            if i['type'] == 'https':
                ip = str(i['host']) + ':' + str(i['port'])
                ips.append(ip)

        for x in ips:
            try:
                requests.get(url2, proxies={'http':'http://'+x},timeout = 2)
                proxy.append(x)
            except Exception as e:
                print(str(e))
    except Exception as e:
        print(str(e))
    return proxy

# 获取页面源码函数
def get_page_resp():
    url ='https://www.lagou.com/'
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)'
    ]
    user_agent = random.choice(user_agent_list)
    headers = {
        'User-Agent': user_agent,
    }

    proxy_list = ['35.224.248.29:3128', '104.198.68.109:3128', '181.215.114.240:8881', '52.179.5.76:8080', '142.93.123.116:8080', '104.248.61.63:8080', '167.99.15.36:8080', '34.239.144.212:29841', '142.93.51.134:8080', '178.128.154.246:8080', '104.248.61.157:8080', '142.93.59.200:3128', '64.72.84.90:8080', '98.101.202.219:8080', '54.39.97.250:3128', '23.101.121.11:3128', '35.237.208.149:3128', '142.93.254.37:8080', '34.204.87.36:29841', '104.248.123.132:3128', '34.211.41.52:3128', '209.34.29.9:8181', '206.125.41.135:80', '54.209.241.24:29841', '168.216.24.246:8080', '142.93.251.84:8080', '23.253.218.68:3128', '138.197.193.129:8080', '198.50.251.188:808', '35.231.123.57:3128']

    proxy_ip = random.choice(proxy_list)

    try:
        resp = requests.get(url, headers=headers, proxies={'https':'https://' + proxy_ip})
        if resp.status_code == 200:
            return resp.text
        print(resp.status_code)
    except RequestException as e:
        print(str(e))

#获取所有职位极其href
def getHrefData():
    soup = BeautifulSoup(get_page_resp(), 'lxml')

    all_positions = soup.select('div.menu_sub.dn > dl > dd > a')

    joburls = [i['href'] for i in all_positions]
    jobnames = [i.get_text() for i in all_positions]
    data = zip(joburls,jobnames)
    return data

#爬取所有href的信息
def getHrefInfo(url, a):

    url_h = url #'https://www.lagou.com/zhaopin/chanpinjingli/3/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    proxy_list = ['35.224.248.29:3128', '104.198.68.109:3128', '181.215.114.240:8881', '52.179.5.76:8080', '142.93.123.116:8080', '104.248.61.63:8080', '167.99.15.36:8080', '34.239.144.212:29841', '142.93.51.134:8080', '178.128.154.246:8080', '104.248.61.157:8080', '142.93.59.200:3128', '64.72.84.90:8080', '98.101.202.219:8080', '54.39.97.250:3128', '23.101.121.11:3128', '35.237.208.149:3128', '142.93.254.37:8080', '34.204.87.36:29841', '104.248.123.132:3128', '34.211.41.52:3128', '209.34.29.9:8181', '206.125.41.135:80', '54.209.241.24:29841', '168.216.24.246:8080', '142.93.251.84:8080', '23.253.218.68:3128', '138.197.193.129:8080', '198.50.251.188:808', '35.231.123.57:3128']
    proxy_ip = proxy_list[a]
    #获取新的有效ip  当原来的ip连接不上的时候删除并获得新的ip加入到代理池中
    while True:
        try:
            resq = requests.get(url_h,headers=headers,proxies={'https':'https://' + proxy_ip})
            if resq.status_code == 200:
                break
            else:
                proxy_list.remove(proxy_ip)
                _new_ip = getProxyIp()
                for ip in _new_ip:
                    if ip not in proxy_list:
                        proxy_list.append(ip)
                        break
        except Exception as e:
            proxy_list.remove(proxy_ip)
            _new_ip = getProxyIp()
            for ip in _new_ip:
                if ip not in proxy_list:
                    proxy_list.append(ip)
                    break
            proxy_ip = random.choice(proxy_list)
            print(proxy_ip + "已从代理池中移除" + '已添加新ip进入代理池' + str(e))
        time.sleep(3)

    if resq.status_code == 200:
        # print('已获取到html')

        try:
            soup = BeautifulSoup(resq.text, 'lxml')
            # print('已经解析成功！！！')
        except Exception as e:
            print('解析不成功！' + str(e))

        # print(soup)

        #职位信息
        positions = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > h3')

        #工作地址
        adds = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > span > em')

        #发布时间
        publishs = soup.select('ul > li > div.list_item_top > div.position > div.p_top > span')

        #薪资信息
        moneys = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div > span')

        #工作要求
        needs = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div')

        #发布公司
        companys = soup.select('ul > li > div.list_item_top > div.company > div.company_name > a')

        #招聘标签信息
        tags = soup.select('ul > li > div.list_item_bot > div.li_b_l')

        #公司福利
        welfares = soup.select('ul > li > div.list_item_bot > div.li_b_r')

        data = []
        for position, add, publish, money, need, company, tag, welfare in zip(positions, adds, publishs, moneys, needs, companys, tags, welfares):
            data_temp = {
                'position': position.get_text(),
                'add': add.get_text(),
                'publish': publish.get_text(),
                'money': money.get_text(),
                'need': need.get_text().split('\n')[2],
                'company': company.get_text(),
                'tag': tag.get_text().replace('\n', '-'),
                'welfare': welfare.get_text().replace('\n','')
            }
            print(data_temp)
            data.append('|'.join(data_temp.values()))
        if len(data) == 0:
            print(soup)
        file = open('f:/lagou.csv','a',encoding='UTF-8')
        file.write('\n'.join(data))
        file.close()
    else:print(resq.status_code)


# def main(page):
#     urls = getHrefData()
#     a = 0
#     for i in urls:
#         for p in range(1,31):
#             url = i[0] + str(p)
#             getHrefInfo(url, a%100)
#             a += 1
#
# if __name__ == '__main__':
#     pool = Pool(processes=4)
#     pages = ([str(p) for p in range(1, 30)])
#     pool.map(main, pages)
#     pool.close()
#     pool.join()


def main(page):
    print('--------------------------------------------' + page + '----------------------------------------------------')

    urls = getHrefData()
    a = 0
    for i in urls:
        url = i[0] + page
        print(i[1] + url)
        getHrefInfo(url, a%30)
        a += 1

if __name__ == '__main__':
    pool = Pool(processes=4)
    pages = ([str(p) for p in range(1, 30)])
    pool.map(main, pages)
    pool.close()
    pool.join()



# url = 'https://www.lagou.com/zhaopin/C%23/3'
# getHrefInfo(url, 3)