#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2023/11/6 18:32
# Author     ：author lin3
"""
import json
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Notebook, Combobox
from testcase import *
from page.PageBase import PageBase

default_text = []
optional_values = ['productId', '扩展字段']

class IosRechargePage(PageBase):
    def __init__(self, Pageframe):
        super(IosRechargePage, self).__init__(Pageframe)

    def init_Component(self):
        super().init_Component()
        self.ExtendInfoLable = Label(self.left_frame, text="扩展字段")
        self.ExtendInfoText = Text(self.left_frame, width=40, height=8, bd=2, wrap=CHAR, insertborderwidth=1)
        self.InsertDeafultText(self.ExtendInfoText, text='不是必填参数, 具体看平台订单是否有扩展信息, 例子: {"test": "test"}', ComponentType='Text')

        self.send_button = Button(self.left_frame, width=8, height=1, text="发送", command=self.get_Entry_data)
        self.Component_grid()

    def Component_grid(self):
        self.left_frame.grid()
        self.right_frame.grid(row=0, column=1, pady=10, sticky='n')
        self.gameOrderNoLable.grid(row=0, column=0, pady=10, sticky='e')
        self.gameOrderNoEntry.grid(row=0, column=1, pady=10, padx=10, sticky='w')
        self.leitingNoLable.grid(row=1, column=0, pady=10, sticky='e')
        self.leitingNoEntry.grid(row=1, column=1, pady=10, padx=10, sticky='w')
        self.thirdAmountLable.grid(row=2, column=0, sticky=E, pady=10)
        self.thirdAmountEntry.grid(row=2, column=1, pady=10, padx=10, sticky='w')
        self.channelNoLable.grid(row=3, column=0, sticky=E, pady=10)
        self.channelNoEntry.grid(row=3, column=1, pady=10, padx=10, sticky='w')
        self.userIdLable.grid(row=4, column=0, sticky=E, pady=10)
        self.userIdEntry.grid(row=4, column=1, pady=10, padx=10, sticky='w')
        self.productIdLable.grid(row=5, column=0, sticky=E, pady=10)
        self.productIdEntry.grid(row=5, column=1, pady=10, padx=10, sticky='w')
        self.ExtendInfoLable.grid(row=6, column=0, sticky=E, pady=10)
        self.ExtendInfoText.grid(row=6, column=1, pady=10, padx=10, sticky='w')
        self.keyLable.grid(row=7, column=0, sticky=E, pady=10)
        self.keyEntry.grid(row=7, column=1, pady=10, padx=10, sticky='w')
        self.NotifyUrlLable.grid(row=8, column=0, sticky=E, pady=10)
        self.NotifyUrlText.grid(row=8, column=1, pady=10, padx=10, sticky='w')
        self.send_button.grid(row=9, column=0, pady=10, padx=10)

        self.ServerResCodeLabel.grid(row=0, column=2)
        self.ServerResCodeText.grid(row=0, column=3, sticky='w')
        self.ServerResLable.grid(row=1, column=2, pady=20, sticky='n')
        self.ServerResText.grid(row=1, column=3, pady=25)
        self.ServerResMsgScrollbar.grid(row=1, column=4, pady=25, sticky='nsew')
        self.ServerResMsgScrollbar.config(command=self.ServerResText.yview)

        self.ReqParamLable.grid(row=2, column=2, sticky='n')
        self.ReqParamText.grid(row=2, column=3, pady=5)
        self.ReqParamScrollbar.grid(row=2, column=4, pady=5, sticky='nsew')
        self.ReqParamScrollbar.config(command=self.ReqParamText.yview)

    def get_Entry_data(self):
        gameOrderNo = self.ValueEmptyCheck('游戏订单号', self.gameOrderNoEntry.get(), optional_values)
        thirdNo = self.ValueEmptyCheck('雷霆订单号', self.leitingNoEntry.get(), optional_values)
        thirdAmount = self.ValueEmptyCheck('金额', self.thirdAmountEntry.get(), optional_values)
        channelNo = self.ValueEmptyCheck('渠道号', self.channelNoEntry.get(), optional_values)
        userId = self.ValueEmptyCheck('雷霆 sid', self.userIdEntry.get(), optional_values)
        productId = self.ValueEmptyCheck('productId', self.productIdEntry.get(), optional_values)
        if channelNo == '210009' and productId == '':
            messagebox.showerror(title='Error', message=f'iOS渠道 productId 不能为空')
            return
        extInfo = self.ValueEmptyCheck('扩展字段', self.ExtendInfoText.get(1.0, END), optional_values)
        key = self.ValueEmptyCheck('签名密钥', self.keyEntry.get(), optional_values)
        NotifyUrl = self.ValueEmptyCheck('回调地址', self.NotifyUrlText.get(1.0, END), optional_values)
        status_code, res, params = RechargeNotify(gameOrderNo, thirdAmount, thirdNo, channelNo, userId, productId, extInfo, key, NotifyUrl, self.callback)

        self.ChangeTestConfig([self.ServerResCodeText, self.ServerResText, self.ReqParamText], state='normal')
        self.clear_text_data([self.ServerResCodeText, self.ServerResText, self.ReqParamText])
        self.ServerResCodeText.insert(END, status_code)
        self.ServerResText.insert(END, res)
        self.ReqParamText.insert(END, f'{params}')
        self.ChangeTestConfig([self.ServerResCodeText, self.ServerResText, self.ReqParamText], state='disabled')



