from appium.webdriver.common.mobileby import MobileBy
import re
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetPage(BasePage):
    """群聊设置页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupSettingActivity'

    __locators = {'菜单区域': (MobileBy.CLASS_NAME, 'android.widget.ScrollView'),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/layout_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  '群聊设置': (MobileBy.ID, 'com.chinasofti.rcs:id/text_title'),
                  'com.chinasofti.rcs:id/show_more_member': (MobileBy.ID, 'com.chinasofti.rcs:id/show_more_member'),
                  '群成员(2人)': (MobileBy.ID, 'com.chinasofti.rcs:id/member_count'),
                  '群成员展开>': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/member_count"]/../android.widget.ImageView'),
                  'com.chinasofti.rcs:id/member_list': (MobileBy.ID, 'com.chinasofti.rcs:id/member_list'),
                  'com.chinasofti.rcs:id/iv_avatar': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_avatar'),
                  'com.chinasofti.rcs:id/iv_head': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_head'),
                  'com.chinasofti.rcs:id/iv_group_chairman_tag': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/iv_group_chairman_tag'),
                  'mobile0...': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
                  'frank': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
                  'com.chinasofti.rcs:id/tv_name': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
                  'com.chinasofti.rcs:id/group_name_line': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name_line'),
                  '群聊名称': (MobileBy.ID, 'com.chinasofti.rcs:id/left_group_chat_name_tv'),
                  '群聊001': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
                  '修改群聊名称': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name_right_arrow'),
                  'com.chinasofti.rcs:id/rl_group_avatars': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_avatars'),
                  '群二维码': (MobileBy.ID, 'com.chinasofti.rcs:id/left_group_code_tv'),
                  'com.chinasofti.rcs:id/iv_group_avatars': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_group_avatars'),
                  'com.chinasofti.rcs:id/arrow1': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow1'),
                  'com.chinasofti.rcs:id/my_group_name_line': (MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name_line'),
                  '我在本群的昵称': (MobileBy.ID, 'com.chinasofti.rcs:id/left_me_group_name_tv'),
                  'mobile0489': (MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name'),
                  'com.chinasofti.rcs:id/my_group_name_right_arrow': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name_right_arrow'),
                  'com.chinasofti.rcs:id/group_manage': (MobileBy.ID, 'com.chinasofti.rcs:id/group_manage'),
                  '群管理': (MobileBy.ID, 'com.chinasofti.rcs:id/left_group_manage_tv'),
                  '消息免打扰': (MobileBy.ID, 'com.chinasofti.rcs:id/left_message_interruption_tv'),
                  '消息免打扰开关': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_undisturb'),
                  '置顶聊天开关': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_set_to_top_switch'),
                  '置顶聊天': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_set_to_top_tv'),
                  'com.chinasofti.rcs:id/tv_serarch_chat_record': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/tv_serarch_chat_record'),
                  '查找聊天内容': (MobileBy.ID, 'com.chinasofti.rcs:id/left_find_chat_record_tv'),
                  'com.chinasofti.rcs:id/tv_chat_empty': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_chat_empty'),
                  '清空聊天记录': (MobileBy.ID, 'com.chinasofti.rcs:id/left_empty_chat_tv'),
                  '删除并退出': (MobileBy.ID, 'com.chinasofti.rcs:id/delete_and_exit'),
                  "确认": (MobileBy.XPATH, '//*[@text ="确认"]'),
                  "取消": (MobileBy.XPATH, '//*[@text ="取消"]')
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待群聊设置页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("群聊设置")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def get_group_total_member(self):
        """获取群成员总人数"""
        el = self.get_element(self.__class__.__locators['群成员(2人)'])
        res = re.search(r"\d+", el.text)
        if res:
            return int(res.group())
        else:
            return 0

    @TestLogger.log()
    def click_group_member_show(self):
        """点击群成员展示>"""
        self.click_element(self.__class__.__locators["群成员展开>"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_add_member(self):
        """点击 '+ ': 添加成员"""
        self.driver.find_elements(MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/tv_name"]')[-2].click()

    @TestLogger.log()
    def click_del_member(self):
        """点击 '-': 删除成员"""
        self.driver.find_elements(MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/tv_name"]')[-1].click()

    @TestLogger.log()
    def click_modify_group_name(self):
        """点击 修改群聊名称"""
        self.click_element(self.__locators['修改群聊名称'])

    @TestLogger.log()
    def click_QRCode(self):
        """点击群二维码"""
        self.click_element(self.__locators['群二维码'])

    @TestLogger.log()
    def click_my_card(self):
        """点击我在本群的昵称"""
        self.click_element(self.__locators['我在本群的昵称'])

    @TestLogger.log()
    def click_group_manage(self):
        """点击群管理"""
        self.click_element(self.__locators['群管理'])

    @TestLogger.log()
    def click_switch_undisturb(self):
        """点击消息免打扰开关"""
        self.click_element(self.__locators['消息免打扰开关'])

    @TestLogger.log()
    def get_switch_undisturb_status(self):
        """获取消息免打扰开关状态"""
        el = self.get_element(self.__locators['消息免打扰开关'])
        return el.get_attribute("checked") == "true"

    @TestLogger.log()
    def get_chat_set_to_top_switch_status(self):
        """获取置顶聊天开关状态"""
        el = self.get_element(self.__locators['置顶聊天开关'])
        return el.get_attribute("checked") == "true"

    @TestLogger.log()
    def click_chat_set_to_top_switch(self):
        """点击置顶聊天开关"""
        self.click_element(self.__locators['置顶聊天开关'])

    @TestLogger.log()
    def click_find_chat_record(self):
        """点击查找聊天内容"""
        self.click_element(self.__locators['查找聊天内容'])

    @TestLogger.log()
    def click_clear_chat_record(self):
        """点击清空聊天记录"""
        self.click_element(self.__locators['清空聊天记录'])

    @TestLogger.log()
    def click_delete_and_exit(self):
        """点击删除并退出"""
        self.click_element(self.__locators['删除并退出'])

    @TestLogger.log()
    def wait_clear_chat_record_confirmation_box_load(self, timeout=10, auto_accept_alerts=True):
        """等待 聊天记录清除确认框"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("是否清空聊天记录")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_exist_and_delete_confirmation_box_load(self, timeout=10, auto_accept_alerts=True):
        """等待 解散群成员确认框加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("解散群")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_confirm(self):
        """点击确认"""
        self.click_element(self.__locators['确认'])

    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__locators['取消'])

    @TestLogger.log()
    def scroll_to_bottom(self):
        """滑到菜单底部"""
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['群聊设置'])
        )
        self.swipe_by_direction(self.__locators['菜单区域'], 'up')
