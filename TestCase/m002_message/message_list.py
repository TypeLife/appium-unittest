import unittest

from selenium.common.exceptions import TimeoutException

import preconditions
from library.core.utils.applicationcache import current_mobile, current_driver
from pages.call.Call import CallPage
from pages.components import BaseChatPage
from pages.contacts import OfficialAccountPage, SearchOfficialAccountPage
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
import time


class Preconditions(LoginPreconditions):
    """前置条件"""

    @staticmethod
    def enter_single_chat_page(name):
        """进入单聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name(name)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def enter_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            # 等待选择联系人页面加载
            flag = scg.wait_for_page_load()
            if not flag:
                scg.click_back()
                time.sleep(2)
                mp.click_add_icon()
                mp.click_group_chat()
            else:
                break
            n = n + 1
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def create_message_record(messages):
        """创造消息记录"""

        for title, text in messages:
            Preconditions.enter_single_chat_page(title)
            scp = SingleChatPage()
            # 输入文本信息
            scp.input_text_message(text)
            time.sleep(2)
            scp.send_text()
            scp.click_back()

    @staticmethod
    def create_contacts_by_name(name, number):
        """检查是否存在指定联系人，没有则创建"""

        mp = MessagePage()
        mp.open_contacts_page()
        ctp = ContactsPage()
        ctp.wait_for_page_load()
        ctp.click_search_box()
        cls = ContactListSearchPage()
        cls.wait_for_page_load()
        cls.input_search_keyword(name)
        time.sleep(2)
        if cls.is_exist_contacts():
            cls.click_back()
        else:
            cls.click_back()
            ctp.wait_for_page_load()
            ctp.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            ccp.input_name(name)
            time.sleep(2)
            ccp.input_number(number)
            ccp.save_contact()
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_back_icon()
        ctp.wait_for_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def create_system_message():
        """创造系统消息"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            # 等待选择联系人页面加载
            flag = scg.wait_for_page_load()
            if not flag:
                scg.click_back()
                time.sleep(2)
                mp.click_add_icon()
                mp.click_group_chat()
            else:
                break
            n = n + 1
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        slc.select_local_contacts(2)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name("群聊999")
        cgnp.click_sure()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_delete_and_exit()
        gcsp.click_sure()
        mp.wait_for_message_list_load()

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """确保应用在消息页面"""

        if not reset_required:
            message_page = MessagePage()
            if message_page.is_on_this_page():
                return
            else:
                try:
                    current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
                except:
                    pass
                current_mobile().launch_app()
            try:
                message_page.wait_until(
                    condition=lambda d: message_page.is_on_this_page(),
                    timeout=3
                )
                return
            except TimeoutException:
                pass
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        login_num = Preconditions.login_by_one_key_login()
        return login_num

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()


class MessageListAllTest(TestCase):
    """
    模块：消息列表
    文件位置：1.1.3全量测试用例->113全量用例--肖立平.xlsx
    表格：消息列表
    Author:刘晓东
    """

    def default_setUp(self):
        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0024(self):
        """消息列表进入"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前页面不在消息列表模块
        mp.open_me_page()
        me_page = MePage()
        me_page.wait_for_me_page_load()
        time.sleep(2)
        # 进入消息列表
        mp.open_message_page()
        # 1.等待消息列表页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0025(self):
        """登录之后消息列表进入"""

        # 重启客户端
        current_mobile().launch_app()
        mp = MessagePage()
        # 1.登录客户端,等待消息列表页面加载
        mp.wait_for_page_load()
        # 2.底部消息图标是否高亮显示
        self.assertEquals(mp.message_icon_is_selected(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0026(self):
        """消息列表载入"""

        mp = MessagePage()
        # 设置手机网络断开
        mp.set_network_status(0)
        # 1.重启客户端,等待消息列表页加载,验证页面搜索,底部tab,右上角+是否可点击
        current_mobile().launch_app()
        mp.wait_for_page_load()
        self.assertEquals(mp.search_box_is_enabled(), True)
        self.assertEquals(mp.message_icon_is_enabled(), True)
        self.assertEquals(mp.call_icon_is_enabled(), True)
        self.assertEquals(mp.workbench_icon_is_enabled(), True)
        self.assertEquals(mp.contacts_icon_is_enabled(), True)
        self.assertEquals(mp.me_icon_is_enabled(), True)
        self.assertEquals(mp.add_icon_is_enabled(), True)
        # 2.搜索框下方提示当前网络不可用，请检查网络设置或稍后重试
        self.assertEquals(mp.is_exist_network_anomaly(), True)
        # 3.底部消息图标是否高亮显示
        self.assertEquals(mp.message_icon_is_selected(), True)

    @staticmethod
    def tearDown_test_message_list_total_quantity_0026():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0027(self):
        """消息列表进入到会话页面"""

        mp = MessagePage()
        # 等待消息列表页加载
        mp.wait_for_page_load()
        # 确保消息列表有消息记录
        name = "大佬1"
        Preconditions.enter_single_chat_page(name)
        scp = SingleChatPage()
        text = "111"
        scp.input_text_message(text)
        time.sleep(2)
        scp.send_text()
        scp.click_back()
        mp.wait_for_page_load()
        # 1.进入到会话页面
        mp.choose_chat_by_name(name)
        scp.wait_for_page_load()
        # 返回消息列表页
        scp.click_back()

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_message_list_total_quantity_0029(self):
        """消息列表未读消息清空"""

        # 重置当前app
        Preconditions.make_already_in_message_page(True)
        mp = MessagePage()
        mp.wait_for_message_list_load()
        # 确保消息列表有未读消息
        self.assertEquals(mp.is_exist_unread_messages(), True)
        # 清空未读消息
        mp.clear_up_unread_messages()
        # 1.验证未读消息小红点标识是否消失
        self.assertEquals(mp.is_exist_unread_messages(), False)

    @unittest.skip("暂时难以实现,跳过")
    def test_message_list_total_quantity_0034(self):
        """消息列表订阅号红点显示"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 切换到标签页：通讯录
        mp.open_contacts_page()
        cp = ContactsPage()
        time.sleep(2)
        # 进入公众号页面
        cp.click_official_account_icon()
        oap = OfficialAccountPage()
        oap.wait_for_page_load()
        # 进入搜索公众号页面
        oap.click_add()
        soap = SearchOfficialAccountPage()
        soap.wait_for_page_load()
        name = "移周刊"
        soap.input_search_key(name)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0038(self):
        """消息列表网络异常显示"""

        mp = MessagePage()
        # 设置手机网络断开
        mp.set_network_status(0)
        time.sleep(5)
        # 1.是否提示当前网络不可用，请检查网络设置或稍后重试
        self.assertEquals(mp.is_exist_network_anomaly(), True)
        # 2.等待消息页面加载
        mp.wait_for_page_load()

    @staticmethod
    def tearDown_test_message_list_total_quantity_0038():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0040(self):
        """消息列表显示未发送成功"""

        mp = MessagePage()
        # 确保消息页面当前没有未发送成功消息标记
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()
        # 进入聊天会话页面
        name = "大佬1"
        Preconditions.enter_single_chat_page(name)
        # 设置手机网络断开
        mp.set_network_status(0)
        scp = SingleChatPage()
        text = "222"
        # 1.输入文本信息
        scp.input_text_message(text)
        time.sleep(2)
        scp.send_text()
        # 2.是否显示消息发送失败标识
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        scp.click_back()
        mp.wait_for_page_load()
        # 3.消息预览中是否显示未发送成功消息标记
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_message_list_total_quantity_0040():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0043(self):
        """消息列表网络异常显示"""

        mp = MessagePage()
        # 设置手机网络断开
        mp.set_network_status(0)
        time.sleep(5)
        # 1.是否提示当前网络不可用，请检查网络设置或稍后重试
        self.assertEquals(mp.is_exist_network_anomaly(), True)
        # 2.等待消息页面加载
        mp.wait_for_page_load()

    @staticmethod
    def tearDown_test_message_list_total_quantity_0043():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0044(self):
        """导航栏-点击导航条切换页签"""

        mp = MessagePage()
        # 1.等待消息页加载
        mp.wait_for_page_load()
        # 2.切换底部标签
        # 切换通话标签
        mp.open_call_page()
        clp = CallPage()
        time.sleep(2)
        if clp.is_exist_specified_prompt():
            clp.click_multi_party_telephone()
            time.sleep(2)
        if clp.is_exist_know():
            clp.click_know()
            clp.click_back()
            time.sleep(2)
        clp.wait_for_page_load()
        # 切换工作台标签
        mp.open_workbench_page()
        wp = WorkbenchPage()
        wp.wait_for_page_load()
        # 切换通讯录标签
        mp.open_contacts_page()
        ctp = ContactsPage()
        ctp.wait_for_page_load()
        # 切换我标签
        mp.open_me_page()
        me_page = MePage()
        me_page.wait_for_me_page_load()
        # 切换消息标签
        mp.open_message_page()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_message_list_total_quantity_0045(self):
        """导航栏-首次进入查看导航栏"""

        # 重置当前app
        Preconditions.make_already_in_message_page(True)
        mp = MessagePage()
        # 1.等待消息页面加载
        mp.wait_for_page_load()
        # 2.导航栏是否显示有消息，通话，工作台，通讯录，我五个tab页
        self.assertEquals(mp.is_exist_message_icon(), True)
        self.assertEquals(mp.is_exist_call_icon(), True)
        self.assertEquals(mp.is_exist_workbench_icon(), True)
        self.assertEquals(mp.is_exist_contacts_icon(), True)
        self.assertEquals(mp.is_exist_me_icon(), True)
        # 消息标签是否高亮显示
        self.assertEquals(mp.message_icon_is_selected(), True)

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_message_list_total_quantity_0046(self):
        """验证首次登陆和飞信，进入消息页面（聊天为空），查看页面元素"""

        # 重置当前app
        Preconditions.make_already_in_message_page(True)
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 1.页面顶部是否展示全局搜索框
        self.assertEquals(mp.is_exist_search_box(), True)
        # 2.右上角是否有“+”号图标
        self.assertEquals(mp.is_exist_add_icon(), True)
        # 3.页面文案是否为“图文消息，一触即发”
        self.assertEquals(mp.is_exist_words(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0048(self):
        """消息列表界面消息列表页面元素检查"""

        mp = MessagePage()
        # 1.等待消息页加载
        mp.wait_for_page_load()
        # 2.消息图标高亮显示
        self.assertEquals(mp.message_icon_is_selected(), True)
        name = "啊" * 15
        number = "13566664567"
        Preconditions.create_contacts_by_name(name, number)
        # 确保有足够的消息记录可供滑动
        messages = [("大佬1", "1"),
                    ("大佬2", "2"),
                    ("大佬3", "3"),
                    ("大佬4", "4"),
                    ("给个红包1", "5"),
                    ("给个红包2", "6"),
                    ("给个红包3", "7"),
                    ("给个红包4", "8"),
                    (name, "9")]
        Preconditions.create_message_record(messages)
        # 列表中显示消息记录，消息左侧显示头像
        mp.is_exist_message_record()
        mp.is_exist_message_img()
        # 右侧显示时间，中间显示发送人和消息预览
        mp.is_exist_message_time()
        mp.is_exist_message_name()
        mp.is_exist_message_content()
        # 滑到消息记录顶端
        mp.slide_to_the_top()
        # 验证超过一屏可以滑动展示
        self.assertEquals(mp.is_slide_message_list(), False)
        # 发送人名称全部展示在消息列表上（名称长度最多为10汉字）
        # 验证一个能显示全名和一个不能显示全名的
        mp.slide_to_the_top()
        self.assertEquals(mp.message_list_is_exist_name("大佬1"), True)
        mp.slide_to_the_top()
        self.assertEquals(mp.message_list_is_exist_name(name), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0049(self):
        """消息列表界面新建消息页面返回操作"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        # 1.等待选择联系人页面加载
        slc.wait_for_page_load()
        # 2.退出新建消息，返回消息列表
        slc.click_back()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0054(self):
        """消息列表非第一个窗口长按置顶（Android）"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        time.sleep(5)
        # 滑到消息记录顶端
        mp.slide_to_the_top()
        # 取消当前页消息记录所有已置顶
        if mp.is_exist_message_name():
            mp.cancel_message_record_stick()
        # 确保当前页面至少两条记录,以便区分置顶效果
        messages = [("大佬1", "123"), ("大佬2", "456")]
        Preconditions.create_message_record(messages)
        time.sleep(2)
        # 置顶非第一条消息记录
        name = mp.top_message_recording_by_number(1)
        time.sleep(2)
        # 获取当前第一条消息名称
        top_name = mp.get_message_name_by_number(0)
        # 1.验证是否置顶成功，排在第一
        self.assertEquals(name, top_name)
        time.sleep(2)
        # 取消置顶该窗口
        mp.cancel_stick_message_recording_by_number(0)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0055(self):
        """消息列表窗口长按取消置顶（Android）"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        time.sleep(5)
        # 滑到消息记录顶端
        mp.slide_to_the_top()
        # 取消当前页消息记录所有已置顶
        if mp.is_exist_message_name():
            mp.cancel_message_record_stick()
        # 确保当前页面至少两条记录,以便区分取消置顶效果
        messages = [("大佬3", "111"), ("大佬4", "222")]
        Preconditions.create_message_record(messages)
        time.sleep(2)
        # 置顶第二条消息记录
        name = mp.top_message_recording_by_number(1)
        time.sleep(5)
        # 获取当前第一条消息名称
        current_top_name = mp.get_message_name_by_number(0)
        # 验证该窗口是否已被置顶
        self.assertEquals(name, current_top_name)
        # 取消置顶该窗口
        cancel_stick_name = mp.cancel_stick_message_recording_by_number(0)
        time.sleep(5)
        # 获取当前第二条消息名称
        current_second_name = mp.get_message_name_by_number(1)
        # 1.验证是否取消置顶成功
        self.assertEquals(cancel_stick_name, current_second_name)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0056(self):
        """消息列表窗口长按删除（Android）"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 确保消息列表有记录
        messages = [("大佬1", "111")]
        Preconditions.create_message_record(messages)
        time.sleep(2)
        # 删除指定消息记录
        mp.delete_message_record_by_name(messages[0][0])
        # 验证是否删除成功,在消息列表消失
        self.assertEquals(mp.current_message_list_is_exist_name(messages[0][0]), False)

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0065(self):
        """已开启免打扰的单聊，未收到新消息"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 消息列表如果已经存在消息免打扰图标,清空聊天记录
        if mp.is_exist_no_disturb_icon():
            mp.clear_message_record()
        # 确保消息列表有记录
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        # 输入文本信息
        scp.input_text_message("123")
        time.sleep(2)
        scp.send_text()
        time.sleep(2)
        scp.click_setting()
        scs = SingleChatSetPage()
        scs.wait_for_page_load()
        time.sleep(2)
        # 开启消息免打扰
        if not scs.is_selected_no_disturb():
            scs.click_no_disturb()
            time.sleep(4)
        scs.click_back()
        scp.wait_for_page_load()
        # 1.单聊会话页面是否显示消息免打扰图标
        self.assertEquals(scp.is_exist_no_disturb_icon(), True)
        scp.click_back()
        mp.wait_for_page_load()
        # 2.消息列表是否显示免打扰铃铛
        self.assertEquals(mp.is_exist_no_disturb_icon(), True)
        # 3.验证免打扰铃铛拖拽是否消除
        self.assertEquals(mp.is_clear_no_disturb_icon(), False)

    @staticmethod
    def tearDown_test_message_list_total_quantity_0065():
        """消息免打扰关闭"""

        mess = MessagePage()
        if not mess.is_on_this_page():
            preconditions.force_close_and_launch_app()
            mess.wait_for_page_load()
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.click_setting()
        scs = SingleChatSetPage()
        scs.wait_for_page_load()
        time.sleep(2)
        # 关闭消息免打扰
        if scs.is_selected_no_disturb():
            scs.click_no_disturb()
            time.sleep(4)
        scs.click_back()
        scp.wait_for_page_load()
        scp.click_back()
        mess.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0069(self):
        """已开启免打扰的群聊，未收到新消息"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 消息列表如果已经存在消息免打扰图标,清空聊天记录
        if mp.is_exist_no_disturb_icon():
            mp.clear_message_record()
            time.sleep(2)
        # 确保消息列表有记录
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 输入文本信息
        gcp.input_text_message("456")
        time.sleep(2)
        gcp.send_text()
        time.sleep(2)
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        time.sleep(2)
        # 开启消息免打扰
        if not gcs.get_switch_undisturb_status():
            gcs.click_switch_undisturb()
            time.sleep(4)
        gcs.click_back()
        gcp.wait_for_page_load()
        # 1.群聊会话页面是否显示消息免打扰图标
        self.assertEquals(gcp.is_exist_undisturb(), True)
        gcp.click_back()
        mp.wait_for_page_load()
        # 2.消息列表是否显示免打扰铃铛
        self.assertEquals(mp.is_exist_no_disturb_icon(), True)
        # 3.验证免打扰铃铛拖拽是否消除
        self.assertEquals(mp.is_clear_no_disturb_icon(), False)

    @staticmethod
    def tearDown_test_message_list_total_quantity_0069():
        """消息免打扰关闭"""

        mp = MessagePage()
        if not mp.is_on_this_page():
            preconditions.force_close_and_launch_app()
            mp.wait_for_page_load()
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        time.sleep(2)
        # 关闭消息免打扰
        if gcs.get_switch_undisturb_status():
            gcs.click_switch_undisturb()
            time.sleep(4)
        gcs.click_back()
        gcp.wait_for_page_load()
        gcp.click_back()
        mp.wait_for_page_load()

    @unittest.skip("新版本系统消息为气泡提示，暂时跳过")
    def test_message_list_total_quantity_0072(self):
        """在消息列表页面，接收到新的系统消息"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 消息列表如果已经存在消息红点,清空聊天记录
        if mp.is_exist_news_red_dot():
            mp.clear_message_record()
            time.sleep(2)
        # 在消息列表首页接收到新的系统消息
        Preconditions.create_system_message()
        # 1.验证是否存在红点提醒
        self.assertEquals(mp.is_exist_news_red_dot(), True)
        # 2.验证消息红点拖拽是否消除
        self.assertEquals(mp.is_clear_news_red_dot(), False)

    @staticmethod
    def tearDown_test_message_list_total_quantity_0072():
        """清除系统消息"""

        mp = MessagePage()
        if not mp.is_on_this_page():
            preconditions.force_close_and_launch_app()
            mp.wait_for_page_load()
        if mp.current_message_list_is_exist_name("系统消息"):
            mp.choose_chat_by_name("系统消息")
            mp.click_back()
            mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_message_list_total_quantity_0073(self):
        """在消息列表页面，未接收到新的系统消息"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 消息列表如果已经存在消息红点,清空聊天记录
        if mp.is_exist_news_red_dot():
            mp.clear_message_record()
            time.sleep(2)
        # 1.验证是否存在红点提醒
        self.assertEquals(mp.is_exist_news_red_dot(), False)

