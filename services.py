#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2024/9/4 16:15
# Author     ：author lin3
"""
from flask import Flask, request, abort, redirect
from log_system import logger
from pre_request import pre, Rule, ParamsValueError
from common import *
import json

app = Flask(__name__)


@app.before_request
def ip_check():
    with open(ip_while_txt_path, 'r') as f:
        if request.remote_addr not in f.read().split('\n'):
            print(request.remote_addr, type(request.remote_addr), f.read().split('\n'))
            logger.error(f'{request.remote_addr} not in ip_while_list')
            abort(403)
    logger.info(
        f'request from: {request.remote_addr}, request path: {request.path}, request params: {request.data}, request header: {request.headers}')


@app.errorhandler(ParamsValueError)
def params_value_error(e):
    # 参数校验失败后 返回此响应
    data = pre.fmt_resp(e).json
    logger.error(f'api={request.path}, err_info={data}, request_data={request.json}')
    return json.dumps({'status': -1, 'msg': '参数校验失败'}), 200, {'Content-Type': 'application/json'}  # 参数校验失败


# 下载apk包
@app.route('/DownloadApk', methods=['POST'])
def DownloadApk():
    """
    :params:
        apkurl: 包体下载链接，string类型，多个ip用逗号','或者换行符隔开 '\n'
        game: 游戏标识，string类型
    :return:
    """
    params_rule = {
        'apkurl': Rule(required=True, type=str),
        'game': Rule(required=True, type=str),
        'serialno': Rule(required=False, type=str),
    }
    rst = pre.parse(params_rule)
    download_queue.put((rst.get('apkurl'), rst.get('game'), rst.get('serialno', None), init_task_id + 1))
    return json.dumps({'status': 0, 'msg': 'success'}), 200, {'Content-Type': 'application/json'}


# @app.route('/report/<path:game>/<path:filename>')
# def get_report(game, filename):
    # return Response(f"/static/1727250264_20240925154606.html")
    # print(game, filename)
    # # # return
    # return 200
    # return redirect(f"/static/{game}/test_leitingsdk.log/{filename}")
    # return redirect(f"/static/test_leitingsdk.log/{filename}")
    # # return redirect(f"/static/1727250264_20240925154606.html")
    # return render_template(filename)


if __name__ == '__main__':
    ThreadPool.submit(scheduled_tasks)  # 多线程, 提交执行定时任务
    app.run(host="0.0.0.0", port=8000, debug=False)