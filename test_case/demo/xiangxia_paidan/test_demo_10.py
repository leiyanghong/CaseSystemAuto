# -*- coding:utf-8 -*-
from time import sleep
import pytest
from config.config import FILE_PATH
from po.case_operate.case_operate_page import case_operate, contains_text_click, case_flow_pop_up_operation, \
    case_flow_pop_up_operation1, application_for_extension
from po.case_report.case_qujishangbao import case_qujishangbao
from po.case_report.case_report import case_reported
from po.login.user_login import user_login
from tools.data import random_tool
from tools.report.assert_tool import assert_xpath_text

'''
街道向上派遣到区>区派遣给指定处置人处置
(街道)案件上报-受理-案件立案-派遣(向上派遣)-(区)待派遣-(区)指派处置人
'''


def test_xiangshangpaiqian(driver):
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
    # 进入待派遣页面-向上派遣
    contains_text_click("span", "案件派遣", "1")
    driver.wait_util_text("(//span[contains(text(),'待派遣')])[1]", "待派遣")
    contains_text_click("span", "待派遣", "1")
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        global case_number
        # 获取案件编号
        case_number = driver.get_text("(//span[contains(text(),'案件编号')])[2]/span")
        # 向上派遣
        case_operate(case_acceptance="向上派遣")
        contains_text_click("span", "确 定", "last()")
        # 断言是否派遣成功
        driver.wait_util_text("//p[contains(text(),'操作成功！')]", "操作成功！")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")

    # 登录区级管理员账号
    user_login("qjadmin", "123456")
    driver.wait_util_text("(//span[contains(text(),'案件派遣')])", "案件派遣")
    # 进入待派遣页面-指派处置人
    contains_text_click("span", "案件派遣", "1")
    driver.wait_util_text("(//span[contains(text(),'待派遣')])[1]", "待派遣")
    contains_text_click("span", "待派遣", "1")
    case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
    if assert_xpath_text(case_number_list, case_number):
        # 弹框搜索区部门管理员
        case_operate(case_acceptance="指派处置人")
        case_flow_pop_up_operation("div", '人员：', "1", "区部门管理员")
        driver.wait_util_text("(//p[contains(text(),'指派成功!')])[1]", "指派成功!")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")

    # 登录区部门账号
    user_login("qubumen_leiyh", "123456")
    # 进入我的案件-处置列表-处置
    driver.wait_util_text('//*[@id="app"]/section/div/div[2]/div/ul/li[2]/div/span', "我的案件")
    driver.click('//*[@id="app"]/section/div/div[2]/div/ul/li[2]/div/span')
    driver.wait_util_text("(//span[contains(text(),'处置列表')])[1]", "处置列表")
    contains_text_click("span", "处置列表", "1")
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        # 获取处置列表页面的所有案件编号
        case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
        # 断言 核实通过的案件编号是否成功流转至发现页面
        assert True == assert_xpath_text(case_number_list, case_number)
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")


'''
向下派遣(区>街道)-街道申请退单-区督办审批
'''


def test_qudubanshenpi(driver):
    # 登录-区级管理员PC端案件上报
    user_login("qjadmin", "123456")
    # 案件上报
    case_qujishangbao("案件描述", random_tool.random_addr())
    # 受理
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        global case_number
        case_number = driver.get_text("(//span[contains(text(),'案件编号')])[2]/span")
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
        # 案件操作：向下派遣 向街镇派遣
        case_operate(case_acceptance="向下派遣")
        driver.click("(//span[contains(text(),'指派下级：')]/../following-sibling::div)[2]/label/span/span")
        driver.send_keys("//div[contains(text(),'街镇：')]/following-sibling::div/div/input", "夏阳街道")
        driver.click('(//i[@class="el-icon-search"])[last()]')
        driver.click('//div[@class="el-table__fixed-body-wrapper"]/table/tbody/tr[1]/td[1]/div/label/span[1]/span')
        contains_text_click("span", "确 定", "last()")
        driver.wait_util_text("(//p[contains(text(),'操作成功！')])[1]", "操作成功！")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1]", "更多操作")

    # 登录-街道管理员申请退单
    user_login("jdadmin", "123456")
    # 进入待派遣页面-向下派遣
    contains_text_click("span", "案件派遣", "1")
    driver.wait_util_text("(//span[contains(text(),'待派遣')])[1]", "待派遣")
    contains_text_click("span", "待派遣", "1")
    # 街道申请退单
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        # 获取列表页面的所有案件编号
        case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
        # 断言 核实区级下派的案件是否成功流转至街道管理的待派遣页面
        assert True == assert_xpath_text(case_number_list, case_number)
        # 案件操作：申请退单
        case_operate(case_acceptance="申请退单")
        contains_text_click("span", "确 定", "last()")
        driver.wait_util_text("(//p[contains(text(),'操作成功！')])[1]", "操作成功！")

    # 登录-区级管理员PC端案件上报
    user_login("qjadmin", "123456")
    # 进入案件督办-退单
    driver.wait_util_text("(//span[contains(text(),'案件督办')])[1]", "案件督办")
    contains_text_click("span", "案件督办", "1")
    driver.wait_util_text("(//span[contains(text(),'退单')])[1]", "退单")
    contains_text_click("span", "退单", "1")
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        # 获取退单列表页面的所有案件编号
        case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
        # 点击更多操作 案件操作：退单通过
        if assert_xpath_text(case_number_list, case_number):
            case_operate(case_acceptance="申请通过")
            contains_text_click("span", "确 定", "last()")
            driver.wait_util_text("(//p[contains(text(),'处理成功')])[1]", "处理成功")
        else:
            driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1] ", "更多操作")
    # 进入再派遣页面
    contains_text_click("span", "案件派遣", "1")
    driver.wait_util_text("(//span[contains(text(),'再派遣')])", "再派遣")
    driver.click("(//span[contains(text(),'再派遣')])")
    case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
    # 断言 收回的案件编号是否成功流转至再派遣页面
    assert True == assert_xpath_text(case_number_list, case_number)


'''
区向下派遣至区部门>收回到区重新派遣
'''
def test_qujichongpai(driver):
    # 登录-街道管理员PC端案件上报
    user_login("qjadmin", "123456")
    # 案件上报
    case_qujishangbao("案件描述", random_tool.random_addr())
    # 受理
    if driver.is_element_exist("(//span[contains(text(),'更多操作')])[1] "):
        global case_number
        case_number = driver.get_text("(//span[contains(text(),'案件编号')])[2]/span")
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
        # 案件操作：向下派遣 向街镇派遣
        case_operate(case_acceptance="向下派遣")
        # driver.click("(//span[contains(text(),'指派下级：')]/../following-sibling::div)[1]/label/span/span")
        driver.send_keys("//div[contains(text(),'部门：')]/following-sibling::div/div/input", "区网格中心")
        driver.click('(//i[@class="el-icon-search"])[last()]')
        driver.click('//div[@class="el-table__fixed-body-wrapper"]/table/tbody/tr[1]/td[1]/div/label/span[1]/span')
        contains_text_click("span", "确 定", "last()")
        driver.wait_util_text("(//p[contains(text(),'操作成功！')])[1]", "操作成功！")
    else:
        driver.wait_util_text("(//span[contains(text(),'更多操作')])[1]", "更多操作")

    # 管控(收回重派)
    driver.wait_util_text("(//span[contains(text(),'管控')])[1]", "管控")
    contains_text_click("span", "管控", "1")
    # 获取管控页面的所有案件编号
    case_number_list = driver.get_texts("//span[contains(text(),'案件编号')]/span")
    if assert_xpath_text(case_number_list, case_number):
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
    case_number_list1 = driver.get_texts("//span[contains(text(),'案件编号')]/span")
    # 断言 收回的案件编号是否成功流转至再派遣页面
    assert True == assert_xpath_text(case_number_list1, case_number)

