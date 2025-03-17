#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2023/11/8 14:39
# Author     ：author lin3
"""
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Notebook, Combobox


class PageBase:
    def __init__(self, Pageframe):
        self.default_text = []          # 默认值文本
        self.clear_Component_default_text = []  # 清理输入框默认值, 只有首次触发输入框点击事件时进行清除
        self.left_frame = Frame(Pageframe)
        self.right_frame = Frame(Pageframe)
        self.init_Component()

    def init_Component(self):
        self.gameOrderNoLable, self.gameOrderNoEntry = self.LabelEntry(frame=self.left_frame, LableText='游戏订单号', bd=2, cursor='arrow', width=40, textvariable=StringVar())
        self.InsertDeafultText(self.gameOrderNoEntry, text='从 manager 系统上查, 必填参数', ComponentType='Entry')

        self.leitingNoLable, self.leitingNoEntry = self.LabelEntry(frame=self.left_frame, LableText='雷霆订单号', bd=2, cursor='arrow', width=40, textvariable=StringVar())
        self.InsertDeafultText(self.leitingNoEntry, text='从 manager 系统上查, 必填参数', ComponentType='Entry')

        self.thirdAmountLable, self.thirdAmountEntry = self.LabelEntry(self.left_frame, LableText='金额（分）', bd=2, cursor='arrow', width=40, textvariable=StringVar())
        self.InsertDeafultText(self.thirdAmountEntry, text='支付金额*100, 例:6元*100=600, 必填参数', ComponentType='Entry')

        self.channelNoLable, self.channelNoEntry = self.LabelEntry(self.left_frame, LableText='渠道号', bd=2, cursor='arrow', width=40, textvariable=StringVar())
        self.channelNoEntry.insert(END, '110001')

        self.userIdLable, self.userIdEntry = self.LabelEntry(self.left_frame, LableText='雷霆 Sid', bd=2, cursor='arrow', width=40, textvariable=StringVar())
        self.InsertDeafultText(self.userIdEntry, text='登录雷霆SDK账号后会自动获取, 必填参数', ComponentType='Entry')

        self.productIdLable, self.productIdEntry = self.LabelEntry(self.left_frame, LableText='productId', bd=2, cursor='arrow', width=40, textvariable=StringVar())
        self.InsertDeafultText(self.productIdEntry, text='商品ID, iOS需要填, Android不填', ComponentType='Entry')

        self.keyLable, self.keyEntry = self.LabelEntry(self.left_frame, LableText='签名密钥', bd=2, cursor='arrow', width=40, textvariable=StringVar())
        self.InsertDeafultText(self.keyEntry, text='游戏配置, 每个游戏的key不一样, 必填参数', ComponentType='Entry')

        self.NotifyUrlLable = Label(self.left_frame, text="游戏回调地址")
        self.NotifyUrlText = Text(self.left_frame, width=40, height=2, bd=2, wrap=CHAR, insertborderwidth=1)
        self.InsertDeafultText(self.NotifyUrlText, text='每个游戏回调地址不一样, 具体找游戏研发提供地址, 必填参数', ComponentType='Text')

        self.ServerResMsgScrollbar = Scrollbar(self.right_frame, orient=VERTICAL)

        self.ServerResCodeLabel = Label(self.right_frame, text="HttpCode")
        self.ServerResCodeText = Text(self.right_frame, width=8, bd=1, height=1)

        self.ServerResLable = Label(self.right_frame, text="服务器响应")
        self.ServerResText = Text(self.right_frame, width=80, height=9, wrap=CHAR, insertborderwidth=1, yscrollcommand=self.ServerResMsgScrollbar.set)

        self.ReqParamScrollbar = Scrollbar(self.right_frame, orient=VERTICAL)
        self.ReqParamLable = Label(self.right_frame, text="请求参数")
        self.ReqParamText = Text(self.right_frame, width=80, height=9, wrap=CHAR, insertborderwidth=1, yscrollcommand=self.ReqParamScrollbar.set)

    # 传参校验，为空时报错
    def ValueEmptyCheck(self, param, data, optional_values=None):
        data = data.replace(' ', '').replace('\n', '').replace('\t', '')

        if optional_values is None:
            optional_values = []

        if data in self.default_text or data in ['', None]:
            if param in optional_values:
                return ''
            else:
                messagebox.showerror(title='Error', message=f'{param}不能为空')
                raise Exception(f'{param}不能为空')
        else:
            return data

    # 首次点击输入框时清除默认值
    def clear_default_text(self, event, Component, ComponentType):
        data = Component.get(1.0, END) if ComponentType == 'Text' else Component.get()
        data = data.replace(' ', '').replace('\n', '').replace('\t', '')
        if Component not in self.clear_Component_default_text:
            if data in self.default_text:
                delete_first = 0 if ComponentType == 'Entry' else 1.0
                Component.delete(delete_first, END)
                self.clear_Component_default_text.append(Component)

    def LabelEntry(self, frame, LableText, **kwargs):
        lable = Label(frame, text=LableText)
        entry = Entry(frame, **kwargs)
        return lable, entry

    # 添加默认值
    def InsertDeafultText(self, Component, text, ComponentType='Entry'):
        self.default_text.append(text.replace(' ', '').replace('\n', '').replace('\t', ''))
        Component.insert(END, text)
        Component.bind('<Button-1>', lambda event: self.clear_default_text(event, Component, ComponentType))

    # 清除请求响应输入框内的值，在下次请求时触发
    def clear_text_data(self, Components):
        if type(Components) == list:
            for i in Components:
                if i.get(1.0, END):
                    i.delete(1.0, END)
        else:
            if Components.get(1.0, END):
                Components.delete(1.0, END)

    # 切换 Text 读写状态。
    def ChangeTestConfig(self, Components, state):
        if type(Components) == list:
            for i in Components:
                i.config(state=state)
        else:
            Components.config(state=state)

    # 请求异常回调
    def callback(self, msg):
        messagebox.showerror(title='Error', message=f'请求异常: {msg}')
