from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time

class CallPage(BasePage):
    """主界面-通话tab页"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '多方通话': (MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall"),
        '返回箭头': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_arror'),
        "消息": (MobileBy.ID, "com.chinasofti.rcs:id/tvMessage"),
        "拨号盘": (MobileBy.ID, "com.chinasofti.rcs:id/tvCall"),
        '拨号键1': (MobileBy.ID, 'com.chinasofti.rcs:id/iv1'),
        '拨号键2': (MobileBy.ID, 'com.chinasofti.rcs:id/iv2'),
        '拨号键3': (MobileBy.ID, 'com.chinasofti.rcs:id/iv3'),
        '拨号键4': (MobileBy.ID, 'com.chinasofti.rcs:id/iv4'),
        '拨号键5': (MobileBy.ID, 'com.chinasofti.rcs:id/iv5'),
        '拨号键6': (MobileBy.ID, 'com.chinasofti.rcs:id/iv6'),
        '拨号键7': (MobileBy.ID, 'com.chinasofti.rcs:id/iv7'),
        '拨号键8': (MobileBy.ID, 'com.chinasofti.rcs:id/iv8'),
        '拨号键9': (MobileBy.ID, 'com.chinasofti.rcs:id/iv9'),
        '拨号键0': (MobileBy.ID, 'com.chinasofti.rcs:id/iv0'),
        '拨号键*': (MobileBy.ID, 'com.chinasofti.rcs:id/ivStar'),
        '拨号键#': (MobileBy.ID, 'com.chinasofti.rcs:id/ivSharp'),
        '删除X': (MobileBy.ID, 'com.chinasofti.rcs:id/ivDelete'),
        '拨号盘收缩删除X': (MobileBy.ID, 'com.chinasofti.rcs:id/ivDeleteHide'),
        '拨打电话按键': (MobileBy.ID, 'com.chinasofti.rcs:id/ivVoiceCall'),
        '通话界面高清显示图片': (MobileBy.ID, 'com.chinasofti.rcs:id/ivNoentrys'),
        '直接拨号或开始搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edt_t9_keyboard'),
        '新建联系人': (MobileBy.XPATH, "//*[contains(@text, '新建联系人')]"),
        '发送消息': (MobileBy.XPATH, "//*[contains(@text, '发送消息')]"),
        '结束通话': (MobileBy.ID, 'com.android.incallui:id/endButton'),
        '呼叫中': (MobileBy.ID, 'com.chinasofti.rcs:id/ivAvatar'),
        '挂断语音通话': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_call_out_term'),
        '视频图片': (MobileBy.ID, 'com.chinasofti.rcs:id/ivMultipartyVideo'),
        '通话显示': (MobileBy.ID, 'com.chinasofti.rcs:id/tvTitle'),
        '通话记录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvName'),
        '0731210086': (MobileBy.XPATH, "//*[contains(@text, '0731210086')]"),
        '删除通话记录': (MobileBy.ID, "com.chinasofti.rcs:id/tvContent"),
        '通话profile': (MobileBy.ID, "com.chinasofti.rcs:id/sdDetail"),
        "多方电话提示框": (MobileBy.ID, "com.chinasofti.rcs:id/mutil_btnFreeCall"),
        "返回": (MobileBy.ID, "com.chinasofti.rcs:id/back"),
        "指定提示": (MobileBy.XPATH, "//*[contains(@text, '点击按钮发起电话')]"),
        '知道了': (MobileBy.XPATH, '//*[@text="知道了"]'),
        '始终允许': (MobileBy.ID, "com.android.packageinstaller:id/permission_allow_button"),
        "多方视频图标": (MobileBy.ID, "com.chinasofti.rcs:id/ivMultipartyVideo"),
        "通话时间": (MobileBy.ID, "com.chinasofti.rcs:id/tvCallTime"),
        "profileName": (MobileBy.ID, "com.chinasofti.rcs:id/tv_profile_name"),
    }


    @TestLogger.log()
    def click_multiparty_call_by_home(self):
        """点击多方通话"""
        self.click_element(self.__locators["多方通话"])

    @TestLogger.log()
    def wait_for_call_page(self, timeout=10, auto_accept_alerts=True):
        """
        等待通话界面
        """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("拨号盘")
            )
        except:
            raise AssertionError("通话界面未显示")
        return self

    @TestLogger.log()
    def is_on_the_call_page(self):
        """判断当前页是否通话界面"""
        flag = False
        element = self.get_elements(self.__locators["视频图片"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def is_on_the_dial_pad(self):
        """判断当前页是否调起拨号盘"""
        flag = False
        element = self.get_elements(self.__locators["拨打电话按键"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_one(self):
        """点击拨号键1"""
        self.click_element(self.__locators["拨号键1"])

    @TestLogger.log()
    def click_two(self):
        """点击拨号键2"""
        self.click_element(self.__locators["拨号键2"])

    @TestLogger.log()
    def click_three(self):
        """点击拨号键3"""
        self.click_element(self.__locators["拨号键3"])

    @TestLogger.log()
    def click_four(self):
        """点击拨号键4"""
        self.click_element(self.__locators["拨号键4"])

    @TestLogger.log()
    def click_five(self):
        """点击拨号键5"""
        self.click_element(self.__locators["拨号键5"])

    @TestLogger.log()
    def click_six(self):
        """点击拨号键6"""
        self.click_element(self.__locators["拨号键6"])

    @TestLogger.log()
    def click_seven(self):
        """点击拨号键7"""
        self.click_element(self.__locators["拨号键7"])

    @TestLogger.log()
    def click_eight(self):
        """点击拨号键8"""
        self.click_element(self.__locators["拨号键8"])

    @TestLogger.log()
    def click_nine(self):
        """点击拨号键9"""
        self.click_element(self.__locators["拨号键9"])

    @TestLogger.log()
    def click_zero(self):
        """点击拨号键0"""
        self.click_element(self.__locators["拨号键0"])

    @TestLogger.log()
    def click_star(self):
        """点击拨号键*"""
        self.click_element(self.__locators["拨号键*"])

    @TestLogger.log()
    def click_sharp(self):
        """点击拨号键#"""
        self.click_element(self.__locators["拨号键#"])

    @TestLogger.log()
    def click_delete(self):
        """点击删除X"""
        self.click_element(self.__locators["删除X"])

    @TestLogger.log()
    def click_delete_hide(self):
        """点击拨号盘收缩删除X"""
        self.click_element(self.__locators["拨号盘收缩删除X"])

    @TestLogger.log()
    def press_zero(self):
        """长按按键0"""
        el = self.get_element(self.__locators["拨号键0"])
        self.press(el)

    @TestLogger.log()
    def press_delete(self):
        """长按删除X"""
        el = self.get_element(self.__locators["删除X"])
        self.press(el)

    @TestLogger.log()
    def press_delete_hide(self):
        """拨号盘收缩删除X"""
        el = self.get_element(self.__locators["拨号盘收缩删除X"])
        self.press(el)

    @TestLogger.log()
    def click_call(self):
        """点击通话"""
        self.click_element(self.__locators["通话"])

    @TestLogger.log()
    def click_message(self):
        """点击消息"""
        self.click_element(self.__locators["消息"])

    @TestLogger.log()
    def click_call_phone(self):
        """点击拨打电话按键"""
        self.click_element(self.__locators["拨打电话按键"])

    @TestLogger.log()
    def check_call_phone(self):
        """检查拨打电话按键"""
        flag = False
        element = self.get_elements(self.__locators["拨打电话按键"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def check_call_image(self):
        """检查拨打电话图片"""
        flag = False
        element = self.get_elements(self.__locators["通话界面高清显示图片"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def check_call_text(self, val=""):
        """检查拨号输入框文本内容与输入相同
        value：输入的文本内容：电话号码，str
        """
        callText=self.get_text(self.__locators["直接拨号或开始搜索"])
        flag = False
        if callText == val:
            flag = True
        return flag

    @TestLogger.log()
    def check_delete_hide(self):
        """检查拨号盘收缩删除X"""
        flag = False
        element = self.get_elements(self.__locators["拨号盘收缩删除X"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_new_contact(self):
        """点击新建联系人"""
        self.click_element(self.__locators["新建联系人"])

    @TestLogger.log()
    def click_send_message(self):
        """点击发送消息"""
        self.click_element(self.__locators["发送消息"])

    @TestLogger.log()
    def click_call_end(self):
        """点击结束通话"""
        self.click_element(self.__locators["结束通话"])

    @TestLogger.log()
    def check_call_success(self):
        """检查拨打电话成功"""
        flag = False
        element = self.get_elements(self.__locators["结束通话"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def wait_for_dial_pad(self, timeout=60, auto_accept_alerts=True):
        """
        等待拨号键盘
        """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("直接拨号")
            )
        except:
            raise AssertionError("通话界面未显示")
        return self

    @TestLogger.log()
    def click_back_by_android(self, times=1):
        """通过android键返回"""
        # times 返回次数
        for i in range(times):
            self.driver.back()
            time.sleep(1)

    @TestLogger.log()
    def get_call_color_of_element(self):
        """获取打电话控件坐标颜色"""
        self.get_coordinate_color_of_element(element=self.__locators["通话"], x=50, y=50, by_percent=True, mode='RGBA')

    @TestLogger.log()
    def check_end_voice_call(self):
        """检查语音通话结束按键是否存在"""
        flag = False
        element = self.get_elements(self.__locators["挂断语音通话"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_end_voice_call(self):
        """点击结束语音通话"""
        self.click_element(self.__locators["挂断语音通话"])


    @TestLogger.log()
    def is_phone_in_calling_state(self):
        """判断是否在通话界面"""
        return self.driver.current_activity == '.InCallActivity'

    @TestLogger.log()
    def hang_up_the_call(self):
        """挂断电话"""
        command = 'input keyevent KEYCODE_ENDCALL'
        if self.is_phone_in_calling_state():
            return self.execute_shell_command(command)

    @TestLogger.log()
    def check_video_image(self):
        """判断是否存在视频图片"""
        return self._is_element_present(self.__locators["视频图片"])

    @TestLogger.log()
    def check_call_display(self):
        """判断是否存在通话显示"""
        return self._is_element_present(self.__locators["通话显示"])

    @TestLogger.log()
    def check_call_display(self):
        """判断是否存在通话显示"""
        return self._is_element_present(self.__locators["通话显示"])

    @TestLogger.log()
    def check_free_call(self):
        """判断是否存在多方通话"""
        return self._is_element_present(self.__locators["多方通话"])

    def get_call_history(self, index):
        """通过下标获取通话记录号码"""
        elements = self.get_elements(self.__locators["通话记录"])
        try:
            if len(elements) > 0:
                return elements[index].text
        except:
            raise IndexError("元素超出索引")

    def dial_number(self, text=""):
        self.input_text(self.__locators["直接拨号或开始搜索"], text)

    @TestLogger.log()
    def press_delete_entry(self):
        """长按删除通话记录"""
        el = self.get_element(self.__locators["通话记录"])
        self.press(el)

    @TestLogger.log()
    def click_delete_entry(self):
        """删除通话记录"""
        self.click_element(self.__locators["删除通话记录"])

    @TestLogger.log()
    def check_delete_entry(self):
        """判断是否删除通话记录弹框"""
        return self._is_element_present(self.__locators["删除通话记录"])

    @TestLogger.log("清空通话记录")
    def delete_all_call_entry(self):
        """前置条件：当前已进入call界面"""
        flag = True
        ret = True
        if self.check_video_image():
            while flag:
                el = self.get_elements(self.__locators["通话记录"])
                if len(el) > 0:
                    self.press(el[0])
                    self.click_delete_entry()
                    if ret:
                        if self.is_text_present("始终允许"):
                            self.click_allow_button()
                        ret = False
                else:
                    print("已清空联系人")
                    flag = False
        else:
            raise AttributeError

    @TestLogger.log()
    def get_call_entry_color_of_element(self):
        """获取通话记录控件坐标颜色"""
        return self.get_coordinate_color_of_element(element=self.__locators["通话记录"], x=50, y=50, by_percent=True, mode='RGBA')

    @TestLogger.log()
    def click_call_profile(self):
        """点击通话profile"""
        self.click_element(self.__locators["通话profile"])

    @TestLogger.log()
    def press_keyboard(self):
        """长按拨号盘输入框"""
        el = self.get_element(self.__locators["直接拨号或开始搜索"])
        self.press(el)

    @TestLogger.log()
    def is_exist_specified_prompt(self):
        """是否存在指定提示"""
        return self._is_element_present(self.__class__.__locators["指定提示"])

    @TestLogger.log()
    def click_multi_party_telephone(self):
        """点击多方电话"""
        self.click_element(self.__class__.__locators["多方电话提示框"])

    @TestLogger.log()
    def is_exist_know(self):
        """是否存在“知道了”文本"""
        return self._is_element_present(self.__class__.__locators["知道了"])

    @TestLogger.log()
    def click_know(self):
        """点击知道了"""
        self.click_element(self.__class__.__locators["知道了"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_exist_allow_button(self):
        """是否存在始终允许"""
        return self._is_element_present(self.__class__.__locators["始终允许"])

    @TestLogger.log()
    def click_allow_button(self):
        """点击允许"""
        self.click_element(self.__class__.__locators["始终允许"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待通话页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["多方视频图标"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_call_time(self):
        """点击通话时间"""
        self.click_element(self.__class__.__locators["通话时间"])

    @TestLogger.log()
    def is_exist_profile_name(self):
        """判断是否存在profile_name"""
        return self._is_element_present(self.__locators["profileName"])

    @TestLogger.log()
    def get_profile_name(self):
        """获取profile_name"""
        return self.get_text(self.__locators["profileName"])
