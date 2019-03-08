import random
import time
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages import *
import uuid


class Preconditions(LoginPreconditions):
    """前置条件"""

    @staticmethod
    def enter_message_page(reset=False):
        """进入消息页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page(reset)

    @staticmethod
    def enter_private_chat_setting_page(reset=False):
        """进入单聊设置页面"""
        Preconditions.enter_private_chat_page(reset)
        chat = SingleChatPage()
        chat.click_setting()
        setting = SingleChatSetPage()
        setting.wait_for_page_load()


class MsgPrivateChatMsgList(TestCase):
    """
    模块：单聊->消息列表
    文件位置：全量/10.整理全量测试用例---黄彩最.xlsx
    表格：单聊
    """

    @classmethod
    def setUpClass(cls):
        pass

    def default_setUp(self):
        """确保每个用例运行前在消息页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        else:
            current_mobile().reset_app()
            Preconditions.enter_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_MsgList_0001(self):
        """消息-消息列表进入"""
        # 1、点击消息
        mess = MessagePage()
        mess.open_message_page()
        if not mess.is_on_this_page():
            raise AssertionError("未成功进入消息列表页面")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_MsgList_0002(self):
        """消息-消息列表界面+功能页面元素检查"""
        # 1、点击消息
        mess = MessagePage()
        mess.open_message_page()
        # 2、点击右上角的+号按钮
        mess.click_add_icon()
        time.sleep(1)
        # 下拉出“新建消息”、“免费短信”、“发起群聊”、分组群发、“扫一扫”，入口
        mess.page_should_contain_text("新建消息")
        mess.page_should_contain_text("免费短信")
        mess.page_should_contain_text("发起群聊")
        mess.page_should_contain_text("扫一扫")
        mess.driver.back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_MsgList_0004(self):
        """消息-消息列表界面新建消息页面元素检查"""
        # 1、点击消息右上角+按钮
        mess = MessagePage()
        mess.open_message_page()
        mess.click_add_icon()
        # 2、查看新建消息页面元素
        # 左上角有返回按钮，左上角显示新建消息标题，下方有搜索输入框，
        # 和通讯录入口，全量联系人列表，左侧显示姓名首字母排序、右侧显示索引字母排序。
        mess.click_new_message()
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        scp.page_contain_element('返回')
        scp.page_contain_element('选择联系人')
        scp.page_contain_element('搜索或输入手机号')
        scp.page_contain_element('右侧字母索引')
        if not scp.is_right_letters_sorted():
            raise AssertionError("右侧字母索引未排序")
        scp.page_contain_element('左侧字母索引')
        if not scp.is_left_letters_sorted():
            raise AssertionError("左侧字母索引未排序")
        # 3、滑动屏幕, 搜索栏常驻顶端
        scp.page_up()
        scp.page_up()
        scp.page_contain_element('搜索或输入手机号')
        scp.click_back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_MsgList_0005(self):
        """消息-消息列表界面新建消息页面返回操作"""
        # 1、点击右上角的+号按钮，成功进入新建消息界面
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        # 2、点击左上角返回按钮，退出新建消息，返回消息列表
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        scp.click_back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_MsgList_0006(self):
        """消息-消息列表界面新建消息页面返回操作"""
        # 1、点击右上角的+号按钮
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        # 2、点击手机系统内置返回返回按钮
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        scp.driver.back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_MsgList_0007(self):
        """资料页发起聊天"""
        # 1、在“联系人资料”页 点击【消息】,进入“个人会话”窗口
        Preconditions.enter_private_chat_page()
        # 返回消息列表页面
        chat = SingleChatPage()
        mess = MessagePage()
        chat.click_back()
        ContactDetailsPage().click_back()
        mess.open_message_page()
        mess.wait_for_page_load()

    @staticmethod
    def setUp_test_Msg_PrivateChat_MsgList_0008():
        """消息列表点击消息记录前，先发送一条消息"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.input_message("hello")
        chat.send_message()
        chat.click_back()
        ContactDetailsPage().click_back()
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_MsgList_0008(self):
        """消息-消息列表进入到会话页面"""
        # 1、在消息列表点击消息记录，进入到会话页面
        mess = MessagePage()
        mess.click_msg_by_content("hello")
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_back()
        mess.wait_for_page_load()

    @staticmethod
    def setUp_test_Msg_PrivateChat_MsgList_0010():
        """消息列表点击消息记录前，先发送一条消息"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.input_message("hello")
        chat.send_message()
        chat.click_back()
        ContactDetailsPage().click_back()
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_MsgList_0010(self):
        """消息-消息列表-消息列表显示未发送成功"""
        # 1、 在会话页面输入文本消息
        mess = MessagePage()
        mess.click_msg_by_content("hello")
        chat = SingleChatPage()
        chat.wait_for_page_load()
        # 断网
        current_mobile().set_network_status(0)
        chat.input_message("MsgList_0010")
        # 2、点击发送
        chat.send_message()
        if not chat.is_msg_send_fail():
            raise AssertionError("断网发送消息，在聊天会话窗无发送失败标志")
        # 3、点击返回消息列表
        chat.click_back()
        mess.wait_for_page_load()
        if not mess.is_iv_fail_status_present():
            raise AssertionError("断网发送消息，在消息列表无发送失败标志")

    @staticmethod
    def tearDown_test_Msg_PrivateChat_MsgList_0010():
        """恢复网络连接"""
        current_mobile().set_network_status(6)

    @staticmethod
    def setUp_test_Msg_PrivateChat_MsgList_0012():
        """消息列表点击消息记录前，先发送一条消息"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.clear_msg()
        chat.input_message("hello")
        chat.send_message()
        chat.click_back()
        ContactDetailsPage().click_back()
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_MsgList_0012(self):
        """消息-消息列表-消息列表显示未发送成功"""
        # 1、 在会话页面输入文本消息
        mess = MessagePage()
        mess.click_msg_by_content("hello")
        chat = SingleChatPage()
        chat.wait_for_page_load()
        # 断网
        current_mobile().set_network_status(0)
        chat.input_message("MsgList_0012")
        # 2、点击发送
        chat.send_message()
        if not chat.is_msg_send_fail():
            raise AssertionError("断网发送消息，在聊天会话窗无发送失败标志")
        # 3、点击返回消息列表
        chat.click_back()
        mess.wait_for_page_load()
        if not mess.is_iv_fail_status_present():
            raise AssertionError("断网发送消息，在消息列表无发送失败标志")
        mess.click_msg_by_content("MsgList_0012")
        # 恢复网络重发消息
        current_mobile().set_network_status(6)
        chat.repeat_send_msg()
        chat.click_sure_repeat_msg()
        chat.click_back()
        mess.wait_for_page_load()
        if mess.is_iv_fail_status_present():
            raise AssertionError("恢复网络重发消息，在消息列表依然存在发送失败标志")

    @staticmethod
    def tearDown_test_Msg_PrivateChat_MsgList_0012():
        """恢复网络连接"""
        current_mobile().set_network_status(6)

    @staticmethod
    def setUp_test_Msg_PrivateChat_MsgList_0013():
        """消息列表点击消息记录前，先发送一条消息"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        msg = "哈哈" * 30
        chat.input_message(msg)
        chat.send_message()
        chat.click_back()
        ContactDetailsPage().click_back()
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_MsgList_0013(self):
        """消息-消息列表-消息列表中文本消息预览"""
        # 1、查看消息列表中一对一文本消息记录
        mess = MessagePage()
        # 消息记录左面显示头像，右侧显示时间，中间上方显示发送消息人的名称，
        mess.page_contain_element('消息头像')
        mess.page_contain_element('消息时间')
        mess.page_contain_element('消息名称')
        # 下方显示文本内容，文本过长时以省略号显示
        mess.page_contain_element('消息简要内容')
        mess.msg_is_contain_ellipsis()


class MsgPrivateChatMsgSetting(TestCase):
    """
    模块：单聊->单聊设置
    文件位置：全量/10.整理全量测试用例---黄彩最.xlsx
    表格：单聊
    """

    @classmethod
    def setUpClass(cls):
        pass

    def default_setUp(self):
        """确保每个用例运行前在单聊设置页面"""
        Preconditions.select_mobile('Android-移动')
        setting = SingleChatSetPage()
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_setting_page()
        if setting.is_on_this_page():
            return
        else:
            current_mobile().reset_app()
            Preconditions.enter_private_chat_setting_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0001(self):
        """消息—一对一消息会话—设置"""
        setting = SingleChatSetPage()
        setting.click_back()
        chat = SingleChatPage()
        # 1.点击右上角的设置按钮,进入聊天设置页面
        chat.click_setting()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0002(self):
        """消息—一对一消息会话—设置页面头像转跳"""
        # 1. 点击联系人头像,进入到联系人详情页。
        setting = SingleChatSetPage()
        setting.click_avatar()
        detail = ContactDetailsPage()
        detail.wait_for_page_load()
        # 回到设置页面
        detail.click_message_icon()
        chat = SingleChatPage()
        chat.click_setting()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0007(self):
        """消息-一对一消息会话-设置页面查找聊天内容"""
        # 1. 点击下方的查找聊天内容按钮, 跳到搜索页面
        setting = SingleChatSetPage()
        setting.search_chat_record()
        fcrp = FindChatRecordPage()
        fcrp.wait_for_page_load()
        fcrp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_Msg_PrivateChat_Setting_0008(self):
        """消息-一对一消息会话-设置页面查找聊天内容"""
        # 先发送消息
        setting = SingleChatSetPage()
        setting.click_back()
        chat = SingleChatPage()
        msg = 'hehe'
        chat.input_message(msg)
        chat.send_message()
        chat.click_setting()
        # 1. 点击下方的查找聊天内容按钮
        setting.search_chat_record()
        # 2. 搜索已接收或发送消息的关键字
        fcrp = FindChatRecordPage()
        fcrp.wait_for_page_load()
        fcrp.input_search_message(msg)
        self.assertTrue(fcrp.is_element_exit('发送人头像'))
        self.assertTrue(fcrp.is_element_exit('发送人名称'))
        self.assertTrue(fcrp.is_element_exit('发送的内容'))
        self.assertTrue(fcrp.is_element_exit('发送的时间'))
        # 3.点击任意一个搜索到的聊天信息
        fcrp.click_record()
        chat.click_setting()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_Msg_PrivateChat_Setting_0009(self):
        """消息-一对一消息会话-设置页面查找不存在的聊天内容"""
        # 1. 点击下方的查找聊天内容按钮
        setting = SingleChatSetPage()
        setting.search_chat_record()
        # 2. 搜索不存在的关键字
        fcrp = FindChatRecordPage()
        times = 20
        while times > 0:
            msg = uuid.uuid4().__str__()
            fcrp.input_search_message(msg)
            try:
                fcrp.page_should_contain_text("无搜索结果")
                break
            except:
                times = times - 1
                continue
        if times == 0:
            raise AssertionError("搜索异常，页面无‘无搜索结果’文本")
        fcrp.click_back()
        setting.wait_for_page_load()

    @staticmethod
    def public_send_file(file_type):
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        setting = SingleChatSetPage()
        setting.click_back()
        chat = SingleChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
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
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_Msg_PrivateChat_Setting_0010(self):
        """消息-一对一消息会话-设置页面查找聊天文件"""
        self.public_send_file('.txt')
        chat = SingleChatPage()
        # 1. 点击右上角个人设置按钮
        chat.click_setting()
        setting = SingleChatSetPage()
        # 2. 点击下方的查找聊天内容按钮
        setting.search_chat_record()
        # 3.点击文件
        fcrp = FindChatRecordPage()
        fcrp.click_file()
        file = ChatFilePage()
        file.wait_for_page_load()
        file.page_should_contain_file()
        file.click_back()
        fcrp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_Msg_PrivateChat_Setting_0011(self):
        """消息-一对一消息会话-设置页面查找聊天文件"""
        # 1. 点击右上角个人设置按钮
        setting = SingleChatSetPage()
        # 2. 点击下方的查找聊天内容按钮
        setting.search_chat_record()
        # 3.点击文件
        fcrp = FindChatRecordPage()
        fcrp.click_file()
        file = ChatFilePage()
        file.wait_for_page_load()
        file.clear_file_record()
        file.page_should_contain_text("暂无文件")
        file.click_back()
        fcrp.click_back()
        setting.wait_for_page_load()

    @staticmethod
    def public_send_video():
        """在聊天会话页面发送一个视频"""
        setting = SingleChatSetPage()
        setting.click_back()
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 选择一个视频发送
        cpp.select_video()
        cpp.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_Msg_PrivateChat_Setting_0012(self):
        """消息-一对一消息会话-设置页面查找聊天图片与视频"""
        self.public_send_video()
        chat = SingleChatPage()
        chat.click_setting()
        # 1.点击查找聊天内容
        setting = SingleChatSetPage()
        setting.search_chat_record()
        # 2.点击图片与视频
        fcrp = FindChatRecordPage()
        fcrp.click_pic_video()
        pv = PicVideoPage()
        pv.wait_for_page_load()
        if not pv.is_exist_video():
            raise AssertionError("发送视频后在聊天记录的图片与视频页面无视频")
        pv.click_back()
        fcrp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_Msg_PrivateChat_Setting_0013(self):
        """消息-一对一消息会话-设置页面查找聊天图片与视频"""
        # 1.点击查找聊天内容
        setting = SingleChatSetPage()
        setting.search_chat_record()
        # 2.点击图片与视频
        fcrp = FindChatRecordPage()
        fcrp.click_pic_video()
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.clear_record()
        pv.page_should_contain_text("暂无内容")
        pv.click_back()
        fcrp.click_back()
        setting.wait_for_page_load()
