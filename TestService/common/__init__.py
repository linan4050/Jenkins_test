#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2024/9/25 14:01
# Author     ：author lin3
"""

from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from device_manager import Device_Manager
import json
import os
import time
import subprocess

init_task_id = int(time.time())
parent_directory_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
ip_while_txt_path = os.path.join(parent_directory_path, 'ip_while.txt')     # ip 白名单文件路径
download_gen_path = os.path.join(parent_directory_path, 'apk')     # apk 下载后保存的根目录
download_queue = Queue(maxsize=20)       # 任务下载队列

with open(os.path.join(parent_directory_path, "setting.json"), 'r') as f:
    setting = json.loads(f.read())

ThreadPool = ThreadPoolExecutor(max_workers=setting['ThreadSetting']['max_workers'])


# 定时任务, 5秒获取一次队列中是否有下载任务
def scheduled_tasks():
    while True:
        if not download_queue.empty():
            ThreadPool.submit(Device_Manager(download_queue, download_gen_path, **setting).download_apk)
        time.sleep(5)