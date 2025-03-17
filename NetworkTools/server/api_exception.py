#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2024/7/27 17:49
# Author     ：author lin3
"""
from flask import json, request
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 1

    def __init__(self, msg=None, code=None, error_code=None,
                 headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        # 调用一下父类的初始化函数
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope={}):
        body = dict(
            status=self.error_code,
            msg=self.msg
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None, scope={}):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]


# IP异常
class IPError(APIException):
    code = 200
    msg = 'IP is Empty'
    error_code = 1


# 网络设置类型异常
class NetworkTypeError(APIException):
    code = 200
    msg = 'NetworkType error'
    error_code = 2


# 验签失败
class SignCheckError(APIException):
    code = 200
    msg = 'sign check fail'
    error_code = 3


# # 参数校验失败
# class ParamsCheckError(APIException):
#     code = 200
#     msg = ''
#     error_code = 4


# shell 执行异常
class CalledProcessError(APIException):
    code = 200
    msg = 'command error'
    error_code = 5


# 网络概率延迟参数设置错误
class DelayPercentError(APIException):
    code = 200
    msg = 'delay percent error'
    error_code = 6


# 参数数据类型错误
class ParamsTypeError(APIException):
    code = 200
    msg = 'params type error'
    error_code = 7