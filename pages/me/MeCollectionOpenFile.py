from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeCollectionOpenFilePage(BasePage):
    """我收藏打开文件页面"""
    ACTIVITY = 'com.cmicc.module_office.WordActivity'

    __locators = {'': (MobileBy.ID, ''),
 'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
 'android:id/content': (MobileBy.ID, 'android:id/content'),
 'com.chinasofti.rcs:id/toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar'),
 '测试文件.docx': (MobileBy.ID, ''),
 'com.chinasofti.rcs:id/container_base': (MobileBy.ID, 'com.chinasofti.rcs:id/container_base'),
 'com.chinasofti.rcs:id/container': (MobileBy.ID, 'com.chinasofti.rcs:id/container')
}
