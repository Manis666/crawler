#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2019-3-4 11:00
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : DianChou.py
# @Software: PyCharm
#爬取点筹网的项目信息并生成excel数据文档


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
    file = '1.xls'
    p1 = os.path.exists(file)
    if not p1:
        excelTabel = xlwt.Workbook()  # 创建excel对象
        excelTabel.add_sheet('项目', cell_overwrite_ok=True)
        excelTabel.add_sheet('基地', cell_overwrite_ok=True)
        excelTabel.save(file)
    wb = xlrd.open_workbook(filename=file)
    row = str(wb.sheets()[a].nrows)
    return row


#写excel
def wexcel(s,a):
    file = '1.xls'
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

#爬取所有的项目url并保存
def getURLlist():
    browser = webdriver.Chrome()
    url00 = 'https://www.idianchou.com/pc/project/index'
    browser.get(url00)
    time.sleep(5)
    scroll_add_crowd_button = browser.find_element_by_xpath('//*[@id="projectList"]/div[1]/div[12]')
    browser.execute_script("arguments[0].scrollIntoView();", scroll_add_crowd_button)
    time.sleep(1)

    url_list = []

    i = 1
    while i<244:
        try:
            print('将第' + str(i) + '页url加入列表。')
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            a_page_list = soup.select('#projectList > div.project > div > a')
            for a_tag in a_page_list:
                href = 'https://www.idianchou.com' + a_tag.get('href')
                url_list.append(href)
                print('已加入url列表：' + href)
            if i == 1:
                browser.find_element_by_xpath('//*[@id="pagination"]/div/a[11]').click()
            else:
                browser.find_element_by_xpath('//*[@id="pagination"]/div/a[13]').click()
            time.sleep(5)
            print('第' + str(i) + 'url加入列表完成。\n')
            i+=1

        except Exception as e:
            print(str(e))

    #记录所有的url
    file = open('urlList.txt', 'a', encoding='UTF-8')
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

                #项目名称
                project_name = soup.select('div.projectMainInfo > div > p')[0].find_all(text=True)[0]


                #按类别进行不同的解析
                if '基地' in project_name:
                    baseinfo(soup,project_name,url)
                else:projectinfo(soup,project_name,url)

                browser.close()

                print('url:' + url)
                print(project_name + '已解析保存！')
                url_list.remove(url_0)

            except Exception as e:
                print(str(e))
                print('url:' + url)

                #报错记录url
                file = open('FlaseUrl.txt', 'a', encoding='UTF-8')
                file.write(url)
                file.close()

                #报错记录日志
                file = open('log.txt', 'a', encoding='UTF-8')
                file.write(url + '\n' + str(e))
                file.close()

        if len(url_list) == 0:
            break


#项目类型型的项目解析
def projectinfo(soup,project_name,url):
    # 项目名称
    project_name = project_name

    # 已筹到
    yi_choudao = soup.select('p.hasFundRow > span > i')[0].find_all(text=True)[0] + \
                 soup.select('div > p.hasFundRow > span')[0].find_all(text=True)[1]

    # 开始时间
    start_time = soup.select('div > p.upTime > span')[0].find_all(text=True)[0]

    # 项目进度
    progress = soup.select('div > div.el-progress.el-progress--line > div.el-progress__text')[0].find_all(text=True)[
        0].replace('\n', '')

    # 后面的一系列数据
    distance = soup.select('div.projectData > div > span.data')

    # 目标金额
    target_amount = distance[0].find_all(text=True)[0].replace(' ', '').replace('\n', '')

    # 参考回报率
    return_rate = distance[1].find_all(text=True)[0]

    # 期限
    time_limit = distance[2].find_all(text=True)[0]

    # 成功/未成功    一份多少钱   #mainContent > div.projectMainInfo > div > div.buttonGroup > span.goFund.preheat
    try:
        state = soup.select('div > div.buttonGroup > span.goFund.preheat')[0].find_all(text=True)[0] + \
                soup.select('div > div.buttonGroup > span.goFund.preheat')[0].find_all(text=True)[1]
    except:
        try:
            state = soup.select('div > div.buttonGroup > span.goFund.usable')[0].find_all(text=True)[0] + \
                    soup.select('div > div.buttonGroup > span.goFund.usable')[0].find_all(text=True)[1]
        except:
            state = soup.select('div > div.buttonGroup > span.goFund.finished')[0].find_all(text=True)[0] + \
                    soup.select('div > div.buttonGroup > span.goFund.finished')[0].find_all(text=True)[1]


    # 风控点评
    risk_review_text = soup.select('#infoContainer2')[0].find_all(text=True)
    risk_review = risk_review_text[0] + '\n' + \
                  risk_review_text[1].replace('\n', '').replace(' ', '') + '\n' + \
                  ''.join(risk_review_text[2:]).replace(' ', '')

    return_way = ''.join(soup.select('div.fundInfo > div.returnType > div.contentBox')[0].find_all(text=True))
    raise_process = ''.join(soup.select('div.identificationProcess > div.contentBox > div')[0]
                            .find_all(text=True)).replace('    ','-->\n').replace('  ', '')

    # 认筹记录
    record_list = soup.select('#infoContainer3')[0].find_all(text=True)[8:]
    a = 1
    b = len(record_list) / 8
    while a < b:
        record_list[a * 8 - 1] = record_list[a * 8 - 1] + '\n'
        a += 1
    record = ''.join(record_list)

    project_details = ''
    img_url = ''
    img_list_src = soup.select('#infoContainer1 > p > img')
    i = 0
    for img_src in img_list_src:
        src = img_src.get('src')
        print(src)
        imgfile = '1/项目/' + getNewrow(0) + project_name + '/'
        if (os.path.isdir(imgfile) == False):
            os.makedirs(imgfile);
        urlretrieve(src, imgfile + str(i) + '.png')
        time.sleep(5)
        pytesseract.pytesseract.tesseract_cmd = 'E:/Tesseract-OCR/tesseract.exe'
        text = pytesseract.image_to_string(Image.open(imgfile + str(i) + '.png'), lang='chi_sim')
        project_details += text.replace('\n', '') + '\n'
        img_url += src + '\n'
        i += 1

    #数据写入到excel
    data = [project_name,yi_choudao,start_time,progress,target_amount,
            return_rate,time_limit,state,risk_review,return_way,
            raise_process,record,project_details,img_url,url]

    # 将爬取的数据写入到excel
    wexcel(data,0)

#获取基地类型的项目信息
def baseinfo(soup,project_name,url):
    # 项目名称
    project_name = project_name

    # 土地面积
    land_area = ''.join(soup.select('div.projectMainInfo > div > p.landArea')[0].find_all(text=True))

    # 项目进度
    progress = soup.select('div > div.el-progress.el-progress--line > div.el-progress__text')[0].find_all(text=True)[
        0].replace('\n', '')

    # 剩余份数
    remaining_copies = soup.select('#remainingNum')[0].find_all(text=True)[0].replace('\n', '').replace(' ', '')

    # 期限
    time_limit = soup.select('#landTime')[0].find_all(text=True)[0]

    # 到期每份获得
    each_harvest = soup.select('div.projectData.projectDataB > div > span.data')[2].find_all(text=True)[0].replace('\n',
                                                                                                                   '').replace(
        ' ', '')
    # 上线时间
    real_time = soup.select('div.projectData.projectDataB > div > span.realTime')[0].find_all(text=True)[0]

    # 成功/未成功    一份多少钱     #mainContent > div.projectMainInfo > div > div.buttonGroup > span.goFund.usable
    try:
        state = soup.select('div > div.buttonGroup > span.goFund.preheat')[0].find_all(text=True)[0] + \
                soup.select('div > div.buttonGroup > span.goFund.preheat')[0].find_all(text=True)[1]
    except:
        try:
            state = soup.select('div > div.buttonGroup > span.goFund.usable')[0].find_all(text=True)[0] + \
                    soup.select('div > div.buttonGroup > span.goFund.usable')[0].find_all(text=True)[1]
        except:
            state = soup.select('div > div.buttonGroup > span.goFund.finished')[0].find_all(text=True)[0] + \
                    soup.select('div > div.buttonGroup > span.goFund.finished')[0].find_all(text=True)[1]

    # 流转流程
    circulation_process = ''.join(
        soup.select('div.identificationProcess > div.contentBox > div.process')[0].find_all(text=True)).replace('    ', '-->\n').replace(' ','')

    # 认筹记录
    record_list = soup.select('#infoContainer4')[0].find_all(text=True)[10:]
    a = 1
    b = len(record_list) / 8
    while a < b:
        record_list[a * 8 - 1] = record_list[a * 8 - 1] + '\n'
        a += 1
    record = ''.join(record_list)

    # 基地详情
    base_details = ''
    base_img_url = ''
    # 产品详情
    product_details = ''
    product_img_url = ''
    # 流转规则
    rules_details = ''
    rules_img_url = ''

    select_list = ['#infoContainer1 > p > img', '#infoContainer2 > p > img', '#infoContainer3 > p > img']

    project_details = ''
    img_url = ''

    j = 0
    for item in select_list:
        j += 1
        img_list_src = soup.select(item)
        i = 0
        for img_src in img_list_src:
            src = img_src.get('src')
            if j == 1:
                last_name = '/基地详情/'
            elif j == 2:
                last_name = '/产品详情/'
            elif j == 3:
                last_name = '/流转规则/'
            imgfile = '1/基地/' + getNewrow(1) + project_name + last_name
            if (os.path.isdir(imgfile) == False):
                os.makedirs(imgfile);
            urlretrieve(src, imgfile + str(i) + '.png')
            time.sleep(5)
            pytesseract.pytesseract.tesseract_cmd = 'E:/Tesseract-OCR/tesseract.exe'
            text = pytesseract.image_to_string(Image.open(imgfile + str(i) + '.png'), lang='chi_sim')
            project_details += text.replace('\n', '') + '\n'
            img_url += src + '\n'
            i += 1
            if j == 1:
                base_details += text.replace('\n', '') + '\n'
                base_img_url += src + '\n'
            elif j == 2:
                product_details += text.replace('\n', '') + '\n'
                product_img_url += src + '\n'
            elif j == 3:
                rules_details += text.replace('\n', '') + '\n'
                rules_img_url += src + '\n'

    data = [project_name,land_area,progress,remaining_copies,time_limit,each_harvest,real_time,
            state,circulation_process,record,base_details,base_img_url,product_details,
            product_img_url,rules_details,rules_img_url,url]

    #将爬取的数据写入到excel
    wexcel(data,1)

if __name__ == '__main__':
    url_list = getURLlist()
    getInfo(url_list)


