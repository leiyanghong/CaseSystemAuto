#!/usr/bin/env python
# -*- coding:utf-8 -*-
from po.login.login_page import LoginPage



def user_login(username,passowrd):
    login = LoginPage()
    login.m_open()
    login.m_username(username)
    login.m_password(passowrd)
    login.m_login()