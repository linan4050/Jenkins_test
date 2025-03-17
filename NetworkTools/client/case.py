import hashlib
import json
import requests
import tkinter as tk
# from PageBase import *


class Client:
    def __init__(self, GUI):
        self.GUI = GUI      #  在 NetworkToolPage 中实例化了 case， self就能直接拿到  NetworkToolPage 里的所有属性了，后面 self.gui 直接拿到 NetworkToolPage 的属性包括输入值
        self.url = 'http://47.101.179.76:5000'
        self.ips = ''       # 存储ip 用于还原弱网设置，后端兼容英文逗号、换行符分隔
        self.setip = ''     # 当前单次设置的ip
        self.NetworkType = {
            'rate': {'outgoing_data': 0, 'incoming_data': 0},  # kbps
            'delay': {'outgoing_data': 0, 'incoming_data': 0},  # ms
            'loss': {'outgoing_data': 0, 'incoming_data': 0},  # %
            'delay_percent': {
                'outgoing_data': 0, 'incoming_data': 0, 'outgoing_delay_percent': 0, 'incoming_delay_percent': 0
            },      # 延时 delay 和概率延时 delay_percent 同时传入时，仅生效概率延时 delay_percent
        }
        self.message_text = None



    # def get_ip(self):
    #     self.ips += f'{self.GUI.IP_Text.get("1.0", tk.END).strip()},'   # 后端兼容英文逗号、换行符分隔，针对分开多次设置不同ip，需要+英文逗号以便后端分割
    #     return self.ips

    def get_ip(self):
        self.setip = self.GUI.IP_Text.get("1.0", tk.END).strip()
        return self.setip


    def get_params(self):
        # self.setip = self.GUI.IP_Text.get("1.0", tk.END).strip()
        self.get_ip()
        delay_outgoing_data = self.GUI.up_delay_Entry.get().strip()
        delay_incoming_data = self.GUI.down_delay_Entry.get().strip()
        loss_outgoing_data = self.GUI.up_loss_Entry.get().strip()
        loss_incoming_data = self.GUI.down_loss_Entry.get().strip()
        rate_outgoing_data = self.GUI.up_rate_Entry.get().strip()
        rate_incoming_data = self.GUI.down_rate_Entry.get().strip()
        delay_percent_outgoing_data = self.GUI.up_delay_data_Entry.get().strip()
        delay_percent_incoming_data = self.GUI.down_delay_data_Entry.get().strip()
        delay_percent_outgoing_delay_percent = self.GUI.up_delay_percent_Entry.get().strip()
        delay_percent_incoming_delay_percent = self.GUI.down_delay_percent_Entry.get().strip()

        # ips = self.GUI.IP_Text.get("1.0", tk.END).strip()
        port = 0  # todo 最后补一下port输入框和取值
        params = {
            'NetworkType': {
                'rate': {'outgoing_data': rate_outgoing_data, 'incoming_data': rate_incoming_data},  # kbps
                'delay': {'outgoing_data': delay_outgoing_data, 'incoming_data': delay_incoming_data},  # ms
                'loss': {'outgoing_data': loss_outgoing_data, 'incoming_data': loss_incoming_data},  # %
                'delay_percent': {'outgoing_data': delay_percent_outgoing_data,
                                  'incoming_data': delay_percent_incoming_data,
                                  'outgoing_delay_percent': delay_percent_outgoing_delay_percent,
                                  'incoming_delay_percent': delay_percent_incoming_delay_percent},
            },
            'ip': self.setip,
        }

        params.update({"sign": hashlib.md5(
            'LT'.join(["NetWorkTest", params.get('ip'), 'CsztTest666']).encode()).hexdigest().lower()})
        print(params)
        return params

    def http_request(self, path):
        try:
            if path == '/ClearAllRules':
                send_data = {'ip': self.ips}

                res = requests.post(self.url + path, data=json.dumps(send_data), headers={'Content-Type': 'application/json'})
                if res.status_code == 200:
                    self.ips = ''
                    self.setip = ''

            elif path == '/NetWorkSet':
                send_data = self.get_params()
                res = requests.post(self.url + path, data=json.dumps(send_data), headers={'Content-Type': 'application/json'})
                if res.status_code == 200:
                    self.ips += f'{self.GUI.IP_Text.get("1.0", tk.END).strip()},'   # 后端兼容英文逗号、换行符分隔，针对分开多次设置不同ip，需要+英文逗号以便后端分割
                    # print(f'当前ips: {self.ips}【检查是否都有换行、英文逗号分割每个ip！！！】')

            elif path == '/NetWorkTest':
                self.get_ip()
                if not self.setip:
                    return 999, ''
                send_data = {'ip': self.setip}
                res = requests.post(self.url + path, data=json.dumps(send_data), headers={'Content-Type': 'application/json'})

            else:
                return 888, ''

            if res.status_code != 200:
                return res.status_code, res.content
            return res.status_code, res.json()
        except Exception as e:
            print(str(e))


    # def NetworkTest(self):
    #     self.get_ip()
    #     try:
    #         data = {'ip': self.ips}
    #         res = requests.post(self.test_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    #         # print(res.content)
    #         # print(res.text)
    #         # print(res.status_code)
    #         # print(res.json())
    #         # print(res.json(), type(res.json()), type(res.text))
    #         self.message_text = {
    #             'HttpCode': res.status_code,
    #             '服务器响应': res.json(),
    #             '请求参数': data,
    #         }
    #         # return res.json()
    #         print(self.message_text)
    #         return self.message_text
    #     except requests.exceptions.RequestException as e:
    #         print(f"请求失败: {e}")
    #         return {'status': -1, 'info': str(e)}
    #
    # # ips = ["139.224.165.26", "139.224.165.26"]
    # # result = NetworkTest(test_url, ips)
    # # print(result)
    #
    #
    #
    # def NetworkClear(self):
    #     try:
    #         data = {'ip': self.ips}
    #         res = requests.post(self.clear_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    #         # print(res.content, res.text, res.status_code)
    #         # print(res.json(), type(res.json()), type(res.text))
    #         # res.raise_for_status()  # 检查是否请求成功。如果是4XX/5XX错误，会引发HTTPError异常
    #         # return res.json()
    #         self.message_text = {
    #             'HttpCode': res.status_code,
    #             '服务器响应': res.json(),
    #             '请求参数': data,
    #         }
    #
    #         print(self.message_text)
    #         # return res.json()
    #         return self.message_text
    #     except requests.exceptions.RequestException as e:
    #         print(f"请求失败: {e}")
    #         return {'status': -1, 'info': str(e)}
    #
    # # ips = ["139.224.165.26", "139.224.165.26"]
    # # result = NetworkClear(clear_url, ips)
    # # print(result)
    #
    #
    # def NetworkSet(self):
    #     self.NetworkClear()
    #     try:
    #         data = self.get_params()
    #         res = requests.post(self.set_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    #         self.message_text = {
    #             'HttpCode': res.status_code,
    #             '服务器响应': res.json(),
    #             '请求参数': data,
    #         }
    #         # return res.json()
    #         print(self.message_text)
    #         return self.message_text
    #     except requests.exceptions.RequestException as e:
    #         print(f"请求失败: {e}")
    #         return {'status': -1, 'info': str(e)}
    #
    #
