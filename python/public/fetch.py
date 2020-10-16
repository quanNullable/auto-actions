# -*- coding: utf-8 -*-
# 简单的网络请求框架

import requests
import json as jsonLib

def post(url, data=None, json=None,text=False, **kwargs):
    if not json is None:
       data = jsonLib.dumps(json,ensure_ascii=False)
    response = requests.post(url, data, **kwargs)
    result = response.text if text else response.json()
    # print('post:',url,data if json is None else json,result)
    return result

def get(url, params=None,text=False, **kwargs):
    response = requests.get(url, params, **kwargs)  
    result = response.text if text else response.json()
    # print('get:',url,result)
    return result

def download(url):
    response = requests.get(url, stream=True)  
    return response
