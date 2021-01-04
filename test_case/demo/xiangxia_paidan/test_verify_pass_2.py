# -*- coding:utf-8 -*-
from time import sleep
import pytest
from config.config import FILE_PATH
from po.case_operate.case_operate_page import case_operate, contains_text_click, case_flow_pop_up_operation, \
    case_flow_pop_up_operation1
from po.case_report.case_report import case_reported
from po.login.user_login import user_login
from tools.data import random_tool
from tools.report.assert_tool import assert_xpath_text

'''
案件上报-受理-案件立案-派遣(向下派遣)-处置(部门处置)-待核查(指定核查人)-审核(审核通过)-结案
'''


def test_CaseReport(driver):
    # 登录-街道管理员PC端案件上报
    user_login("jdadmin", "1234567")
    # 案件上报
    case_reported(f"案件描述{random_tool.random_str_abc(10)}", random_tool.random_addr())
    case_number = driver.get_text("(//span[contains(text(),'案件编号')])[2]/span")
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
        case_operate(case_acceptance="部门处置")
        # 上传案件现场照片
        driver.file_upload("(//div[contains(text(),'案件现场')])[1]/following-sibling::div/div/div/div/i", FILE_PATH)
        sleep(1)
        # 上传处置结果
        driver.file_upload("(//div[contains(text(),'处置结果')])[1]/following-sibling::div/div/div/div/i", FILE_PATH)
        sleep(1)
        # 完成处置
        driver.click(
            "//button[@class='el-button el-tooltip case-el-btn el-button--primary el-button--small']/span[contains(text(),'完成处置')]")
        driver.wait_util_text("(//p[contains(text(),'处置成功')])[1]", "处置成功")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")

    # 登录街道管理员账号-案件核查
    user_login("jdadmin", "123456")
    # 进入案件核查-待核查页面
    contains_text_click("span", "案件核查", "1")
    driver.wait_util_text("(//span[contains(text(),'案件核查')])[1]", "案件核查")
    contains_text_click("span", "待核查", "1")
    # 点击更多操作 案件操作：跳过核查
    case_operate(case_acceptance="跳过核查")
    contains_text_click("span", "确 定", "last()")
    driver.wait_util_text("(//p[contains(text(),'操作成功！')])[1]", "操作成功！")

    # 登录街道管理员结案
    user_login("jdadmin", "123456")
    # 进入案件结案-待结案
    driver.wait_util_text("(//span[contains(text(),'案件结案')])[1]", "案件结案")
    contains_text_click("span", "案件结案", "1")
    driver.wait_util_text("(//span[contains(text(),'待结案')])[1]", "待结案")
    contains_text_click("span", "待结案", "1")
    # 点击更多操作
    case_operate(case_acceptance="结案")
    driver.wait_util_text("(//span[contains(text(),'结案')])[last()]", "结案")
    # 结案
    contains_text_click("span", "结案", 'last()')
    contains_text_click("span", "确定", '1')
    # 进入案件结案-已结案
    driver.wait_util_text("(//span[contains(text(),'已结案')])[1]", "已结案")
    contains_text_click("span", "已结案", "1")
    driver.click('//*[@id="app"]/section/div/div[2]/div/ul/li[1]/ul/li[5]/ul/li[2]/span')
    # 获取案件编号列表
    case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
    print(f"获取案件编号:{case_number_list}")
    # 断言 是否结案成功
    assert True == assert_xpath_text(case_number_list, case_number)


