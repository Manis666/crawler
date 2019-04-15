#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Company : YUNANKAIYA
# @Time    : 2018-12-3 16:38
# @Author  : Yixuefei
# @Email   : i have'nt Email
# @File    : qqnumber.py
# @Software: PyCharm
#自己玩

key = {
            "oe": "0", "n": "0", "z": "0", "on": "0",
            "oK": "1", "6": "1", "5": "1",
            "ow": "2", "-": "2", "A": "2", "oc": "2",
            "oi": "3", "i": "3", "o": "3", "oz": "3",
            "7e": "4", "v": "4", "P": "4", "7n": "4",
            "7K": "5", "4": "5", "k": "5", "7": "5", "7v": "5",
            "7w": "6", "C": "6", "s": "6", "7c": "6",
            "7i": "7", "S": "7", "l": "7", "7z": "7",
            "Ne": "8", "c": "8", "F": "8", "Nn": "8", "ov": "8",
            "NK": "9", "E": "9", "q": "9", "Nv": "9"
        }

qq1 = '2473044856'   #14411521 2350760284
qq2 = '2460030109'   #14411521 2335876778          24883506
qq3 = '937438867'    #14411521 2350696556         1413257689
qq4 = '401015942'    #14411521 0937291016          536275074
qq6 = '577094472'    #14411521 1950199119
qq5 = '1760194207'   #

_s1 = '*S1*oKvPoK6kow6Aoi4z7iCzowcP'
_s2 = '*S1*oKvPoK6kow6AoiokNeSs7iSF'
_s3 = '*S1*oKvPoK6kow6Aoi4z7wEs7K4s'
_s4 = '*S1*oKvPoK6kow6zNKolowE5oe6s'
_s6 = '*S1*oKvPoK6kow65NK4zoKEqoK6q'
_s5 = '*S1*oKnkoKCl7Knion'


# *S1*oKvs7eEkownqon   1464952090
#  *S1*ow4iNKoqoKcq7n  2539391894
# *S1*oKnkoKCl7Knion   1051675030
# *S1*7eEl7eSFoenF      497478008
# *S1*oiSA7KcioKvl      372583147
# https://ti.qq.com/honest-say/my-received.html

qq = ''
string = '*S1*oKvPoK6kow65NK4zoKEqoK6q'
string = string.replace("*S1*", "")
debug=False
while string:
            if len(string) > 1:
                if string[0:2] not in key:
                    if debug:
                        print(string[0:1], key[string[0:1]])
                    qq += key[string[0:1]]
                    string = string[1:]
                else:
                    if debug:
                        print(string[0:2], key[string[0:2]])
                    qq += key[string[0:2]]
                    string = string[2:]
            else:
                if debug:
                    print(string, key[string])
                qq += key[string]
                string = ""
print(qq)