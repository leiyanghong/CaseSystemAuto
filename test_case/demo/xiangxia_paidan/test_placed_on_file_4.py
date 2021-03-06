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
案件上报-受理-案件立案-派遣(向下派遣)-待处置(申请退单)-督办(退单通过)-再派遣(指派处置人)
'''


def test_tuidan(driver):
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
    # 申请退单
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        # 点击 申请退单
        case_operate(case_acceptance="申请退单")
        contains_text_click("span", "确 定", "last()")
        # 断言是否申请退单成功
        driver.wait_util_text("//p[contains(text(),'申请成功！')]", "申请成功！")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")

    # 登录街道管理员账号-督办-退单通过
    user_login("jdadmin", "123456")
    # 进入案件督办-退单
    driver.wait_util_text("(//span[contains(text(),'案件督办')])[1]", "案件督办")
    contains_text_click("span", "案件督办", "1")
    driver.wait_util_text("(//span[contains(text(),'退单')])[1]", "退单")
    contains_text_click("span", "退单", "1")
    # 点击更多操作 案件操作：退单通过
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        case_operate(case_acceptance="申请通过")
        contains_text_click("span", "确 定", "last()")
        driver.wait_util_text("(//p[contains(text(),'处理成功')])[1]", "处理成功")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")


'''
案件上报-受理-案件立案-派遣(向下派遣)-管控(收回重派)-再派遣(向上派遣)
'''


def test_zaipaiqian_xiangshangpaiqian(driver):
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

    # 街道管理员-管控(收回重派)
    # 进入待派遣页面-向上派遣
    driver.wait_util_text("(//span[contains(text(),'管控')])[1]", "管控")
    contains_text_click("span", "管控", "1")
    # 获取管控页面的所有案件编号
    case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        global case_number
        # 获取管控模块的案件编号
        case_number = driver.get_text("(//span[contains(text(),'案件编号')])[2]/span")
        # 管控-收回重派
        case_operate(case_acceptance="收回重派")
        contains_text_click("span", "确 定", "last()")
        # 断言是否收回成功
        driver.wait_util_text("//p[contains(text(),'处理成功！')]", "处理成功！")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")
    # 进入再派遣页面
    driver.wait_util_text("(//span[contains(text(),'再派遣')])", "再派遣")
    driver.click("(//span[contains(text(),'再派遣')])")
    case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
    # 断言 收回的案件编号是否成功流转至再派遣页面
    assert True == assert_xpath_text(case_number_list, case_number)
    # 向上派遣
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        case_operate(case_acceptance="向上派遣")
        contains_text_click("span", "确 定", "last()")
        # 断言是否派遣成功
        driver.wait_util_text("//p[contains(text(),'操作成功！')]", "操作成功！")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")

    # 登录区级管理员账号
    user_login("qjadmin", "123456")
    driver.wait_util_text("(//span[contains(text(),'案件派遣')])", "案件派遣")
    # 进入待派遣页面-验证是否流转至再派遣页面
    contains_text_click("span", "案件派遣", "1")
    driver.wait_util_text("(//span[contains(text(),'待派遣')])[1]", "待派遣")
    contains_text_click("span", "再派遣", "1")
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        case_number_list2 = driver.get_texts("//span[contains(text(),'案件编号')]/span")
        # 断言 验证案件编号是否成功流转至待派遣页面
        assert True == assert_xpath_text(case_number_list2, case_number)
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")