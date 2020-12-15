#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config import config
from tools.ui.base_ui import BaseUI


# 调用BaseUI封装登录页面模块
class LoginPage(BaseUI):
    # 登录页面网址
    url = config.PAIDAN_URL+"/web/#/login"
    # 用户名输入框
    p_username = "//label[contains(text(),'账号')]/../div/div/input"
    # 密码输入框
    p_password = "//label[contains(text(),'密码')]/../div/div/input"
    # 登录按钮
    p_login = '//button/span'

    # 打开url
    def m_open(self):
        self.get(self.url)

    # 输入用户名
    def m_username(self, username):
        self.send_keys(self.p_username, username)

    # 输入密码
    def m_password(self, password):
        self.send_keys(self.p_password, password)

    # 点击登录按钮
    def m_login(self):
        self.click(self.p_login)

