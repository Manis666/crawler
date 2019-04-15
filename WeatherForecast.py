#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2018-12-28 15:13
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : WeatherForecast.py
# @Software: PyCharm
# 通过api获取天气预报信息

import requests
import json
api1 = 'http://flash.weather.com.cn/wmaps/xml/china.xml'
api2 = 'http://flash.weather.com.cn/wmaps/xml/beijing.xml'


def weather_work(city):
    url = 'http://wthrcdn.etouch.cn/weather_mini?city={}'.format(city)
    f=requests.get(url)
    # print(f.text)
    jsons=json.loads(f.text)
    print(jsons)
    # print(jsons['data']['forecast'][0])
    i = jsons['data']['forecast'][0]
    print(i['date'])
    print(i['high'])
    print(i['low'])
    print('风力 '+i['fengli'].replace('<![CDATA[','').replace(']]>',''))
    print(i['type'])
    print(jsons['data']['ganmao'])

weather_work('昆明')