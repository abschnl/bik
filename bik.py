# !/usr/bin/env python3
# coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import urllib.request
import json
import urllib.parse
import http.cookiejar
import time
import os


def dowloadImg(imgUrl, imgName):

    url = 'https://storage1.picacomic.com/static/'+imgUrl

    try:
        response = urllib.request.urlopen(url,timeout=3)
    except Exception as e:
        print("timeOut : "+url)

    data = response.read()

    with open("./img/"+imgName, "wb") as code:
        code.write(data)

def getList():

    url = 'http://picaapi.picacomic.com/comics'

    values = {
        'page': '1',
        's': 'ua'
    }

    user_agent = 'sora/2.2 (com.picacomic.sora; build:2.2; iOS 10.0.1) Alamofire/4.0.1'

    headers = {
        'User-Agent': user_agent,
        'Host': 'picaapi.picacomic.com',
        'Accept': 'application/vnd.picacomic.com.v1+json',
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFic2NobmxAZ21haWwuY29tIiwicm9sZSI6Im1lbWJlciIsIm5hbWUiOiJhYnNjaG5sIiwidmVyc2lvbiI6IjIuMC4xLjMiLCJpYXQiOjE0ODcxNjQyNzIsImV4cCI6MTQ4Nzc2OTA3Mn0.2qPBopttGOdBdsSgdHYjh3Jpi4cQJ1nOvZFfukfw2BY',
        'app-version': '2.0.1.3',
        'api-key': '2587EFC6F859B4E3A1D8B6D33B272',
        'app-platform': 'ios',
        #    'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
        #    'Accept-Language': 'zh-Hans-CN;q=1.0',
        'app-uuid': '8E4C6215-FF1E-4661-986C-226B841B8138',
        'Connection': 'keep-alive',
        'Cookie': '__cfduid=ddcc480f60c67d57be2b9b9ddad3ee5a01487654209'
    }

    url_values = urllib.parse.urlencode(values)

    url_values = url_values.encode(encoding='UTF8')

    full_url = urllib.request.Request(url, url_values,  headers)

    response = urllib.request.urlopen(full_url)

    the_page = response.read()

    print(the_page.decode("UTF8"))

def getCover():

    url = 'https://picaapi.picacomic.com/comics/58ac020c53ab5d740afce911'

    user_agent = 'sora/2.2 (com.picacomic.sora; build:2.2; iOS 10.0.1) Alamofire/4.0.1'

    headers = {
        'User-Agent': user_agent,
        'Host': 'picaapi.picacomic.com',
        'Accept': 'application/vnd.picacomic.com.v1+json',
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFic2NobmxAZ21haWwuY29tIiwicm9sZSI6Im1lbWJlciIsIm5hbWUiOiJhYnNjaG5sIiwidmVyc2lvbiI6IjIuMC4xLjMiLCJpYXQiOjE0ODcxNjQyNzIsImV4cCI6MTQ4Nzc2OTA3Mn0.2qPBopttGOdBdsSgdHYjh3Jpi4cQJ1nOvZFfukfw2BY',
        'app-version': '2.0.1.3',
        'api-key': '2587EFC6F859B4E3A1D8B6D33B272',
        'app-platform': 'ios',
        #    'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
        #    'Accept-Language': 'zh-Hans-CN;q=1.0',
        'app-uuid': '8E4C6215-FF1E-4661-986C-226B841B8138',
        'Connection': 'keep-alive',
        'Cookie': '__cfduid=ddcc480f60c67d57be2b9b9ddad3ee5a01487654209'
    }

    full_url = urllib.request.Request(url, headers = headers)

    response = urllib.request.urlopen(full_url)

    the_page = response.read()

    print(the_page.decode("UTF8"))

def getImgs():

    url = 'https://picaapi.picacomic.com/comics/58ac020c53ab5d740afce911/order/1/pages?page=1'

    user_agent = 'sora/2.2 (com.picacomic.sora; build:2.2; iOS 10.0.1) Alamofire/4.0.1'

    headers = {
        'User-Agent': user_agent,
        'Host': 'picaapi.picacomic.com',
        'Accept': 'application/vnd.picacomic.com.v1+json',
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFic2NobmxAZ21haWwuY29tIiwicm9sZSI6Im1lbWJlciIsIm5hbWUiOiJhYnNjaG5sIiwidmVyc2lvbiI6IjIuMC4xLjMiLCJpYXQiOjE0ODcxNjQyNzIsImV4cCI6MTQ4Nzc2OTA3Mn0.2qPBopttGOdBdsSgdHYjh3Jpi4cQJ1nOvZFfukfw2BY',
        'app-version': '2.0.1.3',
        'api-key': '2587EFC6F859B4E3A1D8B6D33B272',
        'app-platform': 'ios',
        #    'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
        #    'Accept-Language': 'zh-Hans-CN;q=1.0',
        'app-uuid': '8E4C6215-FF1E-4661-986C-226B841B8138',
        'Connection': 'keep-alive',
        'Cookie': '__cfduid=ddcc480f60c67d57be2b9b9ddad3ee5a01487654209'
    }

    full_url = urllib.request.Request(url, headers=headers)

    response = urllib.request.urlopen(full_url)

    the_page = response.read().decode("utf-8")

    jsonStr = json.loads(the_page)

    for e in (jsonStr["data"]["pages"]["docs"]):
        print(e["media"]["originalName"])
        dowloadImg(e["media"]["path"], e["media"]["originalName"])

getImgs()

