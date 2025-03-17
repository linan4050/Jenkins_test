#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2023/5/24 16:01
# Author     ：author lin3
"""
import json
import requests, hashlib, time
import leiting_encrypt as encrypt


# iOS 退款通知
def IosRefundNotify(gameOrderNo, leitingNo, amount, channelNo, userId, productId, tid, key, NotifyUrl, callback):
    params = {
        'status': 1,
        'gameOrderNo': gameOrderNo,
        'leitingNo': leitingNo,
        'amount': amount,
        'channelNo': channelNo,
        'userId': userId,
        'productId': productId,
        'tid': tid,
        'purchaseDate': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 60)),
        'refundDate': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
        'sign': hashlib.md5(f'1#{gameOrderNo}#{tid}#{key}'.encode()).hexdigest(),
    }
    res = requests.post(NotifyUrl, data=json.dumps(params))
    if res.status_code != 200:
        callback(f'退款通知请求失败, Http Code={res.status_code}')
        return res.status_code, res.text, params

    res_text = json.loads(res.text)
    if not res_text.get('status', None):
        callback(f'退款通知接口响应数据异常, 响应数据为: {res_text}')

    return res.status_code, res_text, params


# 充值发货通知
def RechargeNotify(gameOrderNo, thirdAmount, thirdNo, channelNo, userId, productId, extInfo, key, NotifyUrl, callback):
    params = {
            "currency": 'coin',
            "gameCoin": '0',
            "gameOrderNo": gameOrderNo,
            "message": 'success',
            "productId": '',
            "sign": hashlib.md5('#'.join(["success", gameOrderNo, thirdNo, channelNo, 'coin', thirdAmount, productId, userId,
                                 key]).encode()).hexdigest().lower(),
            "status": 'success',
            "thirdAmount": thirdAmount,
            "thirdNo": thirdNo,
            "channelNo": channelNo,
            "userId": userId,
        }
    if extInfo:
        params.update({'extInfo': extInfo})
    res = requests.post(str(NotifyUrl), data={"params": json.dumps(params)})
    if res.status_code != 200:
        callback(f'充值发货请求失败, Http Code={res.status_code}')
        return res.status_code, res.text, params

    if res.text != 'success':
        callback(f'充值发货通知失败, 服务器返回: {res.text}')
    return res.status_code, res.text, params


# sdk 登录
def sdkLogin(kwargs, url, callback):
    sdk_params = {
        "versionName": "1.0",
        "face": "1",
        "versionCode": 1,
        "accompany": "1",
        "checkAuth": "1",
        "serial": "08:00:27:e1:37:b5|530000000053206|ZX1G42CPJD|32257f602b9a5a7b",
        "media": "",
        "mmid": "",
        "os": '1'
    }
    sdk_params.update(kwargs)
    data = encrypt.leitingsdk_aec.encode(json.dumps(sdk_params))
    res = requests.post(url=url, data=data)
    if res.status_code != 200:
        callback(f'SDK登陆请求异常, Http Code={res.status_code}')
        return res.status_code, res.text, sdk_params
    print(res.text)
    res_text = json.loads(res.text)
    if not res_text.get('data', None):
        callback(f'SDK登陆响应数据异常, 响应数据为: {res_text}')
        return res.status_code, res_text, sdk_params

    res_text['data'] = json.loads(encrypt.leitingsdk_aec.decode(res_text['data']))
    return res.status_code, res_text, sdk_params


NotifyUrl = 'http://aobdgameandtf.leiting.com:16061/ThunderPayCallback'
key = 'f2m3Ny4QoW2E7O8D'    # 游戏充值对应的key，需要找研发或者运维要
params = {
        "gameOrderNo": '4yn04m_byy_5_100002_lovz1of6',
        "productId": '',
        "thirdAmount": '600',
        "thirdNo": '2023110810291354418530113',
        "channelNo": '110001',
        "userId": '44lqazmm',
        "key": key,
        "NotifyUrl": NotifyUrl
    }

# 海外充值发货通知
def OverseasRechargeNotify(key, NotifyUrl, callback, params):
    params.update({
        "sign": hashlib.md5('#'.join(["success", params.get('gameOrderNo'), params.get('thirdNo'), key]).encode()).hexdigest().lower()})
    # print(params)
    res = requests.post(str(NotifyUrl), data={"params": json.dumps(params)})
    if res.status_code != 200:
        callback(f'充值发货请求失败, Http Code={res.status_code}')
        return res.status_code, res.text, params

    if res.text != 'success':
        callback(f'充值发货通知失败, 服务器返回: {res.text}')
    return res.status_code, res.text, params

