import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from selenium.common.exceptions import TimeoutException

from library.core.utils.applicationcache import current_mobile


class MeEditUserProfilePage(BasePage):
    """我-》编辑个人资料"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.UserProfileEditActivity'

    __locators = {'': (MobileBy.ID, ''),

                  '意见反馈': (MobileBy.XPATH, "//*[contains(@text, '意见反馈')]"),
                  '网上营业厅': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar_title_tv'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  '保存': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_save'),
                  '姓名': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_contact_name'),
                  '电话': (MobileBy.ID, 'com.chinasofti.rcs:id/phone'),
                  '个人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_photo'),
                  '公司': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_contact_company'),
                  '职位': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_contact_job'),
                  '邮箱': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_contact_email'),
                  '分享名片': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card'),
                  # 打开编辑图片
                  '编辑图片': (MobileBy.ID, 'com.chinasofti.rcs:id/change_photo'),
                  '选择图片': (MobileBy.XPATH, "//*[contains(@text, '选择图片')]"),
                  '点击拍照': (MobileBy.ID, 'com.chinasofti.rcs:id/camera_picture'),
                  '拍照': (MobileBy.XPATH, "//*[contains(@resource-id, 'camera') and contains(@resource-id, 'shutter_button')]"),
                  '确定照片': (MobileBy.XPATH, "//*[contains(@resource-id, 'camera') and contains(@resource-id, 'done')]"),
                  '确定照片2': (MobileBy.XPATH, "//*[contains(@resource-id, 'camera') and contains(@resource-id, 'confirm')]"),
                  '取消照片': (MobileBy.XPATH, "//*[contains(@resource-id, 'camera') and contains(@resource-id, 'cancel')]"),
                  '选择照片': (MobileBy.ID, 'com.chinasofti.rcs:id/album_picture'),
                  '照片框': (MobileBy.ID, 'com.chinasofti.rcs:id/foreground_bg'),
                  '保存截图': (MobileBy.ID, 'com.chinasofti.rcs:id/ok'),
                  '修改资料提示框': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
                  '取消1': (MobileBy.XPATH, "//*[contains(@text, '取消')]"),
                  '保存1': (MobileBy.ID, "com.chinasofti.rcs:id/btn_ok"),

                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待个人编辑页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["编辑图片"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_select_pic_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待个人编辑页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择图片"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('判断该元素是否能点击')
    def element_is_click_able(self, text):
        return self._is_clickable(self.__locators[text])

    @TestLogger.log('判断该元素是否能激活')
    def element_is_enabled_able(self, text):
        return self._is_enabled(self.__locators[text])

    @TestLogger.log('输入姓名文本内容')
    def input_name(self, locator, text):
        self.input_text(self.__locators[locator], text)
        current_mobile().hide_keyboard_if_display()

    @TestLogger.log('获取元素文本内容')
    def get_element_text(self, text):
        infor = self.get_text(self.__locators[text])
        if len(infor) > 40:
            return False
        else:
            return True

    @TestLogger.log('点击保存')
    def click_save(self):
        self.click_element(self.__locators["保存"])

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators["返回"])

    @TestLogger.log('是否有弹框提示保存成功')
    def is_toast_save_success(self):
        return self.is_toast_exist("保存成功", timeout=10)

    @TestLogger.log('是否有弹框提示资料未变化，不保存')
    def is_toast_save(self):
        return self.is_toast_exist("您的资料未变化，无需保存", timeout=10)

    @TestLogger.log('是否有弹框提示资料未变化，不保存')
    def is_toast_save_null(self):
        return self.is_toast_exist("姓名不能为空")

    @TestLogger.log('是否有弹框提示网路异常')
    def is_toast_net(self):
        return self.is_toast_exist("网络不可用，请检查网络设置")

    @TestLogger.log('是否有弹框提示输入格式异常')
    def is_toast_format(self, text):
        return self.is_toast_exist("%s格式不正确，请重新输入" % text)

    @TestLogger.log()
    def edit_clear(self, locator):
        """清除输入框内容"""
        self.click_element(self.__locators[locator])
        text = self.get_text(self.__locators[locator])
        if len(text) == 0:
            return
        self.driver.keyevent(123)
        for i in range(0, len(text)):
            self.driver.keyevent(67)
        current_mobile().hide_keyboard_if_display()

    @TestLogger.log('往下滑动')
    def swipe_up(self):
        # for i in range(12):
        #     self.swipe_by_direction(self.__locators["公司"], "up")
        self.page_up()

    @TestLogger.log('点击公司')
    def click_company(self):
        self.click_element(self.__locators["公司"])

    @TestLogger.log()
    def is_element_exist(self, text):
        """当前页面是否包含此元素"""
        return self._is_element_present(self.__locators[text])

    @TestLogger.log('点击个人头像')
    def click_edit_pic(self):
        self.click_element(self.__locators["个人头像"])

    @TestLogger.log('点击编辑图片')
    def click_edit_pics(self):
        self.click_element(self.__locators["编辑图片"])

    #   选择照片页面方法
    @TestLogger.log('点击拍照')
    def click_take_pics(self):
        self.click_element(self.__locators["点击拍照"])

    @TestLogger.log('拍照')
    def click_taking_pics(self):
        self.click_element(self.__locators["拍照"])
        time.sleep(6.5)

    @TestLogger.log('点击确定照片')
    def click_save_pics(self):
        if self._is_element_present(self.__locators["确定照片"]):
            self.click_element(self.__locators["确定照片"])
        else:
            self.click_element(self.__locators["确定照片2"])

    @TestLogger.log('点击取消照片')
    def click_cancel_pics(self):
        self.click_element(self.__locators["取消照片"])

    @TestLogger.log('点击选择照片')
    def click_select_pics(self, n):
        pics = self.get_elements(self.__locators["选择照片"])
        if n > len(pics):
            raise AssertionError("在所有照片首页没有 %s 张图片，请上传图片." % n)
        pics[n].click()

    @TestLogger.log('点击保存截图')
    def click_save_save_pics(self):
        self.click_element(self.__locators["保存截图"])

    @TestLogger.log('点击取消修改资料')
    def click_cancel_mod(self):
        self.click_element(self.__locators["取消1"])

    @TestLogger.log('点击保存修改资料')
    def click_save_mod(self):
        self.click_element(self.__locators["保存1"])

    @TestLogger.log()
    def is_text_exist(self, text):
        """当前页面是否包含此文本"""
        return self.is_text_present(text)
