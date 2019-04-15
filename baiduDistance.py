#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2019-2-2 9:56
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : baiduDistance.py
# @Software: PyCharm
#加载百度的一个excel文档的程序并通过selenium实现屏幕滑动加载信息，
# 数据只显示当前页和缓存前后一页，共20+页，通过每次屏幕滚动到每一页保存那三页的数据，解析后去重
#通过selenium仿人操作，获取动态数据


from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time



browser = webdriver.Chrome()
url = 'https://wenku.baidu.com/view/f15a777a27284b73f242507f.html'
browser.get(url)
time.sleep(5)
js="window.scrollTo(0,document.body.scrollHeight)"
browser.execute_script(js)
time.sleep(1)
scroll_add_crowd_button = browser.find_element_by_css_selector('#html-reader-go-more > div.banner-core-wrap.super-vip > div.doc-banner-text')
browser.execute_script("arguments[0].scrollIntoView();", scroll_add_crowd_button)
time.sleep(1)
try:
    browser.find_element_by_css_selector('div.continue-to-read > div.banner-more-btn > span').click()
    time.sleep(5)
    browser.execute_script("window.scrollBy(0, 1050)")
    time.sleep(3)

except Exception as e:
    print(str(e))

html = ''

a = 0
js="window.scrollTo(0,document.body.scrollHeight)"
while True:
    a += 1
    html = html + browser.page_source
    browser.execute_script("window.scrollBy(0, 1050)")
    time.sleep(1)
    if a >= 25:
        break




soup = BeautifulSoup(html, 'html.parser')
data_list = soup.select('div.reader-txt-layer > div.ie-fix > p')
#       //*[@id="pageNo-4"]/div/div/div/div[2]/div/p[1]                 #reader-container-inner-1 > div.mod.reader-page.complex.hidden-doc-banner.reader-page-4
#                         #pageNo-4 > div > div > div > div.reader-txt-layer > div > p
#                         #pageNo-3 > div > div > div > div.reader-txt-layer > div > p
print(data_list)
a = 0
b = 0
c = 0
data_all = []
data_line = []

for i in data_list:
    a = a+1
    data = i.find_all(text=True)[0]
    data_line.append(data)
    rese_number = re.compile('\d+')
    if rese_number.search(data):
        b += 1
        s = ','.join(data_line).replace('\n','')
        data_all.append(s)
        data_line = []
        print(s + "_____" + str(b))

    rese = re.compile('\n')
    if rese.search(data):
        c += 1
print(c)

c = 0
data_all = set(data_all)
print(len(data_all))
for i in data_all:
    rese = re.compile('\n')
    if rese.search(i):
        c += 1
print(c)

file = open('f:/baidu_hangju.csv', 'a', encoding='UTF-8')
file.write('\n'.join(data_all))
file.close()