#!/usr/bin/env python
# -*- coding:utf-8 -*-
from po.case_report.cas_report_page import CaseReport


def case_reported(miaoshu, dizhi):
    casereport = CaseReport()
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
