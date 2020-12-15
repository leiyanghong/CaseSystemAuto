from tools.ui.base_ui import BaseUI


# 调用BaseUI封装登录页面模块
class CaseAceptar(BaseUI):
    # 更多操作
    def case_operate(self, xpath):
        self.click(xpath)

    # 动态选择案件分类类型
    def case_accept(self, xpath):
        # 选择案件分类类型
        self.click(xpath)
    def find_element_send_keys(self,xpath,text):
        self.send_keys(xpath,text)

    def find_elements_xpath(self,xpath):
        xpath_list = BaseUI.driver.find_elements_by_xpath(xpath)
        return xpath_list

# 获取多个xpath文本,以列表展示
def get_find_elements_xpath(xpath):
    case_aceptar = CaseAceptar()
    case_aceptar.find_elements_xpath(xpath)

# 更多操作
def case_operate(case_operate="更多操作",case_operate_index="1",case_acceptance="作废",case_acceptance_index="last()"):
    """
    :param case_operate: 更多操作
    :param case_operate_index: 更多操作如果有多个值，可以用索引取指定的值，索引是按1开始索引
    :param case_acceptance: 案件的操作类型
    :param case_acceptance_index: 操作类型如果有多个值，可以用索引取指定的值，索引是按1开始索引
    """
    case_aceptar = CaseAceptar()
    case_aceptar.case_operate(f"(//span[contains(text(),'{case_operate}')])[{case_operate_index}]")
    case_aceptar.case_accept(f"(//li[contains(text(),'{case_acceptance}')])[{case_acceptance_index}]")

def contains_text_click(label,text,index):
    """     封装xpath模糊文本匹配点击
    :param label: xpath传入的标签名
    :param text: 传入的文本名
    :param index: 如果有多个值，可以用索引取指定的值，索引是按1开始索引
    """
    case_aceptar = CaseAceptar()
    case_aceptar.case_operate(f"(//{label}[contains(text(),'{text}')])[{index}]")

def contains_text_sendkeys(label,p_text,index,text):
    """     封装xpath模糊文本匹配输入
    :param label: xpath传入的标签名
    :param text: 传入的文本名
    :param index: 如果有多个值，可以用索引取指定的值，索引是按1开始索引
    """
    case_aceptar = CaseAceptar()
    case_aceptar.find_element_send_keys(f"(//{label}[contains(text(),'{p_text}')])[{index}]",text)

def case_flow_pop_up_operation(label,p_text,index,text):
    """
    封装案件流转的弹框操作
    :param label:xpath传入的标签名
    :param p_text:xpath传入的模糊匹配的文本名
    :param index:如果有多个值，可以用索引取指定的值，索引是按1开始索引
    :param text:传入的文本名
    """
    case_aceptar = CaseAceptar()
    case_aceptar.find_element_send_keys(f"(//{label}[contains(text(),'{p_text}')]/following-sibling::div/div/input)[{index}]", text)
    # case_aceptar.send_keys(f"(//div[contains(text(),'人员：')]/following-sibling::div/div/input)[1]", "雷阳洪")
    case_aceptar.click('(//i[@class="el-icon-search"])[last()]')
    case_aceptar.click('//div[@class="el-table__fixed-body-wrapper"]/table/tbody/tr[1]/td[1]/div/label/span[1]/span')
    contains_text_click("span", "确 定", "last()")
    contains_text_click("span", "确 定", "last()")

def case_flow_pop_up_operation1(label,p_text,index,text):
    """
    封装案件流转的弹框操作
    :param label:xpath传入的标签名
    :param p_text:xpath传入的模糊匹配的文本名
    :param index:如果有多个值，可以用索引取指定的值，索引是按1开始索引
    :param text:传入的文本名
    """

    case_aceptar = CaseAceptar()
    case_aceptar.find_element_send_keys(f"(//{label}[contains(text(),'{p_text}')]/following-sibling::div/div/input)[{index}]", text)
    # case_aceptar.send_keys(f"(//div[contains(text(),'人员：')]/following-sibling::div/div/input)[1]", "雷阳洪")
    case_aceptar.click('(//i[@class="el-icon-search"])[last()]')
    case_aceptar.click('//div[@class="el-table__fixed-body-wrapper"]/table/tbody/tr[1]/td[1]/div/label/span[1]/span')
    contains_text_click("span", "确 定", "last()")

# 申请延期弹框操作
def application_for_extension():
    case_aceptar = CaseAceptar()
    case_aceptar.click("//div[contains(text(),'延期原因：')]/following-sibling::div/div/div/input")
    case_aceptar.click('((//ul[@class="el-scrollbar__view el-select-dropdown__list"])[last()]/li)[1]')
    case_aceptar.click("//div[contains(text(),'申请天数：')]/following-sibling::div/div/div/input")
    case_aceptar.click('((//ul[@class="el-scrollbar__view el-select-dropdown__list"])[last()]/li)[1]')
    contains_text_click("span", "确 定", "last()")

