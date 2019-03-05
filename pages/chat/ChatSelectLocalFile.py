import os
import time

from appium.webdriver.common.mobileby import MobileBy

import settings
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatSelectLocalFilePage(BasePage):
    """选择本地文件页面聊天"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ChooseLocalFileActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  'SD卡内存': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  '列表容器': (MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'),
                  'com.chinasofti.rcs:id/lv_choose': (MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'),
                  'com.chinasofti.rcs:id/rl_sd_file': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_sd_file'),
                  'com.chinasofti.rcs:id/iv_icon_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_icon_layout'),
                  'com.chinasofti.rcs:id/iv_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_icon'),
                  'sogou': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  'Xiaomi': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '2018-11-09 11-06-18-722582.log': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '410.0B': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '10:18': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_create_time'),
                  'com.chinasofti.rcs:id/cb_choose_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/cb_choose_icon'),
                  'ReleaseChannel.txt': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '14.0B': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '11-09 10:07': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_create_time'),
                  'test_video.mp4': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '2.2M': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '文件大小': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '选择文件大小': (MobileBy.XPATH, "//android.widget.CheckBox[@checked='true']/preceding-sibling::android.widget.RelativeLayout/*[@resource-id='com.chinasofti.rcs:id/textview_file_size']"),
                  '10:19': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_create_time'),
                  'txt文件': (MobileBy.XPATH, '//*[contains(@text,".txt")]'),
                  'jpg文件': (MobileBy.XPATH, '//*[contains(@text,".jpg")]'),
                  'xlsx文件': (MobileBy.XPATH, '//*[contains(@text,".xlsx")]'),
                  'pdf文件': (MobileBy.XPATH, '//*[contains(@text,".pdf")]'),
                  'mp4文件': (MobileBy.XPATH, '//*[contains(@text,".mp4")]'),
                  'docx文件': (MobileBy.XPATH, '//*[contains(@text,".docx")]'),
                  'avi文件': (MobileBy.XPATH, '//*[contains(@text,".avi")]'),
                  'BPG文件': (MobileBy.XPATH, '//*[contains(@text,".BPG")]'),
                  'com.chinasofti.rcs:id/rl_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_panel'),
                  '已选: 2.2M': (MobileBy.XPATH, '//*[contains(@text,"已选:")]'),
                  '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/button_send'),
                  '继续发送': (MobileBy.XPATH, '//*[@text="继续发送"]'),
                  # 视频选择页面
                  '视频': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  # 照片选择页面
                  '照片': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  # 音乐选择页面
                  '音乐': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  }

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log("下一页")
    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)

    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=15):
        """找不到元素就滑动"""
        if self._is_element_present(locator):
            return self.get_element(locator)
        else:
            c = 0
            while c < times:
                self.page_up()
                if self._is_element_present(locator):
                    return self.get_element(locator)
                c += 1
            return None

    def swipe_page_up(self):
        """向上滑动"""
        self.swipe_by_percent_on_screen(50, 70, 50, 50, 800)

    def page_down(self):
        """向下滑动"""
        self.swipe_by_percent_on_screen(50, 30, 50, 70, 800)

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
    def get_file_size(self):
        """获取选择的文件大小"""
        try:
            file_size = self.get_element(self.__class__.__locators['选择文件大小']).text
        except:
            # 获取不到大小向上滑动一点
            self.swipe_page_up()
            file_size = self.get_element(self.__class__.__locators['选择文件大小']).text
        return file_size

    @TestLogger.log()
    def get_selected_file_size(self):
        """获取已选文件大小信息"""
        el = self.get_element(self.__class__.__locators['已选: 2.2M'])
        return el.text

    @TestLogger.log()
    def select_file(self, file_type):
        """选择文件"""
        el = self.find_file_by_type((MobileBy.XPATH, '//*[contains(@text,"%s")]' % file_type), file_type)
        if el:
            el.click()
            return el
        else:
            print("在SD卡 无%s类型的文件，请预置相应类型文件" % file_type)

    @TestLogger.log()
    def select_file2(self, file_type):
        """选择文件"""
        els = self.get_elements(self.__class__.__locators[file_type])
        if els:
            els[0].click()
            return els[0]
        else:
            print("在SD卡 无%s类型的文件 或者 页面未加载出来。" % file_type)

    @TestLogger.log()
    def click_preset_file_dir(self):
        """进入预置文件的目录"""
        base_dir = os.path.basename(settings.RESOURCE_FILE_PATH)
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % base_dir))
        if el:
            el.click()
            return el
        else:
            print("在SD卡根目录无%s 文件夹，请将预置文件放入此处" % base_dir)

    @TestLogger.log()
    def push_preset_file(self):
        """如果没有预置文件，则上传"""
        base_dir = os.path.basename(settings.RESOURCE_FILE_PATH)
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % base_dir))
        if el:
            return False
        else:
            self.mobile.push_folder(settings.RESOURCE_FILE_PATH, "/sdcard")
            return True

    @TestLogger.log()
    def send_btn_is_enabled(self):
        """获取发送按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["发送"])

    @TestLogger.log()
    def click_send(self, timeout=4):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(1)
        if self._is_element_present(self.__class__.__locators['继续发送']):
            self.click_element(self.__class__.__locators['继续发送'])
        time.sleep(timeout)

