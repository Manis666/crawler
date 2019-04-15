#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2018-9-19 14:30
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : text.py
# @Software: PyCharm
#编程时测试试水

import urllib
import requests
from bs4 import BeautifulSoup
import urllib
import socket
import time
from urllib.request import urlretrieve
from selenium import webdriver
import os
import xlwt
import xlrd
from xlutils.copy import copy
import pytesseract
from PIL import Image
import ftplib


file = '2taobaozongchong/1.xls'
p1 = os.path.exists(file)
print(p1)
if not p1:
    excelTabel = xlwt.Workbook()  # 创建excel对象
    excelTabel.add_sheet('项目', cell_overwrite_ok=True)
    excelTabel.add_sheet('基地', cell_overwrite_ok=True)
    excelTabel.save(file)

# ftp = ftplib.FTP()
# ftp.set_pasv(1)
#
# ftp.connect('10.6.183.172', 21)
# ftp.login('3umsg','Scal3459!@#')
# ftp.cwd('PRL/')
# filelist = ftp.nlst()
# flen = len(filelist)
# print(flen)
# print(filelist)


src = '//img.alicdn.com/tfscom/TB1gb2pAHrpK1RjSZTESuwWAVXahttps:'
if not src.startswith('https:'):
    src = 'https:' + src
print(src)

#递归遍历文件
# def all_path(dirname):
#
#     result = []#所有的文件
#
#     for f in os.walk(dirname):
#             print(f)
#
#     for maindir, subdir, file_name_list in os.walk(dirname):
#
#         print("1:",maindir) #当前主目录
#         print("2:",subdir) #当前主目录下的所有目录
#         print("3:",file_name_list)  #当前主目录下的所有文件
#
#         for filename in file_name_list:
#             apath = os.path.join(maindir, filename)#合并成一个完整路径
#             result.append(apath)
#
#     return result
#
# print(all_path('f:\study'))

# # exlcel写入操作
# s = [1,2,5,1,7,1,8,3]
# t = [1,4,2,5,1,7,1,8,1,6]
# file = '1.xls'
# p1 = os.path.exists(file)
# if not p1:
#         excelTabel = xlwt.Workbook()  # 创建excel对象
#         sheet1 = excelTabel.add_sheet('项目', cell_overwrite_ok=True)
#         sheet2 = excelTabel.add_sheet('基地', cell_overwrite_ok=True)
#         excelTabel.save(file)
#
# wb = xlrd.open_workbook(filename=file)
# row = wb.sheets()[0].nrows
# excel = copy(wb)
# table = excel.get_sheet(0)
# for i in range(0,len(s)):
#         table.write(row,i,'=' + str(s[i]) + '&CHAR(10)&' + str(s[i]))
# excel.save(file)

#
# #基地项目解析
# url = 'https://www.idianchou.com/pc/project/detail/?projectId=3335'
# browser = webdriver.Chrome()
# browser.get(url)
# time.sleep(3)
# html = browser.page_source
# soup = BeautifulSoup(html, 'html.parser')
#
#
# circulation_process = ''.join(
#         soup.select('div.identificationProcess > div.contentBox > div.process')[0].find_all(text=True)).replace('    ', '-->').replace(' ','')
# print(circulation_process)




# #图片文字提取
# url = 'https://www.idianchou.com/pc/project/detail/?projectId=3333'
# browser = webdriver.Chrome()
# browser.get(url)
# html = browser.page_source
# # time.sleep(3)
# soup = BeautifulSoup(html, 'html.parser')
# risk_review_text = soup.select('#infoContainer2')[0].find_all(text=True)
# risk_review = risk_review_text[0] + '\n' + \
#               risk_review_text[1].replace('\n', '').replace(' ', '') + '\n' + \
#               ''.join(risk_review_text[2:]).replace(' ', '')
#
# print(risk_review)

# # 点筹页面文档解析
# url = 'https://www.idianchou.com/pc/project/detail/?projectId=3333'
# browser = webdriver.Chrome()
# browser.get(url)
# html = browser.page_source
# # time.sleep(3)
# soup = BeautifulSoup(html, 'html.parser')
#
# project_name = soup.select('div.projectMainInfo > div > p')[0].find_all(text=True)[0]
# yi_choudao = soup.select('p.hasFundRow > span > i')[0].find_all(text=True)[0] + soup.select('div > p.hasFundRow > span')[0].find_all(text=True)[1]
# start_time = soup.select('div > p.upTime > span')[0].find_all(text=True)[0]
# progress = soup.select('div > div.el-progress.el-progress--line > div.el-progress__text')[0].find_all(text=True)[0].replace('\n','')
# distance = soup.select('div.projectData > div > span.data')
# target_amount = distance[0].find_all(text=True)[0].replace(' ','').replace('\n','')
# return_rate = distance[1].find_all(text=True)[0]
# time_limit = distance[2].find_all(text=True)[0]
# state = soup.select('div > div.buttonGroup > span.goFund.finished')[0].find_all(text=True)[0] + soup.select('div > div.buttonGroup > span.goFund.finished')[0].find_all(text=True)[1]
# risk_review = ''.join(soup.select('#infoContainer2')[0].find_all(text=True)).replace(' ','')
# record_list = soup.select('#infoContainer3')[0].find_all(text=True)[8:]
# a = 1
# b = len(record_list)/8
# while a<b:
#     record_list[a*8-1] = record_list[a*8-1] + '\n'
#     a += 1
# record = ''.join(record_list)
#
#
#
# print(project_name )
# print(yi_choudao)
# print(start_time)
# print(progress)
# print(target_amount)
# print(return_rate)
# print(time_limit)
# print(state)
# print(risk_review)
# print(record)




# url = 'http://www.gcmap.com/dist?P=JUH-NNG'
# html = requests.get(url)
# html.encoding = 'utf-8'
# soup = BeautifulSoup(html.text, 'lxml')
# distance = str(soup.select('#mdist > tfoot > tr > td')[0].find_all(text=True)[0])
# print(distance)

# #获取有效代理
# User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
# header = {}
# header['User-Agent'] = User_Agent
#
# #获取有效代理
# def getProxyIp():
#     proxy = []
#     for i in range(1, 2):
#         try:
#             url1 = 'http://www.xicidaili.com/wn/' + str(i)
#             url2 = 'https://www.ipip.net/'
#             resq = requests.get(url1, headers=header)
#             res = resq.text
#             soup = BeautifulSoup(res, 'lxml')
#             ips = soup.findAll('tr')
#             for x in range(1, len(ips)):
#                 ip = ips[x]
#                 tds = ip.findAll("td")
#                 ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
#                 try:
#                     requests.get(url2, proxies={'http':'http://'+ip_temp.strip()},timeout = 2)
#                     proxy.append(ip_temp)
#                 except Exception as e:
#                     print(str(e))
#         except Exception as e:
#             continue
#     return proxy
#
#
# print(getProxyIp())
# print(len(getProxyIp()))

# #每次都怕取新的代理
# def getProxyIp():
#     header = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
#     }
#     proxy = []
#     try:
#         url1 = 'http://www.xicidaili.com/wn/1'
#         url2 = 'https://www.ipip.net/'
#         resq = requests.get(url1, headers=header)
#         res = resq.text
#         soup = BeautifulSoup(res, 'lxml')
#         ips = soup.findAll('tr')
#         for x in range(1, 20):
#             ip = ips[x]
#             tds = ip.findAll("td")
#             ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
#             try:
#                 requests.get(url2, proxies={'http':'http://'+ip_temp.strip()},timeout = 2)
#                 proxy.append(ip_temp)
#             except Exception as e:
#                 print(str(e))
#     except Exception as e:
#         print(str(e))
#     return proxy
#
#
# proxy_list = ['46.38.35.62:33368', '5.129.16.27:34853', '185.29.144.226:8080', '219.254.34.231:3128',
#                   '2.139.180.172:43670', '47.105.129.162:80', '47.105.136.225:80', '47.105.80.238:80', '89.179.68.102:59039',
#                   '171.221.239.11:808', '138.197.147.99:8080', '84.52.100.107:60398', '89.184.13.184:38406', '119.179.148.125:8060',
#                   '119.28.230.147:8888', '47.105.84.52:80', '47.105.137.4:80'
#                   ]
#
#
# print(len(proxy_list))
# _new_ip = getProxyIp()
# print(_new_ip)
# for ip in _new_ip:
#     if ip not in proxy_list:
#         proxy_list.append(ip)
#         break
# print(len(proxy_list))