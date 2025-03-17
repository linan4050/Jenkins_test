#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2024/7/18 17:19
# Author     ：author lin3
"""
import time

from flask import Flask, request, abort
from log_system import logger
from pre_request import pre, Rule, ParamsValueError
from api_exception import *
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

import hashlib
import json
import subprocess
import os
import re
import sys

NetWorkTypes = ['loss', 'delay', 'rate', 'delay_percent']
NetWorkTypes_Info = {
    'rate': 'kbps',
    'delay': 'ms',
    'loss': '%',
}

setting_info = {}  # 每个IP设定的情况
setting_ips = []
if sys.platform == 'win32':
    ip_while_txt_path = os.path.join(os.path.dirname(__file__), 'ip_while.txt')
else:
    ip_while_txt_path = 'ip_while.txt'

app = Flask(__name__)
ThreadPool = ThreadPoolExecutor(max_workers=10)


@app.before_request
def ip_check():
    global setting_ips
    with open(ip_while_txt_path, 'r') as f:
        if request.remote_addr not in f.read().split('\n'):
            logger.error(f'{request.remote_addr} not in ip_while_list')
            abort(403)
    logger.info(
        f'request from: {request.remote_addr}, request path: {request.path}, request params: {request.data}, request header: {request.headers}')

    try:
        json.loads(request.data)
    except Exception as e:
        logger.error(f'json loads error, {e}, data={request.data}')  # json 解析异常
        abort(400)

    params_rule = {
        'ip': Rule(required=True, type=str),
    }
    ip = pre.parse(params_rule).get('ip')

    if not ip:
        logger.error(f'path:{request.path}, {IPError.msg}')
        raise IPError

    setting_ips = list(set(ip.replace(' ', '').replace(',', '\n').replace('，', '\n').split('\n')))


@app.errorhandler(ParamsValueError)
def params_value_error(e):
    # 参数校验失败后 返回此响应
    data = pre.fmt_resp(e).json
    logger.error(f'api={request.path}, err_info={data}, request_data={request.json}')
    return json.dumps({'status': 4, 'msg': data['respMsg']}), 200, {'Content-Type': 'application/json'}  # 参数校验失败


def check_sign(params):
    sign = hashlib.md5('LT'.join(["NetWorkTest", params.get('ip'), 'CsztTest666']).encode()).hexdigest().lower()
    if sign != params.get('sign'):
        logger.error(f'{SignCheckError.msg}: {sign}, params: {params}')
        raise SignCheckError


def run_command(command):
    try:
        t = time.time()
        output = subprocess.check_output(command + '&', shell=True, stderr=subprocess.STDOUT, timeout=10)
        logger.info(f'NetWorkSet: {command}, use_time: {time.time() - t}')
    except subprocess.CalledProcessError as e:
        logger.error(f'{CalledProcessError.msg}: {str(e)}')
        raise CalledProcessError
    return output


def params_check(data, data_type):
    if not isinstance(data, data_type):
        logger.error(f'params type error: params={data}, params_type={type(data)}')
        raise ParamsTypeError

    if data < 0:
        logger.error(f'params value error: params={data}, params={data}')
        raise ParamsTypeError

    return data


def set_network(params):
    NetworkType_info = params.get('NetworkType')
    if not NetworkType_info:
        logger.error(f'path:{request.path}, {NetworkTypeError.msg}')
        raise NetworkTypeError
    port = params.get('port')
    outgoing_shell_list = []
    incoming_shell_list = []

    for ip in setting_ips:
        # 保存每个 IP 设置了上行或者下行规则
        setting_info.setdefault(ip, [])
        outgoing_shell = f"tcset eth0 --network {ip} --change" if not port else f"tcset eth0 --network {ip} --port {port} --change"
        incoming_shell = f"tcset eth0 --src-network {ip} --direction incoming --change" if not port else f"tcset eth0 --src-network {ip} --port {port} --direction incoming --change"

        for NetworkType, NetworkValue in NetworkType_info.items():
            # 校验参数, 只接受 int 类型数据
            outgoing_data = params_check(NetworkValue.get("outgoing_data"), int)
            incoming_data = params_check(NetworkValue.get("incoming_data"), int)
            assert NetworkType in NetWorkTypes, f'NetworkType Parameter exception, NetworkType={NetworkType}'

            if NetworkType != 'delay_percent':
                outgoing_shell = outgoing_shell + f' --{NetworkType} {outgoing_data}{NetWorkTypes_Info[NetworkType]}' if outgoing_data else outgoing_shell
                incoming_shell = incoming_shell + f' --{NetworkType} {incoming_data}{NetWorkTypes_Info[NetworkType]}' if incoming_data else incoming_shell

            else:
                outgoing_delay_percent = params_check(NetworkValue.get("outgoing_delay_percent"), int)
                incoming_delay_percent = params_check(NetworkValue.get("incoming_delay_percent"), int)

                # 上行数据和上行概率必须同时有值
                if (not outgoing_data and outgoing_delay_percent) or (outgoing_data and not outgoing_delay_percent):
                    raise DelayPercentError

                # 下行数据和下行概率必须同时有值
                if (not incoming_data and incoming_delay_percent) or (incoming_data and not incoming_delay_percent):
                    raise DelayPercentError

                if outgoing_data:
                    outgoing_delay_data = re.search(r'--delay.*ms', outgoing_shell)
                    math_outgoing_delay_data = outgoing_delay_data.group() if outgoing_delay_data else ''
                    if math_outgoing_delay_data:
                        outgoing_shell = outgoing_shell.replace(math_outgoing_delay_data,
                                                                f' --delay {outgoing_data}ms --reordering {100 - outgoing_delay_percent}%')
                    else:
                        outgoing_shell = outgoing_shell + f' --delay {outgoing_data}ms --reordering {100 - outgoing_delay_percent}%'

                if incoming_data:
                    incoming_delay_data = re.search(r'--delay.*ms', incoming_shell)
                    math_incoming_delay_data = incoming_delay_data.group() if incoming_delay_data else ''
                    if math_incoming_delay_data:
                        incoming_shell = incoming_shell.replace(math_incoming_delay_data,
                                                                f' --delay {incoming_data}ms --reordering {100 - incoming_delay_percent}%')
                    else:
                        incoming_shell = incoming_shell + f' --delay {incoming_data}ms --reordering {100 - incoming_delay_percent}%'

        if outgoing_shell not in [f"tcset eth0 --network {ip} --change",
                                  f"tcset eth0 --network {ip} --port {port} --change"]:
            outgoing_shell_list.append(outgoing_shell)
            if f'outgoing' not in setting_info[ip]:
                setting_info[ip].append('outgoing')

        if incoming_shell not in [f"tcset eth0 --src-network {ip} --direction incoming --change",
                                  f"tcset eth0 --src-network {ip} --port {port} --direction incoming --change"]:
            incoming_shell_list.append(incoming_shell)
            if 'incoming' not in setting_info[ip]:
                setting_info[ip].append('incoming')

    return outgoing_shell_list, incoming_shell_list


# 设置单个网络状态接口
@app.route('/NetWorkSet', methods=['POST'])
def NetWorkSet():
    params_rule = {
        'sign': Rule(required=True, type=str),
        'NetworkType': Rule(required=True, type=dict),
        'ip': Rule(required=True, type=str),
        'port': Rule(required=False, type=int),
    }
    # 参数校验
    rst = pre.parse(params_rule)
    # 验签
    check_sign(rst)
    outgoing_shell_list, incoming_shell_list = set_network(rst)

    for ip in setting_ips:
        if ip not in setting_info: continue
        if not setting_info[ip]:
            setting_info.pop(ip)
            continue

        if 'outgoing' in setting_info[ip]:
            outgoing_shell_list.append(f'tcdel eth0 --network {ip}')

        if 'incoming' in setting_info[ip]:
            incoming_shell_list.append(f'tcdel eth0 --direction incoming --src-network {ip}')

    outgoing_all_task = [ThreadPool.submit(run_command, shell) for shell in outgoing_shell_list]
    incoming_all_task = [ThreadPool.submit(run_command, shell) for shell in incoming_shell_list]

    outgoing_results = [i.result() for i in outgoing_all_task]
    incoming_results = [i.result() for i in incoming_all_task]
    wait(outgoing_all_task, return_when=ALL_COMPLETED)
    wait(incoming_all_task, return_when=ALL_COMPLETED)
    return json.dumps({'status': 0, 'msg': 'network set success'}), 200, {'Content-Type': 'application/json'}


# 清除所有弱网规则接口
@app.route('/ClearAllRules', methods=['POST'])
def ClearAllRules():
    """
    :params: 传入 ip， string类型，多个ip用逗号','或者换行符隔开 '\n'
    :return:
    """
    outgoing_shell_list = []
    incoming_shell_list = []
    for ip in setting_ips:
        if ip not in setting_info: continue
        if not setting_info[ip]:
            setting_info.pop(ip)
            continue
        outgoing_shell_list.append(f'tcdel eth0 --network {ip}')
        incoming_shell_list.append(f'tcdel eth0 --direction incoming --src-network {ip}')

    outgoing_all_task = [ThreadPool.submit(run_command, shell) for shell in outgoing_shell_list]
    incoming_all_task = [ThreadPool.submit(run_command, shell) for shell in incoming_shell_list]

    outgoing_results = [i.result() for i in outgoing_all_task]
    incoming_results = [i.result() for i in incoming_all_task]
    wait(outgoing_all_task, return_when=ALL_COMPLETED)
    wait(incoming_all_task, return_when=ALL_COMPLETED)
    return json.dumps({'status': 0, 'info': 'clear all network rules success'}), 200, {
        'Content-Type': 'application/json'}


def ping_ip(ip):
    res_data = ''
    ping_data = os.popen(f'ping -c 1 -w 5 {ip} &').read()
    math_delay_data = re.search(r'.* time=.* ms', ping_data)
    math_loss_data = re.search(r'[0-9] packets.*ms', ping_data)
    res_data += math_delay_data.group() + '\n' if math_delay_data else res_data
    res_data += math_loss_data.group() + '\n' if math_loss_data else res_data
    return res_data


# 测试弱网规则是否生效
@app.route('/NetWorkTest', methods=['POST'])
def NetWorkTest():
    """
    :params: 传入 ip， string类型，多个ip用逗号','或者换行符隔开 '\n'
    :return:
    """
    res_data = ''
    all_task = [ThreadPool.submit(ping_ip, i) for i in setting_ips]
    res_data = res_data.join([i.result() for i in all_task])
    wait(all_task, return_when=ALL_COMPLETED)
    return json.dumps({'status': 0, 'msg': res_data}, ensure_ascii=False), {'Content-Type': 'application/json'}


if __name__ == '__main__':
    run_command('tcdel eth0 --all')
    app.run(host="0.0.0.0", port=5000, debug=False)
