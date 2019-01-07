import unittest
import time
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
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

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0017(self):
        """标签分组会话页面，点击不能直接打开的文件调起系统应用打开查阅"""
        # 1、在当前聊天会话页面点击不能直接打开的文件
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
        file = local_file.select_file(".html")
        if file:
            local_file.click_send()
            # 打开文件
            chat.open_file_in_chat_page(".html")
            chat.wait_for_call_sys_app_page()
            chat.click_cancle()
            chat.wait_for_page_load()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
            chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0018(self):
        """标签分组天会话页面，长按文件转发到任意群"""
        # 1、在当前群聊天会话页面长按任意文件
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2、选择转发，选择一个群
            chat.forward_file(".txt")
            scp = SelectContactsPage()
            scp.click_select_one_group()
            sogp = SelectOneGroupPage()
            sogp.wait_for_page_load()
            names = sogp.get_group_name()
            if names:
                sogp.select_one_group_by_name(names[0])
                # 3、点击确定
                sogp.click_sure_forward()
                flag = sogp.is_toast_exist("已转发")
                self.assertTrue(flag)
            else:
                print("WARN: There is no group.")
                sogp.click_back()
                scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0019(self):
        """标签分组天会话页面，长按文件取消转发到任意群"""
        # 1、在当前群聊天会话页面长按任意文件
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2、选择转发，选择一个群
            chat.forward_file(".txt")
            scp = SelectContactsPage()
            scp.click_select_one_group()
            sogp = SelectOneGroupPage()
            sogp.wait_for_page_load()
            names = sogp.get_group_name()
            if names:
                sogp.select_one_group_by_name(names[0])
                # 3、点击取消
                sogp.click_cancel_forward()
            else:
                print("WARN: There is no group.")
            sogp.click_back()
            scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0020(self):
        """标签分组天会话页面，长按文件转发到任意和通讯录联系人"""
        # 1、在当前群聊天会话页面长按任意文件
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2、选择转发，选择一个和通讯录联系人
            chat.forward_file(".txt")
            scp = SelectContactsPage()
            scp.click_he_contacts()
            shcp = SelectHeContactsPage()
            shcp.wait_for_page_load()
            teams = shcp.get_team_names()
            if teams:
                shcp.select_one_team_by_name(teams[0])
                detail_page = SelectHeContactsDetailPage()
                detail_page.wait_for_page_load()
                names = detail_page.get_contacts_names()
                if not names:
                    print("WARN: Please add contacts in %s." % teams[0])
                for name in names:
                    detail_page.select_one_linkman(name)
                    flag = detail_page.is_toast_exist("该联系人不可选", timeout=3)
                    if not flag:
                        break
                # 3、点击确定
                detail_page.click_sure_forward()
                flag2 = detail_page.is_toast_exist("已转发")
                self.assertTrue(flag2)
            else:
                print("WARN: Please create a team and add contacts.")
                shcp.click_back()
                scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0021(self):
        """标签分组天会话页面，长按文件取消转发到任意和通讯录联系人"""
        # 1、在当前群聊天会话页面长按任意文件
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2、选择转发，选择一个和通讯录联系人
            chat.forward_file(".txt")
            scp = SelectContactsPage()
            scp.click_he_contacts()
            shcp = SelectHeContactsPage()
            shcp.wait_for_page_load()
            teams = shcp.get_team_names()
            if teams:
                shcp.select_one_team_by_name(teams[0])
                detail_page = SelectHeContactsDetailPage()
                detail_page.wait_for_page_load()
                names = detail_page.get_contacts_names()
                if not names:
                    print("WARN: Please add contacts in %s." % teams[0])
                for name in names:
                    detail_page.select_one_linkman(name)
                    flag = detail_page.is_toast_exist("该联系人不可选", timeout=3)
                    if not flag:
                        break
                # 3、点击取消
                detail_page.click_cancel_forward()
                detail_page.click_back()
            else:
                print("WARN: Please create a team and add contacts.")
            shcp.click_back()
            scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0022(self):
        """标签分组天会话页面，长按文件转发到任意本地通讯录联系人"""
        # 1、在当前群聊天会话页面长按任意文件
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2、选择转发，选择一个本地通讯录联系人
            chat.forward_file(".txt")
            scp = SelectContactsPage()
            scp.select_local_contacts()
            slcp = SelectLocalContactsPage()
            slcp.wait_for_page_load()
            names = slcp.get_contacts_name()
            if names:
                slcp.select_one_member_by_name(names[0])
                # 3、点击确定
                slcp.click_sure_forward()
                flag = slcp.is_toast_exist("已转发")
                self.assertTrue(flag)
            else:
                print("WARN: There is no linkman.")
                slcp.click_back()
                scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0023(self):
        """标签分组会话页面，长按文件取消转发到任意本地通讯录联系人"""
        # 1、在当前群聊天会话页面长按任意文件
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2、选择转发，选择一个本地通讯录联系人
            chat.forward_file(".txt")
            scp = SelectContactsPage()
            scp.select_local_contacts()
            slcp = SelectLocalContactsPage()
            slcp.wait_for_page_load()
            names = slcp.get_contacts_name()
            if names:
                slcp.select_one_member_by_name(names[0])
                # 3、点击取消
                slcp.click_cancel_forward()
            else:
                print("WARN: There is no linkman.")
            slcp.click_back()
            scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0024(self):
        """标签分组会话页面，长按文件进行收藏"""
        # 1、在当前群聊天会话页面长按任意文件
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2.收藏文件
            chat.collection_file(".txt")
            flag = chat.is_toast_exist("已收藏", timeout=10)
            self.assertTrue(flag)
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0025(self):
        """标签分组天会话页面，长按文件进行删除"""
        # 1、在当前群聊天会话页面长按任意文件
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2.删除文件
            chat.delete_mess(".txt")
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0026(self):
        """标签分组天会话页面，长按自己发送的文件，十分钟内撤回"""
        # 1、在当前群聊天会话页面长按任意文件
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2.撤回文件
            chat.recall_mess(".txt")
            if chat.is_text_present("我知道了"):
                chat.click_i_know()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'SLOW')
    def test_msg_label_grouping_0027(self):
        """标签分组天会话页面，长按自己发送的文件，超过十分钟撤回"""
        # 1、在当前群聊天会话页面长按任意文件
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 长按自己发送的文件，超过十分钟撤回，没有撤回菜单按钮
            for i in range(122):
                time.sleep(2)
                text = chat.driver.page_source
                del text
                time.sleep(3)
                tmp = chat.driver.current_activity
                del tmp
            chat.press_mess(".txt")
            flag = chat.is_text_present("撤回")
            self.assertFalse(flag)
            # 删除文件，关闭弹框菜单
            chat.click_delete()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0028(self):
        """标签分组会话页面，点击位置，再返回到会话页面"""
        # 1、在当前会话窗口点击位置
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、点击左上角的返回按钮
        location_page.click_back()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0029(self):
        """标签分组会话页面，点击位置，默认当前位置直接发送"""
        # 1、在当前会话窗口点击位置
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、点击右上角的发送按钮
        location_page.click_send()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0030(self):
        """标签分组会话页面，点击位置，选择500米内的其他位置发送"""
        # 1、在当前会话窗口点击位置
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、滑动500米内的位置列表，选择其他位置
        location_page.select_other_item()
        # 3、点击右上角的发送按钮
        location_page.click_send()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0031(self):
        """标签分组会话页面，点击位置，选择500米内的其他位置后返回到会话窗口"""
        # 1、在当前会话窗口点击位置
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、滑动500米内的位置列表，选择其他位置
        location_page.select_other_item()
        # 3、点击左上角的返回按钮
        location_page.click_back()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0032(self):
        """标签分组会话页面，长按位置消息体进行转发到本地通讯录联系人"""
        # 1、长按位置消息体
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        info = "Hello"
        chat.input_message(info)
        chat.send_message()
        # 2、选择转发，选择一个本地通讯录联系人
        chat.forward_file(info)
        scp = SelectContactsPage()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name()
        if names:
            slcp.select_one_member_by_name(names[0])
            # 3、点击确定
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            print("WARN: There is no linkman.")
            slcp.click_back()
            scp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0033(self):
        """标签分组会话页面，长按位置消息体进行转发到和通讯录联系人"""
        # 1、在当前群聊天会话页面长按长按位置消息体
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        info = "Hello"
        chat.input_message(info)
        chat.send_message()
        # 2、选择一个和通讯录联系人转发
        chat.forward_file(info)
        scp = SelectContactsPage()
        scp.click_he_contacts()
        shcp = SelectHeContactsPage()
        shcp.wait_for_page_load()
        teams = shcp.get_team_names()
        if teams:
            shcp.select_one_team_by_name(teams[0])
            detail_page = SelectHeContactsDetailPage()
            detail_page.wait_for_page_load()
            names = detail_page.get_contacts_names()
            if not names:
                print("WARN: Please add contacts in %s." % teams[0])
            for name in names:
                detail_page.select_one_linkman(name)
                flag = detail_page.is_toast_exist("该联系人不可选", timeout=3)
                if not flag:
                    break
            # 3、点击确定
            detail_page.click_sure_forward()
            flag2 = detail_page.is_toast_exist("已转发")
            self.assertTrue(flag2)
        else:
            print("WARN: Please create a team and add contacts.")
            shcp.click_back()
            scp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0034(self):
        """标签分组会话页面，长按位置消息体进行转发到群"""
        # 1、在当前群聊天会话页面长按位置消息体
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        info = "Hello"
        chat.input_message(info)
        chat.send_message()
        # 2、选择一个群转发
        chat.forward_file(info)
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        names = sogp.get_group_name()
        if names:
            sogp.select_one_group_by_name(names[0])
            # 3、点击确定
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            print("WARN: There is no group.")
            sogp.click_back()
            scp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0035(self):
        """标签分组会话页面点击位置消息体，在位置界面点击右下角按钮进行导航"""
        # 1、在当前页面点击位置消息体
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 点击更多
        chat.click_more()
        more_page = ChatMorePage()
        # 点击位置
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 点击发送
        location_page.click_send()
        chat.wait_for_page_load()
        # 再一次点击，关闭更多
        chat.click_more()
        chat.wait_for_page_load()
        # 点击位置消息体
        chat.click_addr_info()
        # 2、点击右下角按钮
        chat.click_nav_btn()
        toast_flag = chat.is_toast_exist("未发现手机导航应用", timeout=3)
        map_flag = chat.is_text_present("地图")
        self.assertTrue(toast_flag or map_flag)


