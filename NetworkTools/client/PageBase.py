#!/usr/bin/python
# -*- coding: UTF-8 -*-
import hashlib
import tkinter as tk
from collections import defaultdict
from tkinter import *
from tkinter import messagebox

# from case import NetworkClear, NetworkTest, NetworkSet
from case import *


class NetworkToolPage:
    def __init__(self, master):
        self.master = master
        self.master.title("弱网模拟工具")

        self.left_Frame = tk.Frame(self.master)
        self.right_Frame = tk.Frame(self.master)
        self.left_Frame.grid(row=0, column=0, padx=20)
        self.right_Frame.grid(row=0, column=1, padx=20)
        self.client = Client(self)  # 实例化 case , 将 NetworkToolPage 所有属性传给 case 注：这里的self=NetworkToolPage

        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        self.IP_Label = Label(self.left_Frame, text="目标IP")  # IP标签
        self.IP_Label.grid(row=0, column=0, pady=10)
        self.IP_Text = Text(self.left_Frame, bd=5, height=10, width=30)  # IP输入框 # todo 加个提示换行分隔多个ip
        self.IP_Text.grid(row=0, column=1, pady=10)

        self.delay_Lable = Label(self.left_Frame, text="网络延迟(ms)")  # 网络延迟标签
        self.delay_Lable.grid(row=1, column=1)
        self.up_delay_Lable = Label(self.left_Frame, text="上行")  # 上行延迟标签
        self.up_delay_Lable.grid(row=2, column=0)
        self.up_delay_Entry = Entry(self.left_Frame, bd=5)  # 上行延迟输入框
        self.up_delay_Entry.grid(row=2, column=1)
        self.down_delay_Lable = Label(self.left_Frame, text="下行")  # 下行延迟标签
        self.down_delay_Lable.grid(row=3, column=0)
        self.down_delay_Entry = Entry(self.left_Frame, bd=5)  # 下行延迟输入框
        self.down_delay_Entry.grid(row=3, column=1, pady=(0, 10))

        self.loss_Label = Label(self.left_Frame, text="网络丢包率(%)")  # 网络丢包标签
        self.loss_Label.grid(row=4, column=1)
        self.up_loss_Lable = Label(self.left_Frame, text="上行")  # 上行丢包标签
        self.up_loss_Lable.grid(row=5, column=0)
        self.up_loss_Entry = Entry(self.left_Frame, bd=5)  # 上行丢包率输入框
        self.up_loss_Entry.grid(row=5, column=1)
        self.down_loss_Lable = Label(self.left_Frame, text="下行")  # 下行丢包标签
        self.down_loss_Lable.grid(row=6, column=0)
        self.down_loss_Entry = Entry(self.left_Frame, bd=5)  # 下行丢包率输入框
        self.down_loss_Entry.grid(row=6, column=1, pady=(0, 10))

        self.rate_Label = Label(self.left_Frame, text="带宽限制(kbps)")  # 带宽限制标签
        self.rate_Label.grid(row=7, column=1)
        self.up_rate_Lable = Label(self.left_Frame, text="上行")  # 上行带宽标签
        self.up_rate_Lable.grid(row=8, column=0)
        self.up_rate_Entry = Entry(self.left_Frame, bd=5)  # 上行带宽输入框
        self.up_rate_Entry.grid(row=8, column=1)
        self.down_rate_Lable = Label(self.left_Frame, text="下行")  # 下行带宽标签
        self.down_rate_Lable.grid(row=9, column=0)
        self.down_rate_Entry = Entry(self.left_Frame, bd=5)  # 下行带宽输入框
        self.down_rate_Entry.grid(row=9, column=1, pady=(0, 10))

        self.probability_delay_Label = Label(self.left_Frame, text="概率延时")  # 概率延时标签
        self.probability_delay_Label.grid(row=10, column=1)
        self.up_delay_data_Lable = Label(self.left_Frame, text="上行延时(ms)")  # 上行延时标签
        self.up_delay_data_Lable.grid(row=11, column=0)
        self.up_delay_data_Entry = Entry(self.left_Frame, bd=5)  # 上行延时输入框
        self.up_delay_data_Entry.grid(row=11, column=1)
        self.up_delay_percent_Lable = Label(self.left_Frame, text="概率（%）")  # 上行概率标签
        self.up_delay_percent_Lable.grid(row=11, column=2)
        self.up_delay_percent_Entry = Entry(self.left_Frame, bd=5)  # 上行概率输入框
        self.up_delay_percent_Entry.grid(row=11, column=3)
        self.down_delay_data_Lable = Label(self.left_Frame, text="下行延时(ms)")  # 下行延时标签
        self.down_delay_data_Lable.grid(row=12, column=0)
        self.down_delay_data_Entry = Entry(self.left_Frame, bd=5)  # 下行延时输入框
        self.down_delay_data_Entry.grid(row=12, column=1, pady=(0, 10))
        self.down_delay_percent_Lable = Label(self.left_Frame, text="概率（%）")  # 下行概率标签
        self.down_delay_percent_Lable.grid(row=12, column=2)
        self.down_delay_percent_Entry = Entry(self.left_Frame, bd=5)  # 下行概率输入框
        self.down_delay_percent_Entry.grid(row=12, column=3, pady=(0, 10))

        self.test_button = tk.Button(self.left_Frame, text="生效测试", command=lambda: self.client_request(path='/NetWorkTest'), padx=10, pady=5)
        self.test_button.grid(row=0, column=2, padx=20)

        self.on_button = tk.Button(self.left_Frame, text="设置", command=lambda: self.client_request(path='/NetWorkSet'), padx=5, pady=5)
        self.on_button.grid(row=13, column=1, padx=20, pady=10)

        self.off_button = tk.Button(self.left_Frame, text="清除", command=lambda: self.client_request(path='/ClearAllRules'), padx=10, pady=5)
        self.off_button.grid(row=13, column=2, padx=20, pady=10)

        # self.button = tk.Button(self.right_Frame, text="Update Message", command=self.show_message)
        # self.button.grid(row=1, column=0)
        #
        # self.button2 = tk.Button(self.right_Frame, text="test!!!", command=self.send.NetworkSet)
        # self.button2.grid(row=2, column=0)
        #
        # self.message_widget = tk.Message(self.right_Frame, text="Your message will appear here", width=300)
        # self.message_widget.grid(row=3, column=0)

        self.TestResMsg_Label = Label(self.right_Frame, text="测试结果")
        self.TestResMsg_Label.grid(row=0, column=0, padx=10)
        self.TestResMsg_Text = Text(self.right_Frame, bd=5, height=10, width=80)
        self.TestResMsg_Text.grid(row=0, column=1, pady=10)

        self.ServerResCode_Label = Label(self.right_Frame, text="HTTPCode")
        self.ServerResCode_Label.grid(row=1, column=0, padx=10)
        self.ServerResCode_Text = Text(self.right_Frame, bd=5, height=2, width=10)
        # self.ServerResCode_Text = Text(self.right_Frame, width=10, bd=5, height=2, pady=10)
        self.ServerResCode_Text.grid(row=1, column=1, sticky='w')

        self.ServerResMsg_Label = Label(self.right_Frame, text="服务器响应")
        self.ServerResMsg_Label.grid(row=2, column=0, padx=10)
        self.ServerResMsg_Text = Text(self.right_Frame, bd=5, height=30, width=80)
        self.ServerResMsg_Text.grid(row=2, column=1, pady=10)

        #
        # self.ServerResMsgScrollbar = Scrollbar(self.right_Frame, orient=VERTICAL)
        # self.ServerResLable = Label(self.right_Frame, text="服务器响应")
        # self.ServerResText = Text(self.right_Frame, width=80, height=9, wrap=CHAR, insertborderwidth=1, yscrollcommand=self.ServerResMsgScrollbar.set)
        #
        # self.ReqParamScrollbar = Scrollbar(self.right_Frame, orient=VERTICAL)
        # self.ReqParamLable = Label(self.right_Frame, text="请求参数")
        # self.ReqParamText = Text(self.right_Frame, width=80, height=9, wrap=CHAR, insertborderwidth=1, yscrollcommand=self.ReqParamScrollbar.set)

        # self.ServerResCodeLabel = Label(self.right_Frame, text="HttpCode")
        # self.ServerResCodeText = Text(self.right_Frame, width=8, bd=1, height=1, wrap=CHAR)
        #
        # self.ServerResMsgScrollbar = Scrollbar(self.right_Frame, orient=VERTICAL)
        # self.ServerResLable = Label(self.right_Frame, text="服务器响应")
        # self.ServerResText = Text(self.right_Frame, width=80, height=9, wrap=CHAR, insertborderwidth=1, yscrollcommand=self.ServerResMsgScrollbar.set)
        #
        # self.ReqParamScrollbar = Scrollbar(self.right_Frame, orient=VERTICAL)
        # self.ReqParamLable = Label(self.right_Frame, text="请求参数")
        # self.ReqParamText = Text(self.right_Frame, width=80, height=9, wrap=CHAR, insertborderwidth=1, yscrollcommand=self.ReqParamScrollbar.set)

    def testCallBack(self):
        messagebox.showinfo("测试结果", "测试通过")

    def client_request(self, path):
        status_info = {
            1: 'IP异常',
            2: '网络设置类型异常',
            3: '验签失败',
            4: '参数校验失败',
            5:  '指令执行失败',
            999: 'IP不能为空',
            888: '未知错误，请联系lin3、liangsy检查工具',
        }
        status_code, res_data = self.client.http_request(path=path)
        if status_code != 200:
            messagebox.showerror(title='Error', message=f'http error {status_code}')
        else:
            if res_data.get('status') != 0:
                messagebox.showinfo(title='Error', message=f'{status_info[res_data.get("status")]}')

            else:
                messagebox.showinfo(title='Info', message='success')

        if path == '/NetWorkTest':
            print(res_data)
            self.TestResMsg_Text.delete(1.0, END)
            self.TestResMsg_Text.insert(END, res_data['msg'])
            return

        self.ServerResCode_Text.delete(1.0, END)
        self.ServerResCode_Text.insert(END, status_code)
        self.ServerResMsg_Text.delete(1.0, END)
        self.ServerResMsg_Text.insert(END, res_data)

    def on_closing(self):
        # 在窗口关闭之前发送请求
        self.client_request(path='/ClearAllRules')
        # 关闭窗口
        self.master.destroy()

    # def update_message(self):
    #     user_text = self.IP_Text.get("1.0", tk.END).strip()
    #     # self.get_NetworkType()
    #     self.get_ip()
    #     self.message_widget.config(text=user_text)
    #     # self.luoji.get_value()
    #     # todo 获取按钮值之后进行请求
    #     # todo 请求后处理返回数据的展示 return data

    # def show_message(self):
    #     self.message_widget.config(text=self.send.message_text)

    # self.get_params()
    # print(self.params)


if __name__ == "__main__":
    GUI = tk.Tk()
    NetworkTool = NetworkToolPage(GUI)
    GUI.mainloop()
