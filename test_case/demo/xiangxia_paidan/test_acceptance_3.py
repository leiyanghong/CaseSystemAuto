# -*- coding:utf-8 -*-
from time import sleep
import pytest
from config.config import FILE_PATH
from po.case_operate.case_operate_page import case_operate, contains_text_click, case_flow_pop_up_operation, \
    case_flow_pop_up_operation1, application_for_extension
from po.case_report.case_report import case_reported
from po.login.user_login import user_login
from tools.data import random_tool
from tools.report.assert_tool import assert_xpath_text

'''
案件上报-受理-案件立案-派遣(向下派遣)-待处置(申请延期)-督办(延期通过)
'''


def test_CaseReport(driver):
    # 登录-街道管理员PC端案件上报
    user_login("jdadmin", "123456")
    # 案件上报
    case_reported(f"案件描述{random_tool.random_str_abc(10)}", random_tool.random_addr())
    # 受理
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        # 案件操作：受理案件
        case_operate(case_acceptance="受理")
        driver.click("//span[contains(text(),'直接立案')]/preceding-sibling::span/span")
        driver.wait_util_text("//span[contains(text(),'受理并立案')]", "受理并立案")
        contains_text_click("span", "受理并立案", "1")
        driver.wait_util_text("(//p[contains(text(),'立案成功！')])[1]", "立案成功！")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1]", "更多操作")
    # 进入待派遣页面-向下派遣
    contains_text_click("span", "案件派遣", "1")
    driver.wait_util_text("(//span[contains(text(),'待派遣')])[1]", "待派遣")
    contains_text_click("span", "待派遣", "1")
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        # 向下派遣
        case_operate(case_acceptance="向下派遣")
        # 弹框搜索选择向下派遣
        case_flow_pop_up_operation1("div", '部门：', "1", "网格中心")
        # 断言是否派遣成功
        driver.wait_util_text("//p[contains(text(),'操作成功！')]", "操作成功！")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")

    # 登录部门管理员账号
    user_login("leiyanghong", "123456")
    # 进入我的案件-案件处置-待处置
    # 部门处置
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        # 点击处置
        case_operate(case_acceptance="申请延期")
        # 申请延期
        application_for_extension()
        # 断言是否申请延期成功
        driver.wait_util_text("//p[contains(text(),'申请成功！')]", "申请成功！")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")

    # 登录街道管理员账号-督办-延期通过
    user_login("jdadmin", "123456")
    # 进入案件督办-延期
    driver.wait_util_text("(//span[contains(text(),'案件督办')])[1]", "案件督办")
    contains_text_click("span", "案件督办", "1")
    driver.wait_util_text("(//span[contains(text(),'延期')])[1]", "延期")
    contains_text_click("span", "延期", "1")
    # 点击更多操作 案件操作：申请通过
    case_operate(case_acceptance="申请通过")
    contains_text_click("span", "申请通过", "last()")
    driver.wait_util_text("(//p[contains(text(),'处理成功')])[1]", "处理成功")




