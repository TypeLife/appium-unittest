from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time
import os
class ContactDetailsPage(BasePage):
    """个人详情"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.ContactDetailActivity'

    __locators = {
        '联系人列表':(MobileBy.ID,'com.chinasofti.rcs:id/rl_group_list_item'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        "联系人头像":(MobileBy.ID,'com.chinasofti.rcs:id/head_tv'),
        '编辑2':(MobileBy.XPATH,"//*[@text='编辑']"),
        '星标图标':(MobileBy.ID,'com.chinasofti.rcs:id/iv_star'),
        '返回上一页': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '名片标题': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_name'),
        '星标': (MobileBy.ID, 'com.chinasofti.rcs:id/star'),
        '编辑': (MobileBy.ID, 'com.chinasofti.rcs:id/txt_call_detail_edit'),
        '好久不见~打个招呼吧': (MobileBy.ID, 'com.chinasofti.rcs:id/recent_contact_hint'),
        '名片号码': (MobileBy.ID, 'com.chinasofti.rcs:id/phone'),
        '名片首字母': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_photo_tv'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_profile_photo_tv'),
        '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_normal_message'),
        '电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_normal_call'),
        '语音通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_voice_call'),
        '视频通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_call'),
        '和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_dial_hefeixin'),
        '详细信息列表容器': (MobileBy.ID, 'com.chinasofti.rcs:id/sv_info'),
        '公司': (MobileBy.ID, 'com.chinasofti.rcs:id/property'),
        '公司名': (MobileBy.ID, 'com.chinasofti.rcs:id/value'),
        '职位': (MobileBy.ID, 'com.chinasofti.rcs:id/property'),
        '职位名': (MobileBy.ID, 'com.chinasofti.rcs:id/value'),
        '邮箱': (MobileBy.ID, 'com.chinasofti.rcs:id/property'),
        '邮箱地址': (MobileBy.ID, 'com.chinasofti.rcs:id/value'),
        '分享名片': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card'),
        'com.chinasofti.rcs:id/btn_share_card_line': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card_line'),
        '邀请使用': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_invitation_to_use'),
        '大图': (MobileBy.ID, 'com.chinasofti.rcs:id/img_smooth'),
        '电话号码': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/et" and @text="13800138005"]'),
        "确定":(MobileBy.ID,'com.chinasofti.rcs:id/tv_save_or_sure'),
        "确定删除": (MobileBy.ID, 'com.chinasofti.rcs:id/bt_button2'),
        "删除联系人":(MobileBy.ID,"com.chinasofti.rcs:id/tv_delete_contact"),
        "呼叫(1/8)":(MobileBy.ID,"com.chinasofti.rcs:id/tv_sure"),
        "暂不开启":(MobileBy.ID,"android:id/button2"),
        "挂断电话":(MobileBy.ID,"com.chinasofti.rcs:id/ivDecline"),
        "视频通话呼叫中":(MobileBy.XPATH,"//*[@text='	视频通话呼叫中']"),
        "挂断视频通话": (MobileBy.ID, "com.chinasofti.rcs:id/iv_out_Cancel"),
        "取消拨打":(MobileBy.XPATH,"//*[@text='取消拨打']")
    }

    @TestLogger.log("更改手机号码")
    def change_mobile_number(self):
        self.input_text(self.__locators["电话号码"],"13800138006")

    @TestLogger.log("点击呼叫")
    def send_call_number(self):
        time.sleep(1)
        self.click_element(self.__locators["呼叫(1/8)"])
        time.sleep(1)

    @TestLogger.log("设置授权窗口")
    def cancel_permission(self):
        time.sleep(3)
        self.click_element(self.__locators["暂不开启"])

    @TestLogger.log("挂断通话")
    def cancel_call(self):
        time.sleep(7)
        self.click_element(self.__locators["挂断电话"])


    @TestLogger.log("删除联系人")
    def change_delete_number(self):
        time.sleep(1)
        self.click_element(self.__locators['删除联系人'])

    @TestLogger.log()
    def open_contacts_page(self):
        """切换到标签页：通讯录"""
        self.click_element(self.__locators['通讯录'])

    @TestLogger.log("删除所有的联系人")
    def delete_all_contact(self):
        """使用此方法前，app进入消息界面"""
        self.open_contacts_page()
        flag=True
        while flag:
            time.sleep(2)
            elements=self.get_elements(self.__locators['联系人列表'])
            if elements:
                elements[0].click()
                self.click_edit_contact()
                time.sleep(1)
                self.hide_keyboard()
                time.sleep(1)
                self.page_up()
                self.change_delete_number()
                time.sleep(1)
                self.click_sure_delete()
            else:
                self.take_screen_out()
                print("无可删除联系人")
                flag=False


    @TestLogger.log("点击返回按钮")
    def click_back_icon(self):
        """点击返回"""
        self.click_element(self.__locators['返回上一页'])

    @TestLogger.log("点击确定")
    def click_sure_icon(self):
        """点击返回"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log("确定删除")
    def click_sure_delete(self):
        """点击返回"""
        time.sleep(3)
        self.click_element(self.__locators['确定删除'])

    @TestLogger.log("点击编辑")
    def click_edit_contact(self):
        """点击编辑按钮"""
        self.click_element(self.__locators['编辑2'])


    @TestLogger.log("获取名片名称")
    def get_contact_name(self, wait_time=0):
        title = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['名片标题']),
            timeout=wait_time
        )
        return title.text

    @TestLogger.log('获取名片号码')
    def get_contact_number(self, wait_time=0):
        number = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['名片号码']),
            timeout=wait_time
        )
        return number.text

    @TestLogger.log("点击消息图标")
    def click_message_icon(self):
        self.click_element(self.__locators['消息'])

    @TestLogger.log('点击电话图标')
    def click_call_icon(self):
        self.click_element(self.__locators['电话'])

    @TestLogger.log("点击语音通话图标")
    def click_voice_call_icon(self):
        self.click_element(self.__locators['语音通话'])

    @TestLogger.log("点击视频通话图标")
    def click_video_call_icon(self):
        self.click_element(self.__locators['视频通话'])

    @TestLogger.log("点击和飞信电话菜单")
    def click_hefeixin_call_menu(self):
        self.click_element(self.__locators['和飞信电话'])

    @TestLogger.log("点击头像查看大图")
    def click_avatar(self):
        """点击头像查看大图"""
        self.click_element(self.__locators['头像'])

    @TestLogger.log("点击大图")
    def click_big_avatar(self):
        """点击大图"""
        self.click_element(self.__locators['大图'])

    @TestLogger.log("点击分享名片")
    def click_share_business_card(self):
        """点击分享名片"""
        self.click_element(self.__locators['分享名片'])

    @TestLogger.log("邀请使用")
    def click_invitation_use(self):
        """邀请使用"""
        self.click_element(self.__locators['邀请使用'])

    @TestLogger.log()
    def message_btn_is_clickable(self):
        """消息按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators["消息"])

    @TestLogger.log()
    def call_btn_is_clickable(self):
        """电话按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators["电话"])

    @TestLogger.log()
    def voice_btn_is_clickable(self):
        """语音通话按钮状态是否可点击"""
        return self._is_clickable(self.__class__.__locators["语音通话"])

    @TestLogger.log()
    def video_call_btn_is_clickable(self):
        """视频通话按钮状态是否可点击"""
        return self._is_clickable(self.__class__.__locators["视频通话"])

    @TestLogger.log("挂断视频通话")
    def end_video_call(self):
        time.sleep(1)
        self.click_element(self.__locators["取消拨打"])

    @TestLogger.log()
    def hefeixin_call_btn_is_clickable(self):
        """和飞信通话按钮状态是否可点击"""
        return self._is_clickable(self.__class__.__locators["和飞信电话"])

    @TestLogger.log()
    def page_should_contain_element_first_letter(self):
        """页面应该包含首字母"""
        return self.page_should_contain_element("名片首字母")

    @TestLogger.log("截图")
    def take_screen_out(self):

        path = os.getcwd() + "/screenshot"
        print(path)
        timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        os.popen("adb wait-for-device")
        time.sleep(1)
        os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
        time.sleep(1)
        if not os.path.isdir(os.getcwd() + "/screenshot"):
            os.makedirs(path)
        os.popen("adb pull /data/local/tmp/tmp.png " + path + "/" + timestamp + ".png")
        os.popen("adb shell rm /data/local/tmp/tmp.png")

def add(func):
    def wrapper(*args):
        try:
            func(*args)
        except:  # 等待AssertionError
            path = os.getcwd() + "/screenshot"
            print(path)
            timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            os.popen("adb wait-for-device")
            time.sleep(2)
            os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
            time.sleep(2)
            if not os.path.isdir(os.getcwd() + "/screenshot"):
                os.makedirs(path)
            os.popen("adb pull /data/local/tmp/tmp.png " + path + "/" + timestamp + ".png")
            os.popen("adb shell rm /data/local/tmp/tmp.png")
            #raise ArithmeticError

    return wrapper