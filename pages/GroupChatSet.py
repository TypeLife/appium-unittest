from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetPage(BasePage):
    """群聊设置页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupSettingActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/layout_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_toolbar'),
                  'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  '群聊设置': (MobileBy.ID, 'com.chinasofti.rcs:id/text_title'),
                  'com.chinasofti.rcs:id/show_more_member': (MobileBy.ID, 'com.chinasofti.rcs:id/show_more_member'),
                  '群成员(2人)': (MobileBy.ID, 'com.chinasofti.rcs:id/member_count'),
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
                  '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_set_to_top_switch'),
                  '置顶聊天': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_set_to_top_tv'),
                  'com.chinasofti.rcs:id/tv_serarch_chat_record': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/tv_serarch_chat_record'),
                  '查找聊天内容': (MobileBy.ID, 'com.chinasofti.rcs:id/left_find_chat_record_tv'),
                  'com.chinasofti.rcs:id/tv_chat_empty': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_chat_empty'),
                  '清空聊天记录': (MobileBy.ID, 'com.chinasofti.rcs:id/left_empty_chat_tv'),
                  '删除并退出': (MobileBy.ID, 'com.chinasofti.rcs:id/delete_and_exit')
                  }

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
        """点击 > 修改群聊名称"""
        self.click_element(self.__locators['修改群聊名称'])
