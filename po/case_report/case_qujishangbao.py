#!/usr/bin/env python
# -*- coding:utf-8 -*-
from time import sleep

from config import config
from tools.ui.base_ui import BaseUI


# 调用BaseUI封装案件上报页面模块 区级管理员上报案件
class QuJiShangBao(BaseUI):
    # 案件上报
    p_case_report = "//span[contains(text(),'案件上报')]"
    # 案件分类 类型
    p_case_fenlei1 = "//label[contains(text(),'案件分类')]/../div/div/div/input"
    p_case_fenlei2 = "//span[contains(text(),'事件 / 青东五镇专项整治 / 废弃车辆')]"
    p_case_fenlei3 = "//span[contains(text(),'市容环卫')]"
    p_case_fenlei4 = "//span[contains(text(),'废弃车辆')]"
    # 案件名称
    p_case_name1 = "//label[contains(text(),'案件名称')]/../div/div/div/input"
    p_case_name2 = '((//ul[@class="el-scrollbar__view el-select-dropdown__list"])[last()]/li/span)[1]'
    # 案件描述
    p_case_miaoshu = "//label[contains(text(),'案件描述')]/../div/div/textarea"
    # 案件来源
    p_case_source1 = "//label[contains(text(),'案件来源')]/../div/div/div/input"
    p_case_source2 = '((//ul[@class="el-scrollbar__view el-select-dropdown__list"])[last()]/li/span)[1]'

    # 街镇
    p_jiezhen1 = "//label[contains(text(),'街镇')]/../div/div/div/input"
    p_jiezhen2 = '((//ul[@class="el-scrollbar__view el-select-dropdown__list"])[last()]/li/span)[1]'

    # 所属网格
    p_wangge1 = "//label[contains(text(),'所属网格')]/../div/div/div/input"
    p_wangge2 = '(((//div[@class="el-select-dropdown__wrap el-scrollbar__wrap"])[last()]/ul/ul)[1]/li[2]/ul/li/span)[1]'

    # 详细地址
    p_dizhi = "//label[contains(text(),'详细地址')]/../div/div/input"
    # 上报
    p_shangbao = '(//button[@class="el-button el-button--primary el-button--small"])[last()]/span'
    # 确定
    p_queding = "//span[contains(text(),'确 定')]"
    # 断言上报案件是否成功
    p_case_assert = '//p[contains(text(),"案件上报成功！您是否继续上报下一个案件？")]'
    p_case_assert_text = '案件上报成功！您是否继续上报下一个案件？'
    # 是否重复上报
    p_repeat_report = "//span[contains(text(),'否')]"

    # 案件上报
    def case_report(self):
        self.click(self.p_case_report)

    # 选择案件分类
    def case_fenlei(self):
        # 选择案件分类类型
        self.send_keys(self.p_case_fenlei1,"废弃车辆")
        self.click(self.p_case_fenlei2)

    # 选择案件名称
    def case_name(self, ):
        self.click(self.p_case_name1)
        self.click(self.p_case_name2)

    # 输入案件描述
    def case_miaoshu(self, case_miaoshu):
        self.send_keys(self.p_case_miaoshu, case_miaoshu)

    # 选择案件来源
    def case_source(self):
        self.click(self.p_case_source1)
        self.click(self.p_case_source2)

    # 选择街镇
    def jiezhen(self):
        self.click(self.p_jiezhen1)
        self.click(self.p_jiezhen2)

    # 选择所属网格
    def case_gridding(self):
        self.click(self.p_wangge1)
        self.click(self.p_wangge2)

    # 输入地址
    def case_dizhi(self, dizhi):
        self.send_keys(self.p_dizhi, dizhi)

    # 点击上报
    def case_shangbao(self):
        self.click(self.p_shangbao)

    # 点击确定
    def case_queding(self):
        self.click(self.p_queding)

    # 断言是否上报成功
    def case_shangbao_assert(self):
        self.wait_util_text(self.p_case_assert, self.p_case_assert_text)

    # 是否重复上报
    def case_repeat_report(self):
        self.click(self.p_repeat_report)

# 区级案件上报
def case_qujishangbao(miaoshu, dizhi):
    casereport = QuJiShangBao()
    casereport.case_report()
    casereport.case_fenlei()
    casereport.case_name()
    casereport.case_miaoshu(miaoshu)
    casereport.case_source()
    casereport.jiezhen()
    casereport.case_gridding()
    casereport.case_dizhi(dizhi)
    casereport.case_shangbao()
    casereport.case_queding()
    casereport.case_repeat_report()