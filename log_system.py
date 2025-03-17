#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2023/11/10 17:55
# Author     ：author lin3
"""
import os
import logging
import re
import sys
from logging.handlers import TimedRotatingFileHandler


if sys.platform == 'win32':
    path = os.path.join(os.path.dirname(__file__), "log")
else:
    path = "log"


def setup_log(log_name):
    # 创建logger对象。传入logger名字
    logger = logging.getLogger(log_name)
    if not os.path.exists(path):
        os.mkdir(path)

    # 设置日志记录等级
    logger.setLevel(logging.INFO)
    # logging.basicConfig(filename=)

    # interval 滚动周期，
    # when="MIDNIGHT", interval=1 表示每天0点为更新点，每天生成一个文件
    # backupCount  表示日志保存个数
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(path, 'TestService.log'), when="MIDNIGHT", interval=1, backupCount=15, encoding='utf-8'
    )
    # filename="mylog" suffix设置，会生成文件名为mylog.2020-02-25.log
    file_handler.suffix = "%Y-%m-%d.log"

    # extMatch是编译好正则表达式，用于匹配日志文件名后缀
    # 需要注意的是suffix和extMatch一定要匹配的上，如果不匹配，过期日志不会被删除。
    file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    # 定义日志输出格式
    file_handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] [%(process)d] [%(levelname)s] - %(module)s.%(funcName)s (%(filename)s:%(lineno)d) - %(message)s"
        )
    )
    logger.addHandler(file_handler)
    return logger

logger = setup_log('TestService')
