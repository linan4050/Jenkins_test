#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2023/11/6 21:21
# Author     ：author lin3
"""
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Notebook, Combobox
from testcase import *
import leiting_encrypt as encrypt
from page.PageBase import PageBase


class SdkLoginPage(PageBase):
    def __init__(self, Pageframe, IosRechargePage, IosRefundPage):
        super(SdkLoginPage, self).__init__(Pageframe)
        self.IosRechargePage = IosRechargePage
        self.IosRefundPage = IosRefundPage

    def init_Component(self):
        self.AccountLable, self.AccountEntry = self.LabelEntry(frame=self.left_frame, LableText='账号', bd=2, cursor='arrow', width=40, textvariable=StringVar())
        self.PasswordLable, self.PasswordEntry = self.LabelEntry(frame=self.left_frame, LableText='密码', bd=2, cursor='arrow', width=40, textvariable=StringVar())
        self.channelNoLable, self.channelNoEntry = self.LabelEntry(frame=self.left_frame, LableText='渠道号', bd=2, cursor='arrow', width=40, textvariable=StringVar())
        self.GameLable, self.GameEntry = self.LabelEntry(frame=self.left_frame, LableText='游戏标识', bd=2, cursor='arrow', width=40, textvariable=StringVar())

        self.LoginUrlLable = Label(self.left_frame, text="SDK登录地址")
        self.LoginUrlText = Text(self.left_frame, width=40, height=3, bd=2, wrap=CHAR, insertborderwidth=1)
        self.LoginUrlText.insert(END, 'https://login.leiting.com/sdk/login.do')

        self.ServerResMsgScrollbar = Scrollbar(self.right_frame, orient=VERTICAL)

        self.ServerResCodeLabel = Label(self.right_frame, text="HttpCode")
        self.ServerResCodeText = Text(self.right_frame, width=8, bd=1, height=1, wrap=CHAR)

        self.ServerResLable = Label(self.right_frame, text="服务器响应")
        self.ServerResText = Text(self.right_frame, width=80, height=9, wrap=CHAR, insertborderwidth=1, yscrollcommand=self.ServerResMsgScrollbar.set)

        self.ReqParamScrollbar = Scrollbar(self.right_frame, orient=VERTICAL)
        self.ReqParamLable = Label(self.right_frame, text="请求参数")
        self.ReqParamText = Text(self.right_frame, width=80, height=9, wrap=CHAR, insertborderwidth=1, yscrollcommand=self.ReqParamScrollbar.set)

        self.send_button = Button(self.left_frame, width=8, height=1, text="发送", command=self.get_Entry_data)
        self.Component_grid()

    def Component_grid(self):
        self.left_frame.grid(row=0, column=0, sticky='n')
        self.right_frame.grid(row=0, column=1, pady=10, sticky='n')
        self.AccountLable.grid(row=0, column=0, pady=10, sticky='e')
        self.AccountEntry.grid(row=0, column=1, pady=10, padx=10, sticky='w')
        self.PasswordLable.grid(row=1, column=0, pady=10, sticky='e')
        self.PasswordEntry.grid(row=1, column=1, pady=10, padx=10, sticky='w')
        self.channelNoLable.grid(row=2, column=0, sticky=E, pady=10)
        self.channelNoEntry.grid(row=2, column=1, pady=10, padx=10, sticky='w')
        self.GameLable.grid(row=3, column=0, sticky=E, pady=10)
        self.GameEntry.grid(row=3, column=1, pady=10, padx=10, sticky='w')
        self.LoginUrlLable.grid(row=4, column=0, sticky=E, pady=10)
        self.LoginUrlText.grid(row=4, column=1, pady=10, padx=10, sticky='w')
        self.send_button.grid(row=5, column=0, pady=10, padx=10)

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
        account = self.ValueEmptyCheck('账号', self.AccountEntry.get())
        password = encrypt.leitingsdk_pwd_des.encode(self.ValueEmptyCheck('密码', self.PasswordEntry.get()))
        channelNo = self.ValueEmptyCheck('渠道号', self.channelNoEntry.get())
        game = self.ValueEmptyCheck('游戏标识', self.GameEntry.get())
        loginurl = self.ValueEmptyCheck('SDK登陆地址', self.LoginUrlText.get('0.0', END))
        status_code, res, params = sdkLogin({'username': account, 'password': password, 'game': game, 'channelNo': channelNo}, loginurl, self.callback)

        self.ChangeTestConfig([self.ServerResCodeText, self.ServerResText, self.ReqParamText], state='normal')
        self.clear_text_data([self.ServerResCodeText, self.ServerResText, self.ReqParamText])
        self.ServerResCodeText.insert(END, status_code)
        self.ServerResText.insert(END, res)
        self.ReqParamText.insert(END, f'{params}')
        self.ChangeTestConfig([self.ServerResCodeText, self.ServerResText, self.ReqParamText], state='disabled')

        if status_code == 200 and res.get('status', '') == 0:
            self.IosRechargePage.userIdEntry.delete(0, END)
            self.IosRechargePage.userIdEntry.insert(END, res['data']['sid'])
            self.IosRechargePage.channelNoEntry.delete(0, END)
            self.IosRechargePage.channelNoEntry.insert(END, channelNo)

            self.IosRefundPage.userIdEntry.delete(0, END)
            self.IosRefundPage.userIdEntry.insert(END, res['data']['sid'])
            self.IosRefundPage.channelNoEntry.delete(0, END)
            self.IosRefundPage.channelNoEntry.insert(END, channelNo)
