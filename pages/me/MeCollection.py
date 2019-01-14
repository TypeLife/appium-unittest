from appium.webdriver.common.mobileby import MobileBy
import re
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeCollectionPage(BasePage):
    """我->收藏页面"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.FavoriteActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
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
                  '文件名': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '100.5KB': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  '测试文件.docx': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '10.0KB': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  'pptx测试文件.pptx': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '34.5KB': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  '测试xls文件.xls': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '20.0KB': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  '[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口': (MobileBy.ID, 'com.chinasofti.rcs:id/favorite_tv_content'),
                  '录制.txt': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '271.0B': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  # 打开位置页面元素
                  "导航按钮": (MobileBy.ID, 'com.chinasofti.rcs:id/location_nativ_btn'),
                  }

    @TestLogger.log()
    def click_nav_btn(self):
        """点击位置页面右下角导航按钮"""
        self.click_element(self.__class__.__locators['导航按钮'])

    def page_up(self):
        """向上滑动"""
        self.swipe_by_percent_on_screen(50, 80, 50, 30, 800)

    def page_down(self):
        """向下滑动"""
        self.swipe_by_percent_on_screen(50, 30, 50, 80, 800)

    def get_all_file_names(self):
        """获取所有收藏的文件名"""
        els = self.get_elements(self.__class__.__locators["文件名"])
        file_names = []
        if els:
            for el in els:
                file_names.append(el.text)
        else:
             return None
        flag = True
        while flag:
            self.page_up()
            els = self.get_elements(self.__class__.__locators["文件名"])
            for el in els:
                if el.text not in file_names:
                    file_names.append(el.text)
                    flag = True
                else:
                    flag = False
        return file_names

    @TestLogger.log()
    def get_file_types(self):
        """获取收藏的文件类型"""
        file_types = []
        file_names = self.get_all_file_names()
        if not file_names:
            return file_types
        for name in file_names:
            res = re.search(r".*(\..*)", name)
            if res:
                type = res.group(1)
                if type not in file_types:
                    file_types.append(type)
        return file_types

    def find_file_by_type(self, locator, file_type, times=10):
        """根据文件类型查找文件"""
        if self._is_element_present(locator):
            els = self.get_elements(locator)
            if els:
                for el in els:
                    if el.text.endswith(file_type):
                        return el
        c = 0
        while c < times:
            self.page_up()
            if self._is_element_present(locator):
                els = self.get_elements(locator)
                if els:
                    for el in els:
                        if el.text.endswith(file_type):
                            return el
            c += 1
        c = 0
        while c < times:
            self.page_down()
            if self._is_element_present(locator):
                els = self.get_elements(locator)
                if els:
                    for el in els:
                        if el.text.endswith(file_type):
                            return el
            c += 1
        return None

    @TestLogger.log()
    def open_file(self, file_type):
        """打开文件"""
        el = self.find_file_by_type((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file_type), file_type)
        if el:
            el.click()
        else:
            raise AssertionError("无此 %s 类型文件" % file_type)

    @TestLogger.log()
    def open_location(self, location):
        """打开位置"""
        locator = (MobileBy.XPATH, "//*[contains(@text, '%s')]" % location)
        if self._is_element_present(locator):
            self.click_element(locator)
        else:
            max_try = 10
            current = 0
            while current < max_try:
                current += 1
                self.page_up()
                if self._is_element_present(locator):
                    self.click_element(locator)
                    return
            max_try = 10
            current = 0
            while current < max_try:
                current += 1
                self.page_down()
                if self._is_element_present(locator):
                    self.click_element(locator)
                    return
            raise AssertionError('没有收藏位置：{}'.format(location))

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        try:
            self.click_element((MobileBy.ID, "com.chinasofti.rcs:id/back"))
        except:
            self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待收藏页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["收藏"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在收藏页面"""
        el = self.get_elements(self.__class__.__locators["收藏"])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def wait_for_open_file(self, timeout=8, auto_accept_alerts=True):
        """等待打开文件页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/menu'))
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def wait_for_location_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待位置页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/location_title'))
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self
