from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeCollectionOpenAddrPage(BasePage):
    """我打开位置页面"""
    ACTIVITY = 'com.cmicc.module_message.ui.activity.GDLocationActvity'

    __locators = {'': (MobileBy.ID, ''),
 'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
 'android:id/content': (MobileBy.ID, 'android:id/content'),
 'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
 'com.chinasofti.rcs:id/location_back_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/location_back_btn'),
 '位置': (MobileBy.ID, 'com.chinasofti.rcs:id/location_title'),
 'com.chinasofti.rcs:id/gd_map_view': (MobileBy.ID, 'com.chinasofti.rcs:id/gd_map_view'),
 '广东省深圳市龙岗区居里夫人大道与环城路交叉口': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_map_title'),
 'com.chinasofti.rcs:id/location_nativ_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/location_nativ_btn')
}
