import time
import unittest
import uuid
import re

from appium.webdriver.common.mobileby import MobileBy

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from pages.me.MeEditUserProfile import MeEditUserProfilePage
from pages.me.MeViewUserProfile import MeViewUserProfilePage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(object):
    """前置条件"""

    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def select_mobile(category, reset=False):
        """选择手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        if reset:
            current_mobile().reset_app()
        return client

    @staticmethod
    def make_already_in_one_key_login_page():
        """已经进入一键登录页"""
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            # current_mobile().launch_app()
            current_mobile().reset_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        current_mobile().hide_keyboard_if_display()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        permission_list.click_submit_button()
        one_key.wait_for_page_load(30)

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        if one_key.have_read_agreement_detail():
            one_key.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动', reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

    @staticmethod
    def make_already_in_me_all_page():
        """确保应用在消息页面"""

        # 如果在消息页，不做任何操作
        mess = MessagePage()
        mep = MePage()
        if mep.is_on_this_page():
            return
        if mess.is_on_this_page():
            mess.open_me_page()
            mep.is_on_this_page()
            return
        # 进入一键登录页
        Preconditions.make_already_in_message_page(reset=False)
        mess.open_me_page()

    @staticmethod
    def make_already_set_message():
        """确保私人已经发送一条消息，且已收藏"""
        Preconditions.make_already_in_message_page()
        # 1.点击新建消息
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        mess.click_new_message()
        # 2.选择联系人发送一条消息
        scp = SelectContactsPage()
        scp.wait_for_page_local_contact_load()
        scp.click_one_contact("大佬2")
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            bcp.click_i_have_read()
        infor = "测试工程师"
        bcp.input_message(infor * 30)
        bcp.send_message()
        # 3.点击该信息收藏
        mess.press_file_to_do("测试工程师", "收藏")
        if not bcp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        bcp.click_element(["id", 'com.chinasofti.rcs:id/back_arrow'])

    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        sc.click_select_one_group()
        # 群名
        group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        # 有群返回，无群创建
        if group_name in group_names:
            return
        sog.click_back()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        if not names:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def enter_group_chat_page(reset=False):
        """进入群聊聊天会话页面"""
        # 确保已有群
        Preconditions.make_already_have_my_group(reset)
        # 如果有群，会在选择一个群页面，没有创建群后会在群聊页面
        scp = GroupChatPage()
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            group_name = Preconditions.get_group_chat_name()
            # 点击群名，进入群聊页面
            sogp.select_one_group_by_name(group_name)
            scp.wait_for_page_load()
        if scp.is_on_this_page():
            return
        else:
            raise AssertionError("Failure to enter group chat session page.")

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "chargourp" + phone_number[-4:]
        return group_name

    @staticmethod
    def make_already_set_chart_group_message():
        """确保群聊已经发送一条消息，且已收藏"""
        Preconditions.enter_group_chat_page()
        # 1.点击新建消息
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        infor = "我是测试工程师15918730974,www.baidu.com "
        scp.input_message(infor * 40)
        scp.send_message()
        # 3.点击该信息收藏
        scp.press_file_to_do("我是测试工程师", "收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        mess = MessagePage()
        mess.click_back()
        mess.click_back()
        mess.click_back()

    @staticmethod
    def make_already_set_chart_group_video(pic_video="video"):
        """确保群聊已经发送一条视频，且已收藏"""
        Preconditions.enter_group_chat_page()
        # 1.点击新建消息
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        scp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        time.sleep(2)
        if pic_video == "video":
            cpg.select_video_fk()
            cpg.click_send()
            time.sleep(3)
            scp.press_video()
        if pic_video == "pic":
            cpg.select_pic_fk()
            cpg.click_send()
            time.sleep(3)
            scp.press_pic()
        # 3.点击该信息收藏
        scp.click_collection()
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        mess = MessagePage()
        mess.click_back()
        mess.click_back()
        mess.click_back()

    @staticmethod
    def make_already_set_chart_group_voice():
        """确保群聊已经发送一条语音，且已收藏"""
        Preconditions.enter_group_chat_page()
        # 1.点击新建消息
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        scp.click_audio_btn()
        time.sleep(7)
        if scp.is_text_present("仅发送语音"):
            scp.click_element([MobileBy.XPATH, "//*[contains(@text,'仅发送语音')]"], 15)
            scp.click_element([MobileBy.XPATH, "//*[contains(@text,'确定')]"], 15)
        if scp.is_text_present("无法识别，请重试"):
            scp.click_element([MobileBy.XPATH, "//*[contains(@text,'设置')]"], 15)
            scp.click_element([MobileBy.XPATH, "//*[contains(@text,'仅发送语音')]"], 15)
            scp.click_element([MobileBy.XPATH, "//*[contains(@text,'确定')]"], 15)
        time.sleep(2)
        scp.click_send_btn()
        # 3.点击该信息收藏
        time.sleep(2.5)
        scp.press_voice_message_to_do("收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        mess = MessagePage()
        mess.click_back()
        mess.click_back()
        mess.click_back()

    @staticmethod
    def make_already_set_chart_group_name_card():
        """确保群聊已经发送一个名片，且已收藏"""
        Preconditions.enter_group_chat_page()
        # 1.点击新建消息
        mess = MessagePage()
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        scp.click_name_card()
        ssp = SelectContactsPage()
        ssp.wait_for_page_local_contact_load()
        ssp.click_one_local_contacts()
        ssp.click_element([MobileBy.XPATH, "//*[contains(@text,'发送名片')]"], 15)
        time.sleep(3)
        # 3.点击该信息收藏
        scp.press_file_to_do("个人名片", "收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        mess = MessagePage()
        mess.click_back()
        mess.click_back()
        mess.click_back()

    @staticmethod
    def make_already_set_chart_group_location():
        """确保群聊已经发送一个位置信息，且已收藏"""
        Preconditions.enter_group_chat_page()
        # 1.点击更多位置信息
        mess = MessagePage()
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        scp.click_more()
        mess.click_set_message("位置")
        clp = ChatLocationPage()
        clp.wait_for_page_load()
        clp.click_send()
        # 3.点击该信息收藏
        scp.press_message_to_do("收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        mess.click_back()
        mess.click_back()
        mess.click_back()

    @staticmethod
    def make_already_set_chart_group_file(file_type):
        """确保群聊已经发送一个文件信息，且已收藏"""
        Preconditions.enter_group_chat_page()
        # 1.点击更多位置信息
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        scp.click_more()
        cmp = ChatMorePage()
        cmp.wait_for_page_load()
        cmp.click_file1()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 没有预置文件，则上传
        flag = local_file.push_preset_file()
        if flag:
            local_file.click_back()
            csf.click_local_file()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(file_type)
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        # 3.点击该信息收藏
        scp.press_file_to_do(file_type, "收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        cmp.click_back()
        cmp.click_back()
        cmp.click_back()

    @staticmethod
    def delete_all_my_collection():
        """确保群聊已经发送一个文件信息，且已收藏"""
        mep = MePage()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_collection()
        for i in range(len(file_names)):
            mcp.press_and_move_left()
            if mcp.is_delete_element_present():
                mcp.click_delete_collection()
                mcp.click_sure_forward()
                # 4.点击返回
        mep.click_back()
        mep.open_message_page()


class MeAllCollect(TestCase):
    """
    模块：我的_收藏

    文件位置：全量/4.我模块全量测试用例-张淑丽.xlsx
    表格：我页面（收藏模块406后）

    """

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    def default_tearDown(self):
        pass
        # current_mobile().disconnect_mobile()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_406(self):
        """我页面跳转验证"""
        Preconditions.make_already_set_message()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.element_contain_text("我", "我")
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_406(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_407(self):
        """我页面跳转验证"""
        Preconditions.make_already_set_chart_group_message()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.element_contain_text("我", Preconditions.get_group_chat_name())
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_407(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_408(self):
        """我页面跳转验证"""
        Preconditions.make_already_set_chart_group_message()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.element_contain_text("今天", "今天")
        mcp.element_contain_text("我", Preconditions.get_group_chat_name())
        # 3.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_408(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_412(self):
        """查看收藏内容为短视频的展示"""
        Preconditions.make_already_set_chart_group_video()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验是否有视频和播放时长（图片比例暂不做）
        flag = mcp.get_video_len("视频时长")
        self.assertIsNotNone(re.match(r'(\d\d:\d\d)', flag))
        mcp.page_should_contain_element([MobileBy.ID, 'com.chinasofti.rcs:id/iv_favorite_video_bg'])
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_412(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_413(self):
        """查看收藏内容为文字（含短信）的展示"""
        Preconditions.make_already_set_chart_group_message()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验收藏内容不超过三行
        self.assertEquals(mcp.get_width_of_collection("www.baidu.com", 3), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_413(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_414(self):
        """查看收藏内容为语音消息的展示"""
        Preconditions.make_already_set_chart_group_voice()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验语音消息
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        flag = mcp.get_video_len("[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口")
        self.assertIsNotNone(re.match(r'(\d+秒)', flag))
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_414(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_416(self):
        """查看收藏内容为名片的展示"""
        Preconditions.make_already_set_chart_group_name_card()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 进入群聊获取卡名
        mess.click_set_message("名片")
        scp = GroupChatPage()
        scp.wait_for_page_load()
        name = scp.get_name_card()
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        flag1 = mcp.get_video_len("[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口")
        # 名片名称最多显示两行
        self.assertEquals(mcp.get_width_of_collection("[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口", 2), True)
        flag2 = "[名片]" + name + "的个人名片"
        self.assertEquals(flag1, flag2)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_416(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_417(self):
        """查看收藏内容为位置信息的展示"""
        Preconditions.make_already_set_chart_group_location()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 进入群聊获取卡名
        mess.click_set_message('位置')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        location = scp.get_location()
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        flag1 = mcp.get_video_len("[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口")
        flag2 = "[位置]" + location
        # 位置信息最多显示2行
        self.assertEquals(mcp.get_width_of_collection("[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口", 2), True)
        self.assertEquals(flag1, flag2)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_417(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_419(self):
        """查看收藏内容为未知文件的展示"""
        Preconditions.make_already_set_chart_group_file(".log")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        for i in range(2):
            mcp.page_down()
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        mcp.element_should_contain_text(["id", 'com.chinasofti.rcs:id/file_name'], ".log")
        self.assertEquals(mcp.get_width_of_collection("文件名", 1), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_419(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_420(self):
        """查看收藏内容为已知文件的展示"""
        Preconditions.make_already_set_chart_group_file(".doc")
        Preconditions.make_already_set_chart_group_file(".txt")
        Preconditions.make_already_set_chart_group_file(".docx")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        for i in range(2):
            mcp.page_down()
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".docx"), True)
        self.assertEquals(file_names[1].endswith(".txt"), True)
        self.assertEquals(file_names[2].endswith(".doc"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_420(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_421(self):
        """查看收藏内容为可识别的幻灯片格式"""
        Preconditions.make_already_set_chart_group_file(".ppt")
        Preconditions.make_already_set_chart_group_file(".pptx")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        for i in range(2):
            mcp.page_down()
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".pptx"), True)
        self.assertEquals(file_names[1].endswith(".ppt"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_421(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_422(self):
        """查看收藏内容为可识别的表格格式"""
        Preconditions.make_already_set_chart_group_file(".xls")
        Preconditions.make_already_set_chart_group_file(".xlsx")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".xlsx"), True)
        self.assertEquals(file_names[1].endswith(".xls"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_422(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_423(self):
        """查看收藏内容为可识别的PDF格式"""
        Preconditions.make_already_set_chart_group_file(".pdf")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".pdf"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_423(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_425(self):
        """查看收藏内容为可识别的音频格式"""
        Preconditions.make_already_set_chart_group_file(".mp3")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".mp3"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_425(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_427(self):
        """查看收藏内容为可识别的压缩格式"""
        Preconditions.make_already_set_chart_group_file(".rar")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".rar"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_427(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_428(self):
        """查看收藏内容为短视频的展示"""
        Preconditions.make_already_set_chart_group_video()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.点击该收藏内容
        mcp.click_collection_pic_video("收藏的视频")
        mcp.wait_until(
            condition=lambda d: current_mobile()._is_enabled(['id', 'com.chinasofti.rcs:id/favorite_title'])
        )
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/sv_video'])
        # 4.点击返回
        mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_428(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_429(self):
        """在收藏列表中打开音频文件"""
        Preconditions.make_already_set_chart_group_file(".mp3")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        file_name = file_names[0]
        # 3.点击收藏的按钮
        mcp.click_collection_file_name()
        mcp.wait_until(
            condition=lambda d: current_mobile()._is_enabled(['id', 'com.android.mediacenter:id/content_play'])
        )
        mcp.page_should_contain_text(file_name)
        # 4.点击返回
        mcp.click_element(["id", "com.android.mediacenter:id/close_mediaplay"], 15)
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_429(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_430(self):
        """查看收藏内容为图片的展示"""
        Preconditions.make_already_set_chart_group_video(pic_video="pic")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.点击该收藏内容
        mcp.click_collection_pic_video("收藏的图片")
        mcp.wait_until(
            condition=lambda d: current_mobile()._is_enabled(['id', 'com.chinasofti.rcs:id/favorite_title'])
        )
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/iv_photo'])
        # 4.点击返回
        mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_430(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_431(self):
        """在收藏列表中打开文本文件"""
        Preconditions.make_already_set_chart_group_file(".txt")
        Preconditions.make_already_set_chart_group_file(".doc")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        # 3.点击收藏的按钮,文本文件可以显示
        for i in range(len(file_names)):
            try:
                mcp.click_collection_file_name(i=i)
            except Exception:
                mcp.click_collection_file_name(i=i)
            mcp.wait_until(
                condition=lambda d: current_mobile()._is_enabled(['id', 'com.chinasofti.rcs:id/title'])
            )
            file_name = file_names[i]
            mcp.page_should_contain_text(file_name)
            mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_431(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_432(self):
        """在收藏列表中打开文本文件"""
        Preconditions.make_already_set_chart_group_file(".ppt")
        Preconditions.make_already_set_chart_group_file(".pptx")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        # 3.点击收藏的按钮(尝试两次),文本文件可以显示
        for i in range(len(file_names)):
            try:
                mcp.click_collection_file_name(i=i)
            except Exception:
                mcp.click_collection_file_name(i=i)
            mcp.wait_until(
                condition=lambda d: current_mobile()._is_enabled(['id', 'com.chinasofti.rcs:id/title'])
            )
            file_name = file_names[i]
            mcp.page_should_contain_text(file_name)
            mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_432(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_433(self):
        """打开表格格式为.xls  .xlsx"""
        Preconditions.make_already_set_chart_group_file(".xls")
        Preconditions.make_already_set_chart_group_file(".xlsx")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        # 3.点击收藏的按钮,文本文件可以显示
        for i in range(len(file_names)):
            try:
                mcp.click_collection_file_name(i=i)
            except Exception:
                mcp.click_collection_file_name(i=i)
            mcp.wait_until(
                condition=lambda d: current_mobile()._is_enabled(['id', 'com.chinasofti.rcs:id/title'])
            )
            file_name = file_names[i]
            mcp.page_should_contain_text(file_name)
            mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_433(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_434(self):
        """打开文件PDF格式为.pdf"""
        Preconditions.make_already_set_chart_group_file(".pdf")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        file_name = file_names[0]
        # 3.点击收藏的按钮,文本文件可以显示
        mcp.click_collection_file_name()
        mcp.wait_until(
            condition=lambda d: current_mobile()._is_enabled(['id', 'com.chinasofti.rcs:id/title'])
        )
        mcp.page_should_contain_text(file_name)
        # 4.点击返回
        mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_434(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_437(self):
        """打开收藏的位置信息"""
        Preconditions.make_already_set_chart_group_location()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.点击收藏的按钮,文本文件可以显示
        mcp.open_location("位置")
        mcp.wait_for_location_page_load()
        mcp.page_contain_element("导航按钮")
        # 4.点击返回
        mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_437(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_438(self):
        """打开收藏的位置信息"""
        Preconditions.make_already_set_chart_group_location()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.点击收藏的按钮,文本文件可以显示
        mcp.open_location("位置")
        mcp.wait_for_location_page_load()
        mcp.page_contain_element("导航按钮")
        # 4.点击返回，检验是否在收藏位置页面
        mep.click_back()
        mcp.element_contain_text("[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口", "位置")
        # 5.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_all_page_438(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_439(self):
        """设置页面显示验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的设置
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        # 3.检验设置列表页面展示
        sp = SettingPage()
        sp.wait_for_page_load()
        menu = {"短信设置", "消息通知", "来电管理", "副号管理", "联系人管理", "字体大小", "多语言", "参与体验改善计划", "退出", }
        self.assertEquals(sp.page_contain_texts(menu), True)
        # 4.点击返回
        sp.click_back()
        mep.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_442(self):
        """验证我-设置-退出登录(正常网络)"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的设置
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        # 3.点击退出登陆
        sp = SettingPage()
        sp.wait_for_page_load()
        sp.click_logout()
        sp.click_ok_of_alert()
        # 4.校验退出后在登陆页面
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        self.assertEquals(one_key.is_on_this_page(), True)

    # @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    # def test_me_all_page_443(self):
    #     """验证我-设置-退出登录(异常网络)"""
    #     # 1.点击跳转到我的页面
    #     mess = MessagePage()
    #     mess.wait_for_page_load()
    #     mess.set_network_status(0)
    #     # 2.点击我的设置
    #     mess.open_me_page()
    #     mep = MePage()
    #     mep.is_on_this_page()
    #     mep.click_setting_menu()
    #     # 3.点击退出登陆
    #     sp = SettingPage()
    #     sp.wait_for_page_load()
    #     sp.click_logout()
    #     sp.click_ok_of_alert()
    #     # 4.校验退出后在登陆页面
    #     one_key = OneKeyLoginPage()
    #     one_key.wait_for_page_load()
    #     self.assertEquals(one_key.is_on_this_page(), True)
    #     # 5.退出后再点击一键登录有弹框提示
    #     one_key.click_one_key_login()
    #     if not one_key.is_toast_exist("请检查网络设置"):
    #         raise AssertionError("没有此网络异常弹框")
    #
    # def tearDown_test_me_all_page_443(self):
    #     # 1.打开网络
    #     mess = MessagePage()
    #     mess.set_network_status(6)
