from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeCollectionPage(BasePage):
    """我->收藏页面"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.FavoriteActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  '收藏': (MobileBy.ID, 'com.chinasofti.rcs:id/favorite_title'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  '容器列表': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_favorite'),
                  'com.chinasofti.rcs:id/swipe_content': (MobileBy.ID, 'com.chinasofti.rcs:id/swipe_content'),
                  'com.chinasofti.rcs:id/favorite_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/favorite_layout'),
                  'com.chinasofti.rcs:id/tv_head': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_head'),
                  '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
                  '今天': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'www.baidu.com': (MobileBy.ID, 'com.chinasofti.rcs:id/favorite_tv'),
                  'com.chinasofti.rcs:id/favorite_content': (MobileBy.ID, 'com.chinasofti.rcs:id/favorite_content'),
                  'com.chinasofti.rcs:id/favorite_image_shortcut': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/favorite_image_shortcut'),
                  'com.chinasofti.rcs:id/favorite_file_name_size': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/favorite_file_name_size'),
                  'ppt测试文件.ppt': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '100.5KB': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  '测试文件.docx': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '10.0KB': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  'pptx测试文件.pptx': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '34.5KB': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  '测试xls文件.xls': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '20.0KB': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  '[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口': (MobileBy.ID, 'com.chinasofti.rcs:id/favorite_tv_content'),
                  '录制.txt': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '271.0B': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size')
                  }

    def page_up(self):
        """向上滑动"""
        self.swipe_by_direction(self.__locators['容器列表'], 'up')

    def page_dowm(self):
        """向下滑动"""
        self.swipe_by_direction(self.__locators['容器列表'], 'down')

    # el = dr.find_element(MobileBy.XPATH, "//*[contains(@text, '.ppt')]")
    # 打开文件返回
    # el = dr.find_element(MobileBy.XPATH, "//*[@content-desc='返回']")
    # 打开位置返回
    # el = dr.find_element(MobileBy.ID, "com.chinasofti.rcs:id/left_back")