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
案件上报-受理(指定核实人)-核实通过-退回发现
'''


def test_heshitongguo(driver):
    # 登录-街道管理员PC端案件上报
    user_login("jdadmin", "123456")
    # 案件上报
    case_reported(f"案件描述{random_tool.random_str_abc(10)}", random_tool.random_addr())
    # 受理
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        global case_number
        # 获取案件编号
        case_number = driver.get_text("(//span[contains(text(),'案件编号')])[2]/span")
        # 案件操作：指定核实人
        case_operate(case_acceptance="指定核实人")
        case_flow_pop_up_operation("div", '人员：', "1", "雷阳洪")
        driver.wait_util_text("(//p[contains(text(),'指定核实人成功')])[1]", "指定核实人成功")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1]", "更多操作")

    # 登录-部门管理员核实案件
    user_login("leiyanghong", "123456")
    # 进入我的案件-核实列表
    driver.wait_util_text('//*[@id="app"]/section/div/div[2]/div/ul/li[2]/div/span', "我的案件")
    driver.click('//*[@id="app"]/section/div/div[2]/div/ul/li[2]/div/span')
    driver.wait_util_text("(//span[contains(text(),'核实列表')])[1]", "核实列表")
    contains_text_click("span", "核实列表", "1")
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        global case_number_list
        # 获取核实列表页面的所有案件编号
        case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1]", "更多操作")
    # 审核通过
    if assert_xpath_text(case_number_list, case_number):
        # 案件操作：核实通过-退回发现
        case_operate(case_acceptance="核实")
        driver.wait_util_text("(//span[contains(text(),'核实通过')])[1]", "核实通过")
        contains_text_click("span", "核实通过", "1")
        contains_text_click("span", "确定", "1")
        driver.wait_util_text("(//p[contains(text(),'操作成功！')])[1]", "操作成功！")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1]", "更多操作")

    # 登录街道管理员验证核实通过的案件是否退回到发现列表
    user_login("jdadmin", "123456")
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        # 获取核实列表页面的所有案件编号
        case_number_list1 = driver.get_texts("//span[contains(text(),'案件编号')]/span")
        # 断言 核实通过的案件编号是否成功流转至发现页面
        assert True == assert_xpath_text(case_number_list1, case_number)
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")


'''
案件上报-受理(指定核实人)-核实不通过-退回发现
'''


def test_heshibutongguo(driver):
    # 登录-街道管理员PC端案件上报
    user_login("jdadmin", "123456")
    # 案件上报
    case_reported(f"案件描述{random_tool.random_str_abc(10)}", random_tool.random_addr())
    # 受理
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        global case_number
        # 获取案件编号
        case_number = driver.get_text("(//span[contains(text(),'案件编号')])[2]/span")
        # 案件操作：指定核实人
        case_operate(case_acceptance="指定核实人")
        case_flow_pop_up_operation("div", '人员：', "1", "雷阳洪")
        driver.wait_util_text("(//p[contains(text(),'指定核实人成功')])[1]", "指定核实人成功")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1]", "更多操作")

    # 登录-部门管理员核实案件
    user_login("leiyanghong", "123456")
    # 进入我的案件-核实列表
    driver.wait_util_text('//*[@id="app"]/section/div/div[2]/div/ul/li[2]/div/span', "我的案件")
    driver.click('//*[@id="app"]/section/div/div[2]/div/ul/li[2]/div/span')
    driver.wait_util_text("(//span[contains(text(),'核实列表')])[1]", "核实列表")
    contains_text_click("span", "核实列表", "1")
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        global case_number_list
        # 获取核实列表页面的所有案件编号
        case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1]", "更多操作")
    # 审核不通过
    if assert_xpath_text(case_number_list, case_number):
        # 案件操作：核实不通过-退回发现
        case_operate(case_acceptance="核实")
        driver.wait_util_text("(//span[contains(text(),'核实不通过')])[1]", "核实不通过")
        contains_text_click("span", "核实不通过", "1")
        contains_text_click("span", "确定", "1")
        driver.wait_util_text("(//p[contains(text(),'操作成功！')])[1]", "操作成功！")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1]", "更多操作")

    # 登录街道管理员验证核实不通过的案件是否退回到发现列表
    user_login("jdadmin", "123456")
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        # 获取核实列表页面的所有案件编号
        case_number_list1 = driver.get_texts("//span[contains(text(),'案件编号')]/span")
        # 断言 核实不通过的案件编号是否成功流转至发现页面
        assert True == assert_xpath_text(case_number_list1, case_number)
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")
