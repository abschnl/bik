# !/usr/bin/env python3
# coding: utf-8

import urllib.request
import json
import urllib.parse
import time
import os
import threading

#登陆后的token
TOKEN = ""
#线程池
imgsThreads = []

def dowloadImg(imgUrl, imgName, title):

    url = 'https://storage1.picacomic.com/static/'+imgUrl

    try:
        response = urllib.request.urlopen(url)
    except Exception as e:
        print("timeOut : "+url)

    data = response.read()

    if os.path.exists("./img/"+title+"/"):
        pass
    else:
        os.mkdir("./img/"+title+"/")

    with open("./img/"+title+"/"+imgName, "wb") as code:
        code.write(data)

def login():
    url = 'https://picaapi.picacomic.com/auth/sign-in'

    values = {
        'email': '',
        'password': ''
    }

    user_agent = 'sora/2.2 (com.picacomic.sora; build:2.2; iOS 10.0.1) Alamofire/4.0.1'

    headers = {
        'User-Agent': user_agent,
        'Host': 'picaapi.picacomic.com',
        'Accept': 'application/vnd.picacomic.com.v1+json',
        'app-version': '2.0.1.3',
        'api-key': '2587EFC6F859B4E3A1D8B6D33B272',
        'app-platform': 'ios',
        #    'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
        #    'Accept-Language': 'zh-Hans-CN;q=1.0',
        'app-uuid': '8E4C6215-FF1E-4661-986C-226B841B8138',
        'Connection': 'keep-alive'
    }

    url_values = urllib.parse.urlencode(values)

    url_values = url_values.encode(encoding='UTF8')

    full_url = urllib.request.Request(url, url_values, headers)

    response = urllib.request.urlopen(full_url)

    the_page = response.read().decode("utf-8")

    jsonStr = json.loads(the_page)

    global TOKEN

    TOKEN = jsonStr["data"]["token"]

    getList()


def getList():

    global TOKEN

    url = 'http://picaapi.picacomic.com/comics'

    user_agent = 'sora/2.2 (com.picacomic.sora; build:2.2; iOS 10.0.1) Alamofire/4.0.1'

    headers = {
        'User-Agent': user_agent,
        'Host': 'picaapi.picacomic.com',
        'Accept': 'application/vnd.picacomic.com.v1+json',
        'Authorization': TOKEN,
        'app-version': '2.0.1.3',
        'api-key': '2587EFC6F859B4E3A1D8B6D33B272',
        'app-platform': 'ios',
        #    'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
        #    'Accept-Language': 'zh-Hans-CN;q=1.0',
        'app-uuid': '8E4C6215-FF1E-4661-986C-226B841B8138',
        'Connection': 'keep-alive'
    }

    page = 1
    pageTotal = 10

    while page < pageTotal:

        values = {
            'page': page,
            's': pageTotal
        }

        url_values = urllib.parse.urlencode(values)

        url_values = url_values.encode(encoding='UTF8')

        full_url = urllib.request.Request(url, url_values,  headers)

        response = urllib.request.urlopen(full_url)

        the_page = response.read().decode("utf-8")

        jsonStr = json.loads(the_page)

        for e in (jsonStr["data"]["comics"]["docs"]):
            print(e["_id"])
            getCover(e["_id"])

        pageTotal = jsonStr["data"]["comics"]["pages"]
        print("getList pageTotal : "+str(pageTotal))
        page = page + 1
        print(" getList page : "+ str(page))


def getCover(id):
    id = id
    global TOKEN

    url = 'https://picaapi.picacomic.com/comics/'+id

    user_agent = 'sora/2.2 (com.picacomic.sora; build:2.2; iOS 10.0.1) Alamofire/4.0.1'

    headers = {
        'User-Agent': user_agent,
        'Host': 'picaapi.picacomic.com',
        'Accept': 'application/vnd.picacomic.com.v1+json',
        'Authorization':TOKEN,
        'app-version': '2.0.1.3',
        'api-key': '2587EFC6F859B4E3A1D8B6D33B272',
        'app-platform': 'ios',
        #    'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
        #    'Accept-Language': 'zh-Hans-CN;q=1.0',
        'app-uuid': '8E4C6215-FF1E-4661-986C-226B841B8138',
        'Connection': 'keep-alive'
    }

    full_url = urllib.request.Request(url, headers = headers)

    response = urllib.request.urlopen(full_url)

    the_page = response.read().decode("utf-8")

    jsonStr = json.loads(the_page)

    title = jsonStr["data"]["comic"]["title"]

    print(title)

    getImgs(id, title)


def getImgs(id, title):
    id = id
    title = title
    page = 1
    pageTotal = 10

    while page < pageTotal:

        url = 'https://picaapi.picacomic.com/comics/'+id+'/order/1/pages?page='+str(page)

        user_agent = 'sora/2.2 (com.picacomic.sora; build:2.2; iOS 10.0.1) Alamofire/4.0.1'

        headers = {
            'User-Agent': user_agent,
            'Host': 'picaapi.picacomic.com',
            'Accept': 'application/vnd.picacomic.com.v1+json',
            'Authorization':TOKEN,
            'app-version': '2.0.1.3',
            'api-key': '2587EFC6F859B4E3A1D8B6D33B272',
            'app-platform': 'ios',
            #    'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
            #    'Accept-Language': 'zh-Hans-CN;q=1.0',
            'app-uuid': '8E4C6215-FF1E-4661-986C-226B841B8138',
            'Connection': 'keep-alive'
        }

        full_url = urllib.request.Request(url, headers=headers)

        response = urllib.request.urlopen(full_url)

        the_page = response.read().decode("utf-8")

        jsonStr = json.loads(the_page)

        def doDowload(e):
            print("getImgs media originalName : " + e["media"]["originalName"])
            dowloadImg(e["media"]["path"], e["media"]["originalName"], title)

        for e in (jsonStr["data"]["pages"]["docs"]):
            th = threading.Thread(target=doDowload, args=(e,))
            th.start();
            imgsThreads.append(th)
            print(" imgsThreads count :" + str(len(imgsThreads)))

        for t in imgsThreads:
            t.join()

        time.sleep(10)

        imgsThreads.clear();

        pageTotal = jsonStr["data"]["pages"]["pages"]
        page = page + 1

login()




