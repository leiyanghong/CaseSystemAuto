# -*- coding:utf-8 -*-
from time import sleep
import pytest
from config.config import FILE_PATH
from po.case_operate.case_operate_page import case_operate, contains_text_click, case_flow_pop_up_operation
from po.case_report.case_report import case_reported
from po.login.user_login import user_login
from tools.data import random_tool
from tools.report.assert_tool import assert_xpath_text

'''
案件上报-受理-案件立案-派遣(指派处置人)-处置人处置-待核查(指定核查人)-审核(审核通过)-结案
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
        contains_text_click("span", "确定", "1")
        driver.wait_util_text("(//p[contains(text(),'受理成功！')])[1]", "受理成功！")
    else:
        # 案件上报
        case_reported(f"案件描述{random_tool.random_str_abc(10)}", random_tool.random_addr())
        # 案件操作：受理案件
        case_operate(case_acceptance="受理")
        contains_text_click("span", "确定", "1")
        driver.wait_util_text("(//p[contains(text(),'受理成功！')])[1]", "受理成功！")
    # 立案
    driver.wait_util_text("(//span[contains(text(),'案件立案')])[1]", "案件立案")
    contains_text_click("span", "案件立案", "1")
    driver.wait_util_text("(//span[contains(text(),'待立案')])[1]", "待立案")
    contains_text_click("span", "待立案", "1")
    try:
        if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
            # 案件操作：受理案件
            case_operate(case_acceptance="立案")
            contains_text_click("span", "立案", "last()")
            contains_text_click("span", "确 定", "last()")
            driver.wait_util_text("(//p[contains(text(),'立案成功！')])[1]", "立案成功！")
        else:
            driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")
    except Exception as e:
        print("没有可立案的案件，请受理后再立案")
        raise e
    # 进入待派遣页面-指派处置人
    contains_text_click("span", "案件派遣", "1")
    driver.wait_util_text("(//span[contains(text(),'待派遣')])[1]", "待派遣")
    contains_text_click("span", "待派遣", "1")
    try:
        if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
            # 指派处置人
            case_operate(case_acceptance="指派处置人")
            # 弹框搜索选择指派处置人
            case_flow_pop_up_operation("div", '人员：', "1", "雷阳洪")
            # 断言是否指派成功
            driver.wait_util_text("//p[contains(text(),'指派成功!')]", "指派成功!")
        else:
            driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")
    except Exception as e:
        print("没有可派遣的案件，请立案后再派遣")
        raise e

    # 登录部门管理员账号
    user_login("leiyanghong", "123456")
    # 进入我的案件-处置列表-处置
    driver.wait_util_text('//*[@id="app"]/section/div/div[2]/div/ul/li[2]/div/span', "我的案件")
    # contains_text_click("span", "我的案件", "1")
    driver.click('//*[@id="app"]/section/div/div[2]/div/ul/li[2]/div/span')
    driver.wait_util_text("(//span[contains(text(),'处置列表')])[1]", "处置列表")
    contains_text_click("span", "处置列表", "1")
    # 处置
    try:
        if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
            # 点击处置
            case_operate(case_acceptance="处置")
            # 上传案件现场照片
            driver.file_upload("(//div[contains(text(),'案件现场')])[1]/following-sibling::div/div/div/div/i", FILE_PATH)
            sleep(1)
            # 上传处置结果
            driver.file_upload("(//div[contains(text(),'处置结果')])[1]/following-sibling::div/div/div/div/i", FILE_PATH)
            # 完成处置
            driver.click(
                "//button[@class='el-button el-tooltip case-el-btn el-button--primary el-button--small']/span[contains(text(),'完成处置')]")
        else:
            driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")
    except Exception as e:
        print("没有可处置的案件，请重新派遣")
        raise e

    # 登录街道管理员账号-案件核查
    user_login("jdadmin", "123456")
    # 进入案件核查-待核查页面
    contains_text_click("span", "案件核查", "1")
    driver.wait_util_text("(//span[contains(text(),'案件核查')])[1]", "案件核查")
    contains_text_click("span", "待核查", "1")
    # 点击更多操作
    case_operate(case_acceptance="指定核查人")
    # 案件操作：指定核查人
    driver.clear_send_keys("(//div[contains(text(),'人员：')]/following-sibling::div/div/input)[1]", "雷阳洪")
    driver.click('(//i[@class="el-icon-search"])[last()]')
    driver.click('//div[@class="el-table__fixed-body-wrapper"]/table/tbody/tr[1]/td[1]/div/label/span[1]/span')
    contains_text_click("span", "确 定", "last()")
    driver.click("//div[contains(text(),'责任部门')]/following-sibling::div/div/div/input")
    contains_text_click("span", "网格中心", "last()")
    contains_text_click("span", "确 定", "last()")
    driver.wait_util_text("(//p[contains(text(),'指定核查人成功！')])[1]", "指定核查人成功！")

    # 登录部门管理员审核
    user_login("leiyanghong", "123456")
    # 进入我的案件-核查列表-处置
    contains_text_click("span", "我的案件", "1")
    driver.wait_util_text("(//span[contains(text(),'核查列表')])[1]", "核查列表")
    contains_text_click("span", "核查列表", "1")
    # 点击更多操作
    case_operate(case_acceptance="审核")
    driver.wait_util_text("(//span[contains(text(),'审核通过')])[1]", "审核通过")
    contains_text_click("span", "审核通过", "1")
    # 上传案件现场照片
    driver.file_upload("//div[contains(text(),'核查图片')]/following-sibling::div/div/div/button", FILE_PATH)
    sleep(1)
    contains_text_click("span", "确定", "last()")
    driver.wait_util_text("(//p[contains(text(),'审核已通过')])[1]", "审核已通过")

    # 登录街道管理员结案
    user_login("jdadmin", "123456")
    # 进入案件结案-待结案
    driver.wait_util_text("(//span[contains(text(),'案件结案')])[1]", "案件结案")
    contains_text_click("span", "案件结案", "1")
    driver.wait_util_text("(//span[contains(text(),'待结案')])[1]", "待结案")
    contains_text_click("span", "待结案", "1")
    case_number = driver.get_text("(//span[contains(text(),'案件编号')])[2]/span")
    # 点击更多操作
    case_operate(case_acceptance="结案")
    driver.wait_util_text("(//span[contains(text(),'结案')])[last()]", "结案")
    # 结案
    contains_text_click("span", "结案", 'last()')
    contains_text_click("span", "确定", '1')
    # 进入案件结案-已结案
    driver.wait_util_text("(//span[contains(text(),'已结案')])[1]", "已结案")
    contains_text_click("span", "已结案", "1")
    print("进入已结案页面")
    # 获取案件编号列表
    case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
    print(f"获取案件编号:{case_number_list}")
    # 断言 是否结案成功
    assert True == assert_xpath_text(case_number_list, case_number)
    print("断言成功")
