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
    文件位置：113整理全量测试用例-黄彩最.xlsx
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

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_1315(self):
        """新建消息"""
        # 1、点击右上角+号 - 新建消息
        mess = MessagePage()
        mess.open_message_page()
        mess.click_add_icon()
        mess.click_new_message()
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        # 页面元素有为号码输入或搜索框，黄页通讯录列表（含名称与号码、按名称拼音首字母排列）
        scp.page_contain_element('搜索或输入手机号')
        scp.page_contain_element('local联系人')
        scp.page_contain_element('左侧字母索引')
        if not scp.is_left_letters_sorted():
            raise AssertionError("左侧字母索引未排序")
        scp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_1317(self):
        """新建消息"""
        # 1、点击右上角+号 - 新建消息
        mess = MessagePage()
        mess.open_message_page()
        mess.click_add_icon()
        mess.click_new_message()
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        # 2、选中黄页内一名联系人，进入聊天窗口
        scp.click_one_local_contacts()
        chat = SingleChatPage()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        chat.wait_for_page_load()
        chat.click_back()


class MsgPrivateChatMsgSetting(TestCase):
    """
    模块：单聊->单聊设置
    文件位置：113整理全量测试用例-黄彩最.xlsx
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

    @tags('ALL', 'SMOKE', 'CMCC')
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

    @tags('ALL', 'SMOKE', 'CMCC')
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

    @tags('ALL', 'SMOKE', 'CMCC')
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

    @tags('ALL', 'SMOKE', 'CMCC')
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

    @tags('ALL', 'SMOKE', 'CMCC')
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

    @tags('ALL', 'SMOKE', 'CMCC')
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

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0020(self):
        """ 一对一聊天设置创建群聊 """
        # 1.点击+添加成员,进入选择成员页面
        setting = SingleChatSetPage()
        setting.click_add_icon()
        scp = SelectContactsPage()
        scp.wait_for_page_local_contact_load()
        scp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0021(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name()
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                break
        # 4.点击反回聊天设置
        slcp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0022(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 选择一个成员
        names = slcp.get_contacts_name()
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                break
        # 4.点击确定,进入群聊名称设置
        slcp.click_sure()
        name_set = CreateGroupNamePage()
        name_set.wait_for_page_load()
        name_set.click_back()
        slcp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0023(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.搜索选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name()
        for name in names:
            slcp.search_and_select_one_member_by_name(name)
        # 4.点击确定,进入群聊名称设置
        slcp.click_sure()
        name_set = CreateGroupNamePage()
        name_set.wait_for_page_load()
        name_set.click_back()
        slcp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0024(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 选择一个成员
        names = slcp.get_contacts_name()
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                break
        # 4.点击确定进入群聊名称设置
        slcp.click_sure()
        name_set = CreateGroupNamePage()
        name_set.wait_for_page_load()
        # 5.再点击返回聊天设置
        name_set.click_back()
        slcp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0025(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.搜索选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 选择多个成员
        names = slcp.get_contacts_name()
        for name in names:
            slcp.search_and_select_one_member_by_name(name)
        # 4.点击确定进入群聊名称设置
        slcp.click_sure()
        name_set = CreateGroupNamePage()
        name_set.wait_for_page_load()
        # 5.再点击返回聊天设置
        name_set.click_back()
        slcp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0026(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        cur_name = setting.get_name()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.搜索选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 选择一个成员
        names = slcp.get_contacts_name()
        if cur_name in names:
            names.remove(cur_name)
        if '本机' in names:
            names.remove('本机')
        for name in names:
            slcp.search_and_select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                if not slcp.contacts_is_selected(name):
                    raise AssertionError("联系人未被选中")
                # 4.点击左上角选择的成员名称或再次点击列表里该成员名称
                slcp.select_one_member_by_name(name)
                if slcp.contacts_is_selected(name):
                    raise AssertionError("搜索选择一个成员后再次点击列表里该成员，依然是选择状态")
                break
        slcp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0027(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        cur_name = setting.get_name()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 选择一个成员
        names = slcp.get_contacts_name()
        if cur_name in names:
            names.remove(cur_name)
        if '本机' in names:
            names.remove('本机')
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                if not slcp.contacts_is_selected(name):
                    raise AssertionError("联系人未被选中")
                # 4.点击左上角选择的成员名称或再次点击列表里该成员名称
                slcp.select_one_member_by_name(name)
                if slcp.contacts_is_selected(name):
                    raise AssertionError("搜索选择一个成员后再次点击列表里该成员，依然是选择状态")
                break
        slcp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0028(self):
        """ 一对一聊天设置创建群聊,无网络 """
        setting = SingleChatSetPage()
        cur_name = setting.get_name()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name()
        if cur_name in names:
            names.remove(cur_name)
        if '本机' in names:
            names.remove('本机')
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                break
        # 4.点击确定，再点击创建
        slcp.click_sure()
        # 断网
        current_mobile().set_network_status(0)
        name_set = CreateGroupNamePage()
        name_set.wait_for_page_load()
        name_set.click_sure()
        if not name_set.is_toast_exist("网络不可用", timeout=6):
            raise AssertionError("无网络不可用提示")
        name_set.click_back()
        slcp.click_back()
        setting.wait_for_page_load()

    @staticmethod
    def tearDown_test_Msg_PrivateChat_Setting_0028():
        """恢复网络连接"""
        current_mobile().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0029(self):
        """ 一对一聊天设置创建群聊,无网络 """
        setting = SingleChatSetPage()
        cur_name = setting.get_name()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name()
        if cur_name in names:
            names.remove(cur_name)
        if '本机' in names:
            names.remove('本机')
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                break
        # 4.点击确定，统一群聊名称，再点击创建
        slcp.click_sure()
        name_set = CreateGroupNamePage()
        name_set.wait_for_page_load()
        group_name = 'testGroup'
        name_set.input_group_name(group_name)
        name_set.click_sure()
        group_chat = GroupChatPage()
        group_chat.wait_for_page_load()
        if group_name not in group_chat.get_group_name():
            raise AssertionError("群聊的名称显示不是所编辑的名称 " + group_name)
        # 清除测试数据
        group_chat.click_setting()
        group_set = GroupChatSetPage()
        group_set.click_delete_and_exit()
        group_set.click_sure()
        chat.wait_for_page_load()
        chat.click_setting()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0031(self):
        """ 点对点建群"""
        setting = SingleChatSetPage()
        setting.click_back()
        # 1.长按文本消息
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.clear_msg()
        chat.input_message("hello")
        chat.send_message()
        chat.press_mess("hello")
        # 弹出多功能列表，包含复制、转发、删除、撤回、收藏、（移动用户有/异网无）转为短信发送、多选
        chat.page_should_contain_text("复制")
        chat.page_should_contain_text("转发")
        chat.page_should_contain_text("删除")
        chat.page_should_contain_text("撤回")
        chat.page_should_contain_text("收藏")
        chat.page_should_contain_text("转为短信发送")
        chat.page_should_contain_text("多选")
        chat.driver.back()
        chat.click_setting()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0033(self):
        """ 输入框中输入表情消息不发送，进入查找聊天内容后是否还显示草稿"""
        setting = SingleChatSetPage()
        setting.click_back()
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.input_message("hello")
        chat.send_message()
        if not chat.is_open_expression():
            chat.open_expression()
        # 2、在聊天输入框中输入数十个表情
        chat.select_expression(n=10)
        # 3、点击设置按钮
        chat.click_setting()
        # 4.点击查找聊天内容
        setting.search_chat_record()
        # 5.输入框中输入已存在会话中的关键词
        fcrp = FindChatRecordPage()
        fcrp.wait_for_page_load()
        fcrp.input_search_message('hello')
        # 6.点击任意一条搜索结果
        fcrp.click_record()
        chat.wait_for_page_load()
        chat.page_should_contain_text('说点什么...')
        chat.click_setting()
        setting.wait_for_page_load()

    @staticmethod
    def public_input_mess(msg):
        """Msg_PrivateChat_Setting_0034-0038共有部分提取"""
        setting = SingleChatSetPage()
        setting.click_back()
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.input_message("hello")
        chat.send_message()
        # 2、在聊天输入框中输入msg
        chat.input_message(msg)
        # 3、点击设置按钮
        chat.click_setting()
        # 4.点击查找聊天内容
        setting.search_chat_record()
        # 5.输入框中输入已存在会话中的关键词
        fcrp = FindChatRecordPage()
        fcrp.wait_for_page_load()
        fcrp.input_search_message('hello')
        # 6.点击任意一条搜索结果
        fcrp.click_record()
        chat.wait_for_page_load()
        chat.page_should_contain_text('说点什么...')
        chat.click_setting()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0034(self):
        """ 输入框中输入文字不发送，进入查找聊天内容后是否还显示草稿"""
        self.public_input_mess("您好")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0035(self):
        """ 输入框中输入数字消息不发送，进入查找聊天内容后是否还显示草稿"""
        self.public_input_mess("123456789")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0036(self):
        """ 输入框中输入字母消息不发送，进入查找聊天内容后是否还显示草稿"""
        self.public_input_mess("abcdef")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0037(self):
        """ 输入框中输入字符消息不发送，进入查找聊天内容后是否还显示草稿"""
        self.public_input_mess("@#$%%%^&")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_Setting_0038(self):
        """ 输入框中输入各种混合消息体不发送，进入查找聊天内容后是否还显示草稿"""
        self.public_input_mess("abc123@#$%^&")


class MsgContactSelector(TestCase):
    """
    模块：单聊->联系人选择器
    文件位置：113整理全量测试用例-黄彩最.xlsx
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

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_1183(self):
        """ 进入新建消息是否正常"""
        # 1.点击右上角的+
        mess = MessagePage()
        mess.click_add_icon()
        # 2.点击新建消息
        mess.click_new_message()
        # 3.查看页面展示
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        # 左上角标题：选择联系人；搜索栏缺省文字：搜索或输入手机号；
        # 选择和通讯录联系人；下方为本地联系人列表
        scp.page_should_contain_text("选择联系人")
        scp.page_should_contain_text("搜索或输入手机号")
        scp.page_should_contain_text("选择和通讯录联系人")
        scp.page_contain_element("local联系人")
        scp.click_back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_1194(self):
        """ 进入免费/发送短信查看展示页面"""
        # 1.点击右上角的+
        mess = MessagePage()
        mess.click_add_icon()
        # 2.点击免费/发送短信
        mess.click_free_sms()
        # 首次进入会弹出“欢迎使用免费短信”/“欢迎使用短信”弹框，点击确定后直接进入联系人选择器，
        # 非首次进入的直接进入联系人选择器
        try:
            time.sleep(1)
            mess.page_should_contain_text("欢迎使用免费短信")
            mess.click_text("确定")
        except:
            pass
        # 3.查看页面展示
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        # 左上角标题：选择联系人；搜索栏缺省文字：搜索或输入手机号；
        # 选择和通讯录联系人；下方为本地联系人列表
        scp.page_should_contain_text("选择联系人")
        scp.page_should_contain_text("搜索或输入手机号")
        scp.page_should_contain_text("选择和通讯录联系人")
        scp.page_contain_element("local联系人")
        scp.click_back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_1205(self):
        """ 最近聊天选择器：单聊内转发消息"""
        # 1、在聊天会话页面，长按可转发的消息，是否可以跳转到联系人选择器页面
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.input_message("hehe")
        chat.send_message()
        chat.press_mess('hehe')
        chat.click_to_do('转发')
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_back()
        chat.click_back()
        ContactDetailsPage().click_back()
        ContactsPage().open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_1206(self):
        """ 最近聊天选择器：单聊内转发消息--选择一个群"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.input_message("hello")
        chat.send_message()
        chat.press_mess('hello')
        chat.click_to_do('转发')
        # 1、在联系人选择器页面，点击选择一个群
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 2、进入到群聊列表展示页面，顶部的搜索文案是否展示为：搜索群聊
        sogp.page_should_contain_text("搜索群组")
        group_names = sogp.get_group_name()
        sogp.click_search_group()
        # 3、在顶部的搜索框中输入搜索条件，不存在搜索结果时下方展示文案是否是：无搜索结果
        times = 60
        while times > 0:
            msg = uuid.uuid4().__str__()
            sogp.input_search_keyword(msg)
            time.sleep(1)
            if sogp.is_text_present('无搜索结果'):
                break
            times -= 1
        if times == 0:
            raise AssertionError("无 ‘无搜索结果’")
        if not group_names:
            raise AssertionError('无群，请创建！')
        # 4、存在搜索结果时，展示的搜索结果是否符合需求
        sogp.input_search_keyword(group_names[0])
        time.sleep(1)
        sogp.page_should_contain_text(group_names[0])
        # 5、点击选中一个搜索结果，是否会弹出确认弹窗
        sogp.click_search_result()
        time.sleep(2)
        if not sogp.is_text_present("发送给"):
            raise AssertionError("转发消息给群组时，无含‘发送给’文本的弹窗")
        sogp.click_text("确定")
        chat.wait_for_page_load()
        chat.click_back()
        ContactDetailsPage().click_back()
        ContactsPage().open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_1207(self):
        """ 最近聊天选择器：单聊内转发消息--选择本地联系人"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.input_message("hehe")
        chat.send_message()
        chat.press_mess('hehe')
        chat.click_to_do('转发')
        # 1、在联系人选择器页面，点击选择本地联系人，跳转到本地联系人列表展示页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 2、当前页面左上角展示的文案是否符合需求展示为：选择联系人
        slcp.page_should_contain_text("选择联系人")
        # 3、顶部搜索框中，默认展示的文案是否是：搜索或输入手机号
        slcp.page_should_contain_text('搜索或输入手机号')
        names = slcp.get_contacts_name()
        # 4、在搜索框中输入搜索条件，检查不存在搜索结果时，下方是否展示：无搜索结果
        times = 60
        while times > 0:
            msg = uuid.uuid4().__str__()
            slcp.search(msg)
            time.sleep(1)
            if not slcp.is_search_result(msg):
                break
            times -= 1
        if times == 0:
            raise AssertionError("无 ‘无搜索结果’")
        if not names:
            raise AssertionError('无联系人，请创建！')
        # 5、在搜索框中输入搜索条件，存在搜索结果时，下方展示的搜索结果是否符合需求
        # 6、点击选中搜索出的结果，是否会弹出确认弹窗
        slcp.search_and_select_one_member_by_name(names[0])
        time.sleep(2)
        if not slcp.is_text_present("发送给"):
            raise AssertionError("转发消息给本地联系人时，无含‘发送给’文本的弹窗")
        slcp.click_text("确定")
        chat.wait_for_page_load()
        chat.click_back()
        ContactDetailsPage().click_back()
        ContactsPage().open_message_page()


class MsgPrivateChatDialog(TestCase):
    """
    模块：单聊->单聊聊天会话
    文件位置：113整理全量测试用例-黄彩最.xlsx
    表格：单聊
    """

    @classmethod
    def setUpClass(cls):
        pass

    def default_setUp(self):
        """确保每个用例运行前在单聊会话页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().reset_app()
            Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_1277(self):
        """ 页面样式"""
        # 1、进入一对一天聊天界面,页面右下角出现表情选择按钮
        chat = SingleChatPage()
        chat.page_should_contains_element('打开表情')

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_1278(self):
        """ 页面样式"""
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        # 2、点击聊天界面右下角的表情选择按钮
        if not chat.is_open_expression():
            chat.open_expression()
        time.sleep(1)
        chat.page_should_contains_element('表情id')
        chat.page_should_contains_element('表情集选择栏')
        chat.page_should_contains_element('翻页小圆点')
        chat.page_should_contains_element('删除表情按钮')
        # 表情‘键盘’
        chat.page_should_contains_element('关闭表情')
        chat.close_expression()

