# !/usr/bin/env python3
# coding: utf-8

import urllib.request
import json
import urllib.parse
import time
import os
import threading
import redis

#Redis
r = redis.Redis(host='192.168.2.113', port=6379, db=0)

retry = 0
data = bytes()

def openUrl(url):
    try:
        response = urllib.request.urlopen(url,timeout=10)
        global data
        data = response.read()
    except Exception as e:
        global retry
        retry = retry + 1
        print(" retry :"+str(retry) +" url : "+ url)


def dowloadImg(imgUrl, imgName, title):

    url = 'https://storage1.picacomic.com/static/'+imgUrl

    global retry

    openUrl(url)

    if retry != 0 & retry < 4:
        openUrl(url)


    if os.path.exists("./cos/"+title+"/"):
        pass
    else:
        os.mkdir("./cos/"+title+"/")

    with open("./cos/"+title+"/"+imgName, "wb") as code:
        global data
        code.write(data)

    data = bytes()

    retry = 0

def getUrl():
    i = 1
    while True:
        key = str('DOWN-LOAD-COS-' + str(i))
        print("key = "+key)
        if r.exists(name=key) == 0:
            print("the key is not exists : "+key)
            break

        jsonStr = r.get(name=key).decode("utf-8")

        jsonObject = json.loads(jsonStr)

        print("jsonStr : "+str(jsonObject))
        for e in jsonObject:
            dowloadImg(e["imgUrl"], e["imgName"], e["title"])

        i =  i + 1

getUrl()