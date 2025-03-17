#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2024/9/4 21:35
# Author     ：author lin3
"""
import datetime
import os
import time
import requests
from airtest.core.android.adb import *
from pyaxmlparser import APK


class Device_Manager:
    def __init__(self, download_queue, download_gen_path, **kwargs):
        self.download_queue = download_queue
        self.download_gen_path = download_gen_path
        self.testcase_path = kwargs.get('game_testcase_path', None)
        self.feishu_robot_notify_url = kwargs.get('feishu_robot_notify_url', None)
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }
        self.notify_text = ''
        self.apk_name = None
        self.package_name = None
        self.dev_model = None
        self.install_use_time = None
        self.adb = ADB()

    @property
    def get_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_notify_text(self, text):
        self.notify_text += f'[{self.get_time}] {text}\n'

    def feishu_robot_notify(self, msg_type='text', content={}):
        headers = {
            "Content-Type": "application/json"
        }
        res = requests.post(url=self.feishu_robot_notify_url, headers=headers, json={'msg_type': msg_type, 'content': content})
        print(res.content)
        self.notify_text = ''

    def install_to_device(self, apk_path, serialno=None, notify_text=None):
        serialno_list = [i[0] for i in self.adb.devices()]
        # 如果没有指定某个设备, 就从当前设备里随机挑一个进行跑测
        self.adb.serialno = random.choice(serialno_list) if not serialno else serialno
        third_package = self.adb.start_shell('pm list package -3').stdout.read().decode()
        self.package_name = APK(apk_path).package

        if self.package_name in third_package:
            self.set_notify_text(f'{self.package_name} 已经安装，进行删除操作')
            self.adb.uninstall_app(self.package_name)
            self.set_notify_text(f'{self.package_name} 删除成功')
            time.sleep(1)

        start_time = time.time()
        try:
            self.set_notify_text(f'开始安装 {self.apk_name} ')
            self.adb.install_app(apk_path, replace=True, install_options=['-g'])
        except Exception as e:
            self.set_notify_text(f'{self.apk_name} 安装失败, 安装耗时: {int(time.time() - start_time)}s， 失败信息: {str(e)} ')
            return False
        self.set_notify_text(f'{self.apk_name} 安装成功, 安装耗时: {int(time.time() - start_time)}s')
        return True

    def download_apk(self):
        download_url, game, serialno, task_id = self.download_queue.get()  # 获取下载链接、游戏标识、设备号、任务id
        print(f'任务开始执行, taskid={task_id}, game={game}, serialno={serialno}')
        self.apk_name = download_url.split('/')[-1]  # 获取 apk 名
        download_game_path = os.path.join(self.download_gen_path, game)  # 拼接每个游戏 apk 存放的目录

        # 游戏 apk 存放的目录不存在则创建目录
        if not os.path.exists(download_game_path):
            os.makedirs(download_game_path)

        # 拼接下载后的 apk 的路径
        download_apk_path = os.path.join(download_game_path, self.apk_name)

        # 如果旧 apk 存在, 执行删除操作。主要针对 M值 包。
        self.notify_text = f'设备号: {serialno}\n'
        if os.path.exists(download_apk_path):
            self.set_notify_text(f'{self.apk_name} 已存在, 执行删除重新下载操作')
            os.remove(download_apk_path)
            time.sleep(1)

        start_time = time.time()
        self.set_notify_text(f'开始下载安装包, 下载链接: {download_url} 游戏标识: {game}')
        with requests.get(url=download_url, headers=self.headers, stream=True) as response:
            apk_size = response.headers.get('Content-Length', None)
            with open(download_apk_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        self.set_notify_text(f'下载完成, 总耗时: {int(time.time() - start_time)}s')
        download_apk_size = os.path.getsize(download_apk_path)
        if not os.path.exists(download_apk_path) and download_apk_size != int(apk_size):
            self.set_notify_text(f'下载失败, 包体大小异常, 预计大小={int(apk_size)}, 实际下载大小={download_apk_size}')
            self.feishu_robot_notify(content={'text': self.notify_text})
            return

        install_res = self.install_to_device(download_apk_path, serialno)
        if not install_res:
            self.feishu_robot_notify(content={'text': self.notify_text})
            return

        self.set_notify_text(f'开始执行测试, 任务id: {task_id}')
        self.feishu_robot_notify(content={'text': self.notify_text})
        subprocess.run(f'python {self.testcase_path} {self.adb.serialno} {game} {self.package_name} {task_id}')
        return