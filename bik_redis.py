# !/usr/bin/env python3
# coding: utf-8

import urllib.request
import json
import urllib.parse
import time
import os
import threading
import redis

#登陆后的token
TOKEN = ""
#Redis
r = redis.Redis(host='192.168.2.113', port=6379, db=0)

i = 1

# 登陆方法
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


#获取列表
def getList():

    global TOKEN

    user_agent = 'sora/2.2 (com.picacomic.sora; build:2.2; iOS 10.0.1) Alamofire/4.0.1'

    headers = {
        'User-Agent': user_agent,
        'Host': 'picaapi.picacomic.com',
        'Accept': 'application/vnd.picacomic.com.v1+json',
        'Authorization': TOKEN,
        'app-version': '2.0.1.3',
        'api-key': '2587EFC6F859B4E3A1D8B6D33B272',
        'app-platform': 'ios',
        'app-uuid': '8E4C6215-FF1E-4661-986C-226B841B8138',
        'Connection': 'keep-alive'
    }

    page = 1

    while True:

        # cosplay列表
        cosUrl = "https://picaapi.picacomic.com/comics?"
        cosUrl = cosUrl + "page=" + str(page) + "&c=Cosplay&s=ua"

        print("cosUrl : " + cosUrl)

        # 最近更新列表
        # url = 'http://picaapi.picacomic.com/comics?'
        #
        # url = url + "page="+str(page)+"&s=ua"
        #
        # print("url : "+ url)

        full_url = urllib.request.Request(cosUrl, headers=headers)

        response = urllib.request.urlopen(full_url)

        the_page = response.read().decode("utf-8")

        jsonStr = json.loads(the_page)

        for e in (jsonStr["data"]["comics"]["docs"]):
            print(e["_id"])
            getCover(e["_id"])

        pageTotal = jsonStr["data"]["comics"]["pages"]
        print("getList pageTotal : "+str(pageTotal))
        page = page + 1
        print(" getList page : " + str(page))

        if page > pageTotal:
            print("page : "+page+" pageTotal : "+ pageTotal)
            break


def getCover(id):
    id = id
    global TOKEN

    url = "https://picaapi.picacomic.com/comics/"+id

    print(url)

    user_agent = 'sora/2.2 (com.picacomic.sora; build:2.2; iOS 10.0.1) Alamofire/4.0.1'

    headers = {
        'User-Agent': user_agent,
        'Host': 'picaapi.picacomic.com',
        'Accept': 'application/vnd.picacomic.com.v1+json',
        'Authorization':TOKEN,
        'app-version': '2.0.1.3',
        'api-key': '2587EFC6F859B4E3A1D8B6D33B272',
        'app-platform': 'ios',
        'app-uuid': '8E4C6215-FF1E-4661-986C-226B841B8138',
        'Connection': 'keep-alive'
    }

    full_url = urllib.request.Request(url, headers = headers)

    response = urllib.request.urlopen(full_url)

    the_page = response.read().decode("utf-8")

    jsonStr = json.loads(the_page)

    title = jsonStr["data"]["comic"]["title"]

    timeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    print("timeStr : "+timeStr+"  title : "+title)

    getImgs(id, title)


def getImgs(id, title):
    id = id
    title = title
    page = 1

    while True:

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
            'app-uuid': '8E4C6215-FF1E-4661-986C-226B841B8138',
            'Connection': 'keep-alive'
        }

        full_url = urllib.request.Request(url, headers=headers)

        try:
            response = urllib.request.urlopen(full_url,timeout=20)
        except Exception as e:
            print("full_url : "+url+" e: "+str(e))
            continue

        the_page = response.read().decode("utf-8")

        jsonStr = json.loads(the_page)

        for e in (jsonStr["data"]["pages"]["docs"]):

            data = [{"imgUrl": e["media"]["path"], "imgName": e["media"]["originalName"], "title": title}]
            dataJson = json.dumps(data)
            global i
            key = str('DOWN-LOAD-COS-' +str(i))

            # print("key : "+key+" value :"+dataJson)

            r.setex(name=key,value=dataJson,time=60*60*24*7)

            i = i + 1

        pageTotal = jsonStr["data"]["pages"]["pages"]

        print("imgPageTotal : "+ str(pageTotal))

        page = page + 1
        if page > pageTotal:
            print("getImgs page : "+str(page)+" pageTotal : "+ str(pageTotal))
            break

login()