import unittest
from library.core.common.simcardtype import CardType
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *

REQUIRED_MOBILES = {
    'Android-移动': 'single_mobile',
    # 'Android-移动': 'M960BDQN229CH',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(object):
    """前置条件"""

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
        one_key.wait_for_tell_number_load(30)
        one_key.click_one_key_login()
        one_key.click_read_agreement_detail()

        # 同意协议
        agreement = AgreementDetailPage()
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_for_page_load(60)

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动', reset)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

    @staticmethod
    def enter_label_grouping_chat_page(reset=False):
        """进入标签分组会话页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.click_label_grouping()
        label_grouping = LabelGroupingPage()
        label_grouping.wait_for_page_load()
        # 不存在标签分组则创建
        group_name = Preconditions.get_label_grouping_name()
        group_names = label_grouping.get_label_grouping_names()
        if not group_names:
            label_grouping.click_new_create_group()
            label_grouping.wait_for_create_label_grouping_page_load()
            label_grouping.input_label_grouping_name(group_name)
            label_grouping.click_sure()
            # 选择成员
            slc = SelectLocalContactsPage()
            names = slc.get_contacts_name()
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            for name in names:
                slc.select_one_member_by_name(name)
            slc.click_sure()
            label_grouping.wait_for_page_load()
            label_grouping.select_group(group_name)
        # 选择一个标签分组
        label_grouping.select_group(group_names[0])
        lgdp = LableGroupDetailPage()
        # 点击群发信息
        lgdp.click_send_group_info()
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()

    @staticmethod
    def get_label_grouping_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "alg" + phone_number[-4:]
        return group_name


# @unittest.skip("编码中。。。")
class MsgLabelGroupingTest(TestCase):
    """消息->标签分组 模块"""

    @classmethod
    def setUpClass(cls):
        # 登录进入消息页面
        Preconditions.enter_label_grouping_chat_page()

    def default_setUp(self):
        """确保每个用例运行前在标签分组会话页面"""
        chat = LabelGroupingChatPage()
        if chat.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_label_grouping_chat_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0001(self):
        """标签分组会话页面，不勾选本地文件内文件点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、不选择文件，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0002(self):
        """标签分组会话页面，勾选本地文件内文件点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0003(self):
        """标签分组会话页面，不勾选本地视频文件内视频点击发送按钮"""
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击视频
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        # 3、不选择视频，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0004(self):
        """标签分组会话页面，勾选本地视频文件内视频点击发送按钮"""
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击视频
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        # 3、选择视频，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        el = local_file.select_file2("视频")
        if el:
            local_file.click_send()
            chat.wait_for_page_load()
        else:
            local_file.click_back()
            csf.click_back()
            chat.wait_for_page_load()
            raise AssertionError("There is no video")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0005(self):
        """标签分组会话页面，不勾选本地照片文件内视频点击发送按钮"""
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击照片
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        # 3、不选择照片，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0006(self):
        """标签分组会话页面，勾选本地照片文件内视频点击发送按钮"""
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击照片
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        # 3、选择照片，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        el = local_file.select_file2("照片")
        if el:
            local_file.click_send()
            chat.wait_for_page_load()
        else:
            local_file.click_back()
            csf.click_back()
            chat.wait_for_page_load()
            raise AssertionError("There is no pic")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0007(self):
        """标签分组会话页面，不勾选本地音乐文件内视频点击发送按钮"""
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击音乐
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 3、不选择音乐，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0008(self):
        """标签分组会话页面，勾选本地音乐文件内视频点击发送按钮"""
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击音乐
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 3、选择音乐，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        el = local_file.select_file2("音乐")
        if el:
            local_file.click_send()
            chat.wait_for_page_load()
        else:
            local_file.click_back()
            csf.click_back()
            chat.wait_for_page_load()
            raise AssertionError("There is no music")

    @staticmethod
    def public_open_file(file_type):
        """在聊天会话页面打开文件"""
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
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
            # 打开文件
            chat.open_file_in_chat_page(file_type)
            chat.wait_for_open_file()
            chat.click_back_in_open_file_page()
            chat.wait_for_page_load()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
            chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0009(self):
        """标签分组会话页面，点击格式为格式为doc的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为doc的文件
        self.public_open_file(".doc")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0010(self):
        """标签分组会话页面，点击格式为格式为docx的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为docx的文件
        self.public_open_file(".docx")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0011(self):
        """标签分组会话页面，点击格式为格式为ppt的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为ppt的文件
        self.public_open_file(".ppt")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0012(self):
        """标签分组会话页面，点击格式为格式为pptx的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为pptx的文件
        self.public_open_file(".pptx")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0013(self):
        """标签分组会话页面，点击格式为格式为pdf的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为pdf的文件
        self.public_open_file(".pdf")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0014(self):
        """标签分组会话页面，点击格式为格式为xls的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为xls的文件
        self.public_open_file(".xls")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0015(self):
        """标签分组会话页面，点击格式为格式为xlsx的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为xlsx的文件
        self.public_open_file(".xlsx")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0016(self):
        """标签分组会话页面，点击格式为格式为txt的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为txt的文件
        self.public_open_file(".txt")

