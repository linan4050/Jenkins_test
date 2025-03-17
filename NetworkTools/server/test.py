#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2024/7/23 10:25
# Author     ：author lin3
"""
import hashlib
import re
import time

import requests
import json

# data = {"ip":["www.baidu.com", "www.blog.csdn.net"]}
# a = requests.post(url='http://10.5.2.70:8000/ClearAllRules', data=json.dumps(data))
# print(a.content)

# data = {"outgoing_data": 256, "incoming_data": 1, "sign": "123141", "NetworkType": "rate",
#         "ip": ['zzzzzzz', 'asfasfasfa']}
# data = {"ip": "www.baidu.com\nwww.blog.csdn.net"}
# a = requests.post(url='http://10.5.2.70:8000/NetWorkTest', data=json.dumps(data), headers={'Content-Type': 'application/json'})
# print(a.json())

a = {
    'NetworkType': {
        'rate': {'outgoing_data': 32000000, 'incoming_data': 32000000},    # kbps
        'delay': {'outgoing_data': 2, 'incoming_data': 2},   # ms
        'loss': {'outgoing_data': 10, 'incoming_data': 10},      # %
        'delay_percent': {'outgoing_data': 0, 'incoming_data': 0, 'outgoing_delay_percent': 0, 'incoming_delay_percent': 0},
    },
    'ip': '183.2.172.42',
    # 'ip': '183.2.172.42',
    # 'port': 8080
}
sign = hashlib.md5('LT'.join(["NetWorkTest", a.get('ip'), 'CsztTest666']).encode()).hexdigest().lower()
a.update({'sign': sign})

res = requests.post(url='http://47.101.179.76:5000/NetWorkTest', data=json.dumps(a), headers={'Content-Type': 'application/json'})
print(res.content)
# res = requests.post(url='http://47.101.179.76:5000/NetWorkSet', data=json.dumps(a), headers={'Content-Type': 'application/json'})

# res = requests.post(url='http://47.101.179.76:5000/ClearAllRules', data=json.dumps(a), headers={'Content-Type': 'application/json'})
# res = requests.post(url='http://10.5.2.70:5000/NetWorkSet', data=json.dumps(a), headers={'Content-Type': 'application/json'})
# res = requests.post(url='http://10.5.2.70:5000/ClearAllRules', data=json.dumps(a), headers={'Content-Type': 'application/json'})
# res = requests.post(url='http://8.217.181.29:8089/NetWorkSet', data=json.dumps(a), headers={'Content-Type': 'application/json'})
# print(time.time()-t)
# print(res.content)
# tcset eth0 --change --direction outgoing --rate 2000kbps --direction outgoing --delay 2000ms
# sudo su -

# a = ['--loss', '--delay', '--rate', '--delay_percent']
# b = 'tcset eth0 --src-network 103.162.172.125 --port 8080 --direction incoming --change --rate'
# print(any(i in b for i in a))
# a = {'0.0.0.0': [1,2,3]}
# a.pop('0.0.0.0')
# print(a)

# [('/data/lin3/NetWorkTools/api_exception.py', '/data/lin3/NetWorkTools'), ('/data/lin3/NetWorkTools/ip_while.txt', '/data/lin3/NetWorkTools'), ('/data/lin3/NetWorkTools/log_system.py', '/data/lin3/NetWorkTools')]



# data = '1 packets transmitted, 1 received, 0% packet loss, time 0ms'
# math_loss_data = re.search(r'[0-9] packets.*ms', data).group()
# print(math_loss_data)
# 10
# datas = [('/root/NetWorkTool/api_exception.py', '/root/NetWorkTool'), ('/root/NetWorkTool/log_system.py', '/root/NetWorkTool')],

