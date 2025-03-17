#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2023/11/6 18:35
# Author     ：author lin3

"""
from tkinter import *
from tkinter.ttk import Notebook

from page.OverseasRechargePage import OverseasRechargePage
from page.iosRechargePage import IosRechargePage
from page.iosRefundPage import IosRefundPage
from page.sdkLoginPage import SdkLoginPage

UI = Tk()
page = Notebook()  # 分页栏
page.grid()
UI.title("回调测试工具")  # 窗口名
UI.geometry("1050x565+50+50")



class start_gui:
    def __init__(self):
        self.IosRefundPageframe = Frame(page)
        self.IosRechargePageframe = Frame(page)
        self.SdkLoginPageframe = Frame(page)
        self.OverseasRechargePageframe = Frame(page)
        page.add(self.IosRechargePageframe, text="充值发货")
        page.add(self.IosRefundPageframe, text="IOS退款")
        page.add(self.SdkLoginPageframe, text="雷霆SDK登录")
        page.add(self.OverseasRechargePageframe, text="海外充值发货")
        self.IosRechargePage = IosRechargePage(self.IosRechargePageframe)
        self.IosRefundPage = IosRefundPage(self.IosRefundPageframe)
        self.SdkLoginPage = SdkLoginPage(self.SdkLoginPageframe, self.IosRechargePage, self.IosRefundPage)
        self.OverseasRechargePage = OverseasRechargePage(self.OverseasRechargePageframe)


a = start_gui()
UI.mainloop()
