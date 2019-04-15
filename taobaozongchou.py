#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2019-3-20 16:37
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : taobaozongchou.py
# @Software: PyCharm
#爬取淘宝网的众筹项目信息并生成excel数据文档

from selenium import webdriver
from bs4 import BeautifulSoup
import os
from urllib.request import urlretrieve
import time
import pytesseract
from PIL import Image
import xlwt
import xlrd
from xlutils.copy import copy

#获取excel的最新行
def getNewrow(a):
    file = '2taobaozongchong/1.xls'
    isExitPath('2taobaozongchong/')
    p1 = os.path.exists(file)
    if not p1:
        excelTabel = xlwt.Workbook()  # 创建excel对象
        excelTabel.add_sheet('项目', cell_overwrite_ok=True)
        excelTabel.add_sheet('基地', cell_overwrite_ok=True)
        excelTabel.save(file)
    wb = xlrd.open_workbook(filename=file)
    row = str(wb.sheets()[a].nrows)
    return row

#判断路径是否存在
def isExitPath(path):
    if (os.path.isdir(path) == False):
        os.makedirs(path);

#写excel
def wexcel(s,a):
    file = '2taobaozongchong/1.xls'
    wb = xlrd.open_workbook(filename=file)
    row = wb.sheets()[a].nrows
    excel = copy(wb)
    table = excel.get_sheet(a)
    for i in range(0, len(s)):
        table.write(row, i, s[i])
    excel.save(file)
    time.sleep(5)

def getSoup(url):
    browser = webdriver.Chrome()
    browser.get(url)
    html = browser.page_source
    time.sleep(5)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def getimgText(img_list_src,project_name):
    img_text = ''
    img_url = ''
    i = 0
    for img_src in img_list_src:
        src = img_src.get('src')
        if src.startswith('//'):
             src = 'https:' + src
        imgfile = '2taobaozongchong/项目/' + getNewrow(0) + project_name + '/'
        if (os.path.isdir(imgfile) == False):
            os.makedirs(imgfile);
        urlretrieve(src, imgfile + str(i) + '.png')
        time.sleep(5)
        #!!!!文字识别的修改这里的路径
        pytesseract.pytesseract.tesseract_cmd = 'E:/Tesseract-OCR/tesseract.exe'
        text = pytesseract.image_to_string(Image.open(imgfile + str(i) + '.png'), lang='chi_sim')
        img_text += text.replace('\n', '').replace(' ','') + '\n'
        img_url += src + '\n'
        i += 1
    return img_text,img_url

#爬取所有的项目url并保存
def getURLlist():
    browser = webdriver.Chrome()
    url00 = 'https://hi.taobao.com/market/hi/list.php?spm=a215p.1472830.1.3.298b69a27TuSJR#page=1&status=2&sort=&type=123330001'
    browser.get(url00)
    time.sleep(5)
    js = "window.scrollTo(0,document.body.scrollHeight)"
    browser.execute_script(js)
    time.sleep(1)

    url_list = []

    i = 1
    while i<120:
        try:
            print('将第' + str(i) + '页url加入列表。')
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            a_page_list = soup.select('#J_Projects > li > a')
            for a_tag in a_page_list:
                href = 'https:' + a_tag.get('href')
                url_list.append(href)
                print('已加入url列表：' + href)
            browser.find_element_by_class_name('next').click()
            time.sleep(5)
            print('第' + str(i) + 'url加入列表完成。\n')
            i+=1

        except Exception as e:
            print(str(e))

    #记录所有的url
    path = '2taobaozongchong/'
    isExitPath(path)
    file = open(path + 'urlList2.txt', 'a', encoding='UTF-8')
    file.write('\n'.join(url_list))
    file.close()

    browser.close()

    return url_list

def getInfo(list):
    url_list = list
    while True:
        for url_0 in url_list:
            url = url_0
            try:
                browser = webdriver.Chrome()
                browser.get(url)
                time.sleep(3)
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')

                projectinfo(soup,url)

                browser.close()

                print('url:' + url)
                print(url + '已解析保存！')
                url_list.remove(url_0)

            except Exception as e:
                print(str(e))
                print('url:' + url)
                url_list.remove(url_0)
                browser.close()

                #报错记录url
                file = open('2taobaozongchong/FlaseUrl.txt', 'a', encoding='UTF-8')
                file.write(url)
                file.close()

                #报错记录日志
                file = open('2taobaozongchong/log.txt', 'a', encoding='UTF-8')
                file.write(url + '\n' +'未解析成功\n'+ str(e))
                file.close()

        if len(url_list) == 0:
            break

#项目类型型的项目解析
def projectinfo(soup,url):
    # 项目名称
    print(url + '解析项目名称.....')
    project_name = soup.select('#J_Detail > div.project-title > h1')[0].find_all(text=True)[0]
    print(project_name)

    #收藏人数
    print(project_name + '解析收藏人数.....')
    collection_num = soup.select('#J_Detail > div.project-title > a > span.J_LikeNum')[0].find_all(text=True)[0]
    print(collection_num)

    # 已筹到
    print(project_name + '解析已筹到.....')
    yi_choudao = soup.select('div.money-box > p.current-money > span')[0].find_all(text=True)[0] + \
                 soup.select('div.box.schedule-box > div.money-box > p.current-money')[0].find_all(text=True)[1]
    print(yi_choudao)


    # 结束时间
    print(project_name + '结束时间.....')
    end_string = soup.select(' div.box.schedule-box > div.money-box > p.target-money')[0].find_all(text=True)[0]
    end_time = end_string.split('\xa0')[1]
    print(end_time)

    # 目标金额
    print(project_name + '解析目标金额.....')
    target_amount = ''.join(soup.select(' div.money-box > p.target-money > em')[0].find_all(text=True))
    print(target_amount)

    # 项目进度
    print(project_name + '解析项目进度.....')
    progress = soup.select('div > div.project-status-bar > span.percentage')[0].find_all(text=True)[0]
    print(progress)

    #支持人数
    print(project_name + '解析支持人数.....')
    support_people = soup.select('div > div.projects-schedule-data > span')[1].find_all(text=True)[0]

    #剩余时间
    print(project_name + '解析剩余时间.....')
    time_limit = soup.select('div > div.projects-schedule-data > span')[3].find_all(text=True)[0]
    print(time_limit)

    #项目状态############################################################################################
    print(project_name + '解析项目状态.....')
    progect_state = soup.select('div.box.schedule-box > div.reserve > span')[0].find_all(text=True)[0]
    print(progect_state)

    # 发起的企业!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    print(project_name + '解析发起的企业/企业地区.....')
    company_name = soup.select('div.sponsor > div.sponsor-info > span.sponsor-name')[0].find_all(text=True)[0]
    print(company_name)

    #项目介绍
    print(project_name + '解析项目介绍.....')
    project_introduce_0 = '\n'.join(soup.select('div.content > div > div')[0].find_all(text=True))+'\n'
    project_introduce_1 = '\n'.join(soup.select('#J_Desc')[0].find_all(text=True)).replace('\n\n','').replace(' ','') + '\n'
    img_list_src = soup.select('#J_Desc > h2 > img')
            # 项目介绍图片数
    count_img_src = len(img_list_src)
    print(count_img_src)
    img_text,img_url = getimgText(img_list_src,project_name)
    project_introduce = project_introduce_0 + project_introduce_1 + img_text
    print(project_introduce)

    #投资额分层
    print(project_name + '投资额分层.....')
    phase_a = soup.select('div.col-right > div.repays > div.repay-box > div.repay')[0]
    count_phase = len(soup.select('div.col-right > div.repays > div > div'))
        #最低投资额
    min_phase = ''.join(soup.select('div > div.repay-title > span')[0].find_all(text=True))               #最低投资额
        #最低投资信息
    min_phase_info = ''.join(phase_a.find_all(text=True)).replace('\n','').replace(' ','').replace(',,','')
    print(count_phase)
    print(min_phase)
    print(min_phase_info)

    #是否有video
    is_exit_video = '否'
    if len(soup.select('video'))>=1:
        is_exit_video = '有'
    print(is_exit_video)

    #项目动态
    print(project_name + '解析项目动态.....')
    progect_dynamic = '|.|'.join(soup.select('div.col-left.J_ProjectReport > div > ul')[0].find_all(text=True)).replace('\n','').replace('|.|','\n')
    print(progect_dynamic)

    #数据写入到excel
    print('正在写入数据到excel。。。')
    data = [project_name, collection_num,yi_choudao,end_time,target_amount,progress,support_people,time_limit,progect_state,
            company_name, project_introduce,img_url,count_img_src, count_phase, min_phase, min_phase_info, is_exit_video, progect_dynamic,url]

    # 将爬取的数据写入到excel
    wexcel(data,0)

if __name__ == '__main__':
    progect_url_list = ['https://izhongchou.taobao.com/dreamdetail.htm?id=18710']
    # progect_url_list = getURLlist()
    # file = open('2taobaozongchong/urlList2.txt')
    # progect_url_list = file.readlines()
    # print(progect_url_list)
    # file.close()
    getInfo(progect_url_list)

    # 最小的投资额，
    # 投资额分层
    # 有没有视频