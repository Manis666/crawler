#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2018-11-30 13:51
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : wordcloud1.py
# @Software: PyCharm
#生成词云


from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np

font = 'C:/Windows/Fonts/SIMLI.TTF'
file_path = 'F:/lagou.csv'
img_path = 'E:/progect/python'
file = open(file_path,'r',encoding='utf-8')

lines = file.readlines()
file.close()

list_words = []
i = 0
for line in lines:
    i += 1
    _s = line.split('|')[0]
    list_words.append(_s)
    print(i,_s)
string_words = ' '.join(list_words)
print(string_words)


img = Image.open(img_path + '/1.jpg')
img_array = np.array(img)#将图片装换为数组
stopword=['xa0']  #设置停止词，也就是你不想显示的词

wc = WordCloud(background_color='white',width=1000,height=800,mask=img_array,font_path=font,stopwords=stopword)
wc.generate_from_text(string_words)#绘制图片
plt.imshow(wc)
plt.axis('off')
plt.figure()
plt.show()  #显示图片
wc.to_file('f:/new1.png')  #保存图片