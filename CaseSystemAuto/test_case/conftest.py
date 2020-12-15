# -*- coding:utf-8 -*-

import pytest
from tools.ui.base_ui import BaseUI

@pytest.fixture(scope='session')
def driver():
    base = BaseUI()  # 实例初始化baseui
    base.start_browser("chrome")
    # base.start_browser("chrome_debugger")  # 启动谷歌浏览器驱动
    yield base  # yield关键字 会优先执行上面的代码，然后执行case，最后执行yield下面的代码
    base.driver.quit()  # 关闭浏览器驱动