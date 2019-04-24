import preconditions
from library.core.TestCase import TestCase
from selenium.common.exceptions import TimeoutException
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components.BaseChat import BaseChatPage
import time
import unittest

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
    def make_already_in_call():
        """确保进入通话界面"""
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        cpg = CallPage()
        message_page = MessagePage()
        if message_page.is_on_this_page():
            cpg.click_call()
            return
        if cpg.is_on_the_call_page():
            return
        try:
            current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
        except:
            pass
        current_mobile().launch_app()
        try:
            message_page.wait_until(
                condition=lambda d: message_page.is_on_this_page(),
                timeout=15
            )
            cpg.click_call()
            return
        except TimeoutException:
            pass
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()
        cpg.click_call()

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


class CallAll(TestCase):
    """
    模块：通话
    文件位置：全量/ 7.通话（拨号盘、多方视频-非RCS、视频通话、语音通话）全量测试用例-申丽思.xlsx
    表格：通话（拨号盘、多方视频-非RCS、视频通话、语音通话）
    Author:wangquansheng
    """

    @classmethod
    def setUpClass(cls):
        # 创建联系人
        fail_time = 0
        import dataproviders
        while fail_time < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
                current_mobile().hide_keyboard_if_display()
                for name, number in required_contacts:
                    preconditions.make_already_in_message_page()
                    conts.open_contacts_page()
                    if conts.is_text_present("显示"):
                        conts.click_text("不显示")
                    conts.create_contacts_if_not_exits(name, number)

                # 创建群
                # required_group_chats = dataproviders.get_preset_group_chats()
                #
                # conts.open_group_chat_list()
                # group_list = GroupListPage()
                # for group_name, members in required_group_chats:
                #     group_list.wait_for_page_load()
                #     group_list.create_group_chats_if_not_exits(group_name, members)
                # group_list.click_back()
                # conts.open_message_page()
                return
            except:
                fail_time += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)

    @classmethod
    def tearDownClass(cls):
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()
        cdp = ContactDetailsPage()
        cdp.delete_all_contact()

    def default_setUp(self):
        """进入Call页面,清空通话记录"""
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()

    # def default_tearDown(self):
    #     pass

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0001(self):
        """检查进入到通话界面，“通话”按钮变为“拨号盘”"""
        # Step:1.点击通话tab
        cpg = CallPage()
        cpg.click_call()
        # CheckPoint:1.进入到通话记录列表界面，底部“通话”按钮变成“拨号盘”，拨号盘按钮显示9蓝点
        cpg.page_should_contain_text('拨号盘')
        cpg.click_call()

    @staticmethod
    def setUp_call_shenlisi_0002():
        # 清除应用app缓存，并登陆和飞信
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_call()

    # @tags('ALL', 'CMCC_RESET', 'Call')
    @unittest.skip("pass")
    def test_call_shenlisi_0002(self):
        """检查未开通通讯录权限，进入到通话记录列表界面"""
        # Step:1.点击通话tab
        cpg = CallPage()
        cpg.click_call()
        CalllogBannerPage().skip_multiparty_call()
        time.sleep(1)
        GrantPemissionsPage().deny_contacts_permission()
        cpg.click_call()
        # Step:2.切换为消息，再次进入通话界面
        cpg.click_message()
        cpg.click_call()
        # CheckPoint:1.未开启其他通讯录权限时，每次进入通话，会弹出权限开启提示
        cpg.page_should_contain_text('需要读取通话记录权限')

    @staticmethod
    def tearDown_call_shenlisi_0002():
        """重新清除应用缓存，确保应用权限获取正常"""
        preconditions.reset_and_relaunch_app()

    @staticmethod
    def setUp_call_shenlisi_0003():
        # 清除应用app缓存，并登陆和飞信
        preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

    # @tags('ALL', 'CMCC_RESET', 'Call')
    @unittest.skip("pass")
    def test_call_shenlisi_0003(self):
        """检查用户首次进入到“通话”界面"""
        # Step:1.点击通话tab
        cpg = CallPage()
        cpg.click_call()
        # CheckPoint:1.拨号提示内容：点击底部【拨号】按钮即可弹出/收起拨号盘。可关闭成功
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        cpg.click_call()
        flag = cpg.check_call_phone()
        self.assertFalse(flag)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0004(self):
        """检查拨号盘展开"""
        cpg = CallPage()
        # Step:1.点击“拨号盘"按钮
        cpg.click_call()
        # CheckPoint:1.拨号盘展示，输入框提示“直接拨号或者开始搜索”，菜单栏被隐藏
        cpg.page_should_contain_text('直接拨号或开始搜索')
        cpg.page_should_not_contain_text('多方通话')
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0005(self):
        """检查展开拨号盘，通话记录展示"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘为展开状态
        cpg = CallPage()
        callselect = CallTypeSelectPage()
        cpg.click_call()
        cpg.dial_number("15343030000")
        cpg.click_call_phone()
        callselect.click_call_by_general()
        time.sleep(1)
        cpg.hang_up_the_call()

        time.sleep(30)
        if not cpg.is_on_the_dial_pad():
            cpg.click_call()
        cpg.dial_number("15343038867")
        cpg.click_call_phone()
        callselect.click_call_by_general()
        time.sleep(1)
        cpg.hang_up_the_call()
        time.sleep(1)

        # Step:1.查看通话记录
        # CheckPoint:1.展开后，通话记录按最近通话顺序展示
        if cpg.is_on_the_dial_pad():
            cpg.click_call()
        self.assertTrue(cpg.get_call_history(index=0)[0:11] == "15343038867")
        self.assertTrue(cpg.get_call_history(index=1)[0:11] == "15343030000")

        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0006(self):
        """检查展开拨号盘，通话记录为空"""
        # Step:1.查看通话记录
        cpg = CallPage()
        # CheckPoint:1.页面中间显示图片以及提示语
        cpg.page_should_contain_text("高清通话，高效沟通！")
        flag = cpg.check_call_image()
        self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0007(self):
        """检查拨号盘按键可点击"""
        cpg = CallPage()
        cpg.click_call()
        # Step:1.点击按键“1”
        cpg.click_one()
        # Step:2.点击按键“2”
        cpg.click_two()
        # Step:3.点击按键“3”
        cpg.click_three()
        # Step:4.点击按键“4”
        cpg.click_four()
        # Step:5.点击按键“5”
        cpg.click_five()
        # Step:6.点击按键“6”
        cpg.click_six()
        # Step:7.点击按键“7”
        cpg.click_seven()
        # Step:8.点击按键“8”
        cpg.click_eight()
        # Step:9.点击按键“9”
        cpg.click_nine()
        # Step:10.点击按键“0”
        cpg.click_zero()
        # Step:11.点击按键“*”
        cpg.click_star()
        # Step:12.点击按键“#”
        cpg.click_sharp()
        # CheckPoint:1.步骤1-12：拨号盘各键输入正常
        cpg.page_should_contain_text("1234567890*#")
        # 清除拨号盘，返回通话界面
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0008(self):
        """检查在拨号盘输入“+”"""
        # Step:1.检查在拨号盘输入“+”
        cpg = CallPage()
        cpg.click_call()
        time.sleep(1)
        cpg.press_zero()
        # CheckPoint:1.展开后，通话记录按最近通话顺序展示
        cpg.page_should_contain_text("+")
        # 清除拨号盘，返回通话界面
        cpg.click_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0009(self):
        """检查输入框有内容时拨号盘可切换到其它模块"""
        # Step:1.切换至其它模块后又返回到拨号盘
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("15343030000")
        time.sleep(1)
        # CheckPoint:1.收起时切换到其他的模块，内容不清除，正常显示
        cpg.page_should_contain_text("15343030000")
        # Step:2. 切换为消息
        cpg.click_message()
        time.sleep(2)
        # CheckPoint:2.收起时切换到其他的模块，内容不清除，正常显示
        cpg.page_should_not_contain_text("15343030000")
        # Step:3. 切换为拨号盘
        cpg.click_call()
        # CheckPoint:3.收起时切换到其他的模块，内容不清除，正常显示
        cpg.page_should_contain_text("15343030000")
        # 清除拨号盘，返回通话界面
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0010(self):
        """检查拨号盘删除按键可点击"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘输入框存在手机号
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("15343038860")
        # Step:1.点击按键“X”
        cpg.click_delete()
        # CheckPoit:1.可删除输入框的数据
        cpg.page_should_contain_text("1534303886")
        # Step:2.长按“X”
        cpg.press_delete()
        # CheckPoit:2.连续删除输入框的数据
        cpg.page_should_contain_text("直接拨号或开始搜索")
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0011(self):
        """检查拨号盘“多方电话”按键可点击"""
        # Step:1.点击按键“多方电话”
        cpg = CallPage()
        cpg.click_free_call()
        time.sleep(2)
        # CheckPoint:1.调起联系人多方电话联系人选择器
        self.assertTrue(CalllogBannerPage().is_exist_contact_search_bar())
        cpg.click_back()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0012(self):
        """检查拨号盘输入框为空点击“拨打”按钮"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘为展开状态
        # 3.拨号盘输入框为空
        cpg = CallPage()
        cpg.click_call()
        # Step:1.点击“拨号”按钮
        cpg.click_call_phone()
        # CheckPoint:1.提示“拨打号码不能为空”
        flag = cpg.is_toast_exist("拨打号码不能为空")
        self.assertTrue(flag)
        cpg.click_call()

    # @tags('ALL', 'CMCC', 'Call')
    @unittest.skip("pass")
    def test_call_shenlisi_0013(self):
        """检查拨号盘展开状态可收起"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘为展开状态
        cpg = CallPage()
        # Step:1.点击拨号盘按钮
        # CheckPoint:1.拨号盘可收起展开，拨号盘图标变为7个蓝点
        callcolor = cpg.get_call_color_of_element()
        # TODOs

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0014(self):
        """检查输入框有内容可收起拨号盘"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘为展开状态
        # 3.拨号盘存在数值
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("153")
        # Step:1点击拨号盘按钮
        cpg.click_call()
        # CheckPoint:1.拨号盘可收起展开，收起展开内容保留不清除，正常显示
        flag = cpg.check_delete_hide()
        self.assertTrue(flag)
        cpg.page_should_contain_text("153")
        # 删除拨号盘输入内容
        cpg.click_call()
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0015(self):
        """检查输入框有内容收起拨号盘可切换到其它模块"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘为收起展开状态
        # 3.拨号盘存在数值
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("153")
        # Step:1.切换至其它模块后又返回到拨号盘
        cpg.click_message()
        flag = cpg.check_call_phone()
        self.assertFalse(flag)
        cpg.click_call()
        # CheckPoint:1.拨号盘可收起展开，收起展开内容保留不清除，正常显示
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        cpg.page_should_contain_text("153")
        time.sleep(1)
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0016(self):
        """检查输入框有内容收起展开可退到后台"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘为收起展开状态
        # 3.拨号盘存在数值
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("153")
        time.sleep(2)
        # Step:1.点击手机主键
        cpg.click_call()
        # Step:2.再次进入到和飞信-拨号盘
        cpg.background_app(2)
        time.sleep(2)
        # CheckPoint:1.拨号盘可收起展开，收起展开内容保留不清除，正常显示
        flag = cpg.check_delete_hide()
        self.assertTrue(flag)
        cpg.page_should_contain_text("153")
        cpg.click_call()
        cpg.page_should_contain_text("153")
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        time.sleep(1)
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0017(self):
        """检查输入框有内容展开状态可退到后台"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘为展开状态
        # 3.拨号盘存在数值
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("153")
        # Step:1.点击手机主键
        # Step:2.再次进入到和飞信-拨号盘
        cpg.background_app(2)
        time.sleep(2)
        # CheckPoint:1.拨号盘可收起展开，收起展开内容保留不清除，正常显示
        cpg.page_should_contain_text("153")
        flag = cpg.check_call_phone()
        self.assertTrue(flag)

        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0018(self):
        """检查杀掉进程会清除拨号盘的数值"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘存在数值
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("*53")

        # Step:1.杀掉进程，再次进入到和飞信-拨号盘
        current_mobile().terminate_app('com.chinasofti.rcs')
        current_mobile().launch_app()
        time.sleep(2)
        # CheckPoint:1.杀死进程在进入，输入内容被清除，拨号盘默认收起
        cpg.click_call()
        cpg.page_should_not_contain_text("*53")
        flag = cpg.check_call_phone()
        self.assertFalse(flag)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0020(self):
        """检查输入框输入超长数字"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘展开状态
        # 3.拨号盘存在超长数值（数值超一行）
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("153153153153153")
        # Step:1.查看输入框样式
        # CheckPoint:1.显示正常
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        flag = cpg.check_call_text(val="153153153153153")
        self.assertTrue(flag)
        # Step:2.点击拨号盘，查看输入框样式
        cpg.click_call()
        # 2.输入超长数字，收起显示正常
        flag = cpg.check_call_phone()
        self.assertFalse(flag)
        flag = cpg.check_call_text(val="153153153153153")
        self.assertTrue(flag)

        cpg.click_call()
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0022(self):
        """检查拨号盘精确搜索功能---内陆本地联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的内陆号本地已保存
        cpg = CallPage()
        cpg.setting_dial_mode_and_go_back_call()
        # Step:1.点击“拨号盘”
        cpg.click_call()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入11位数内陆号
        cpg.dial_number("13800138001")
        # CheckPoint:2.可匹配出符合条件的联系人，匹配的结果高亮
        cpg.page_should_contain_text("给个红包2")
        # ret = cpg.get_call_entry_color_of_element()
        # self.assertEqual(ret, (133, 128, 95, 255))
        # Step:3.点击匹配出的联系人右侧的时间节点
        cpg.click_call_profile()
        time.sleep(1)
        # CheckPoint:3.可进入到该联系人的通话profile
        cpg.page_should_contain_text("分享名片")
        # Step:4.点击拨号按钮
        cpg.click_back_by_android()
        time.sleep(1)
        cpg.click_call_phone()
        # CheckPoint:4.可弹出拨号方式
        time.sleep(1)
        cpg.page_should_contain_text("和飞信电话（免费）")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("普通电话")

        cpg.click_back_by_android(2)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0023(self):
        """检查拨号盘精确搜索功能---内陆陌生联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的内陆号本地未保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.setting_dial_mode_and_go_back_call()
        cpg.click_call()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入11位数内陆号
        cpg.dial_number("15343039999")
        time.sleep(2)
        # CheckPoint:2.通话记录列表弹出“新建联系人”“发送消息”按钮
        cpg.page_should_contain_text("新建联系人")
        cpg.page_should_contain_text("发送消息")
        # Step:3.点击拨号按钮
        cpg.click_call_phone()
        # CheckPoint:3.可弹出拨号方式
        time.sleep(2)
        cpg.page_should_contain_text("和飞信电话（免费）")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("普通电话")

        cpg.click_back_by_android()
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0024(self):
        """检查拨号盘精确搜索功能---香港本地联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的香港号本地已保存
        cpg = CallPage()
        # Step:1.点击“拨号盘”
        cpg.click_call()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入8位数香港号
        cpg.dial_number("67656003")
        # CheckPoint:2.可匹配出符合条件的联系人，匹配的结果高亮
        cpg.page_should_contain_text("香港大佬")
        # Step:3.点击匹配出的联系人右侧的时间节点
        cpg.click_call_profile()
        time.sleep(1)
        # CheckPoint:3.可进入到该联系人的通话profile
        cpg.page_should_contain_text("分享名片")
        cpg.click_back_by_android(2)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0025(self):
        """检查拨号盘精确搜索功能---香港陌生联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的香港号本地未保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.click_call()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入8位数香港号
        cpg.dial_number("23454097")
        time.sleep(2)
        # CheckPoint:2.通话记录列表弹出“新建联系人”“发送消息”按钮
        cpg.page_should_contain_text("新建联系人")
        cpg.page_should_contain_text("发送消息")

        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0026(self):
        """检查从拨号盘进入到陌生人消息会话窗口"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘已输入陌生联系人A的手机号
        # 3.通话记录列表已弹出“新建联系人”“发送消息”按钮
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("15343038860")
        # Step:1.点击“发送消息”按钮
        cpg.click_send_message()
        chatpage = BaseChatPage()
        flag = chatpage.is_exist_dialog()
        if flag:
            chatpage.click_i_have_read()
        # CheckPoint:1.进入与陌生联系人A的消息回话窗口
        cpg.page_should_contain_text("说点什么...")

        cpg.click_back_by_android()
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0027(self):
        """检查从拨号盘新建联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘已输入陌生联系人A的手机号
        # 3.通话记录列表已弹出“新建联系人”“发送消息”按钮
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("15343038860")
        # Step:1.点击“新建联系人”按钮
        cpg.click_new_contact()
        time.sleep(2)
        cpg.hide_keyboard()
        # CheckPoint:1.跳转到新建联系人界面，电话栏自动填充联系人A的手机号，其它输入框为空
        cpg.page_should_contain_text("输入姓名")
        cpg.page_should_contain_text("15343038860")
        cpg.page_should_contain_text("输入公司")
        cpg.page_should_contain_text("输入职位")
        cpg.page_should_contain_text("输入邮箱")

        cpg.click_back_by_android()
        cpg.press_delete()
        cpg.click_call()

    # @tags('ALL', 'CMCC', 'Call')
    @unittest.skip("跳过")
    def test_call_shenlisi_0030(self):
        """检查搜索结果超一屏"""
        # 1.用户已登录和飞信：通话记录列表-拨号盘
        # 2.匹配结果超过一屏
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("1380013800")
        if cpg.is_on_the_dial_pad():
            cpg.click_call()
        # Step:1.上下滑动屏幕
        # CheckPoint:1.匹配结果超过一屏时，可滑动
        #  向下滑动
        for i in range(2):
            cpg.swipe_by_percent_on_screen(50, 50, 50, 80, 800)
        cpg.page_should_contain_text("给个红包3")

        #  向上滑动
        for i in range(2):
            cpg.swipe_by_percent_on_screen(50, 80, 50, 30, 800)
        cpg.page_should_contain_text("大佬1")

        # Step:2.查看排序
        time.sleep(1)
        # CheckPoint:2.排序正常
        # TODO

    @staticmethod
    def tearDown_test_call_shenlisi_0030():
        CallPage().delete_all_call_entry()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0031(self):
        """检查本网用户登录，在拨号盘拨打手机号拨号方式推荐---多方时长>0"""
        # 1.异网用户已登录在通话--拨号盘
        # 2.拨号方式设置“总是询问”
        # 3.多方时长>0
        # 4.在拨号盘输入手机号
        # Step:1.点击【拨号】按钮
        # CheckPoint:1弹出拨号方式依次显示“和飞信电话（免费）、语音通话（免流量）、普通电话”
        cpg = CallPage()
        callselect = CallTypeSelectPage()
        cpg.setting_dial_mode_and_go_back_call()
        cpg.click_call()
        # （本网号：13662498503
        cpg.dial_number(text="13662498503")
        cpg.click_call_phone()
        time.sleep(1)
        cpg.page_should_contain_text("和飞信电话（免费）")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("普通电话")
        self.assertTrue(
            callselect.get_call_by_hefeixin_y() < callselect.get_call_by_voice_y() < callselect.get_call_by_general_y())
        cpg.click_back_by_android(2)

        # 本网加区+8613662498503/008613662498503
        cpg.click_call()
        cpg.dial_number(text="008613662498503")
        cpg.click_call_phone()
        time.sleep(1)
        cpg.page_should_contain_text("和飞信电话（免费）")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("普通电话")
        self.assertTrue(
            callselect.get_call_by_hefeixin_y() < callselect.get_call_by_voice_y() < callselect.get_call_by_general_y())
        cpg.click_back_by_android(2)

        # 异网号：13260892669
        cpg.click_call()
        cpg.dial_number(text="13260892669")
        cpg.click_call_phone()
        time.sleep(1)
        cpg.page_should_contain_text("和飞信电话（免费）")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("普通电话")
        self.assertTrue(
            callselect.get_call_by_hefeixin_y() < callselect.get_call_by_voice_y() < callselect.get_call_by_general_y())
        cpg.click_back_by_android(2)

        # 异网加区号：+8613260892669
        cpg.click_call()
        cpg.dial_number(text="+8613260892669")
        cpg.click_call_phone()
        time.sleep(1)
        cpg.page_should_contain_text("和飞信电话（免费）")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("普通电话")
        self.assertTrue(
            callselect.get_call_by_hefeixin_y() < callselect.get_call_by_voice_y() < callselect.get_call_by_general_y())
        cpg.click_back_by_android(2)

        # 香港号：67656003
        cpg.click_call()
        cpg.dial_number(text="67656003")
        cpg.click_call_phone()
        time.sleep(1)
        cpg.page_should_contain_text("和飞信电话（免费）")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("普通电话")
        self.assertTrue(
            callselect.get_call_by_hefeixin_y() < callselect.get_call_by_voice_y() < callselect.get_call_by_general_y())
        cpg.click_back_by_android(2)
        # 香港号加区号：+85267656003/0085267656003
        # ）
        cpg.click_call()
        cpg.dial_number(text="0085267656003")
        cpg.click_call_phone()
        time.sleep(1)
        cpg.page_should_contain_text("和飞信电话（免费）")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("普通电话")
        self.assertTrue(
            callselect.get_call_by_hefeixin_y() < callselect.get_call_by_voice_y() < callselect.get_call_by_general_y())
        cpg.click_back_by_android(2)

    # @tags('ALL', 'CMCC', 'Call')
    @unittest.skip("用例修改，先跳过")
    def test_call_shenlisi_0035(self):
        """检查本网用户登录，在拨号盘拨打固号拨号方式推荐---多方时长>0"""
        # 1.本网用户已登录在通话--拨号盘
        # 2.拨号方式设置“总是询问”
        # 3.多方时长>0
        # 4.在拨号盘输入固号
        # （无区号内陆固号：
        # （10位数）0223786543
        # （11位数）02023769875
        # （12位数）0987345690209
        # 无区号香港固号：
        # 以“2”开头固号：2345876
        # 以“3”开头固号：30980987
        # 有区号香港固号（+852/00852）:
        # 以“2”开头固号：23458765
        # 以“3”开头固号：30980987
        #
        # 1.点击【拨号】按钮
        lst = ["0223786543", "02023769875", "0987345690209", "2345876", "30980987", "+85223458765", "+85230980987", ]
        cpg = CallPage()
        callselect = CallTypeSelectPage()
        cpg.setting_dial_mode_and_go_back_call()
        for i in range(7):
            cpg.click_call()
            cpg.dial_number(str(lst[i]))
            cpg.click_call_phone()
            time.sleep(1)
            cpg.page_should_contain_text("和飞信电话（免费）")
            cpg.page_should_contain_text("普通电话")
            # 弹出拨号方式依次显示“和飞信电话（免费”、“普通电话”
            self.assertTrue(
                callselect.get_call_by_hefeixin_y() < callselect.get_call_by_general_y())
            cpg.click_back_by_android(2)

    # @tags('ALL', 'CMCC', 'Call')
    @unittest.skip("用例修改，先跳过")
    def test_call_shenlisi_0036(self):
        """检查固号加区号无法拨打成功"""
        # 1.本网用户已登录在通话--拨号盘
        # 2.拨号方式设置“总是询问”
        # 3.在拨号盘输入有区号内陆固号（+86/0086）：
        # （10位数）0223786543
        # （11位数）0202376987
        # （12位数）0987345690209
        # 1.点击拨号按钮
        lst = ["+860223786543","+860202376987","+860987345690209"]
        cpg = CallPage()
        cpg.setting_dial_mode_and_go_back_call()
        for i in range(3):
            cpg.click_call()
            cpg.dial_number(str(lst[i]))
            cpg.click_call_phone()
            time.sleep(1)
            # 1.调起系统电话后，系统电话拨打失败
            self.assertTrue(cpg.is_phone_in_calling_state())
            cpg.hang_up_the_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0050(self):
        """检查拨号盘取消拨号方式"""
        # 1.用户已登录和飞信：通话-拨号盘
        # 2.已弹出拨号方式
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("15340038800")
        cpg.click_call_phone()
        # Step:1.点击“取消”按钮
        cpg.click_back_by_android()
        # CheckPoint:1.拨号方式收起，停留在输入号码的拨号盘页
        self.assertTrue(cpg.check_call_phone())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0051(self):
        """检查在拨号盘输入异常字符拨号"""
        # 1.用户已登录和飞信：通话-拨号盘
        # 2.在拨号盘已输入*，#、空格等字符
        # 3.无副号
        # Step:1.点击拨号按钮
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("*# ")
        cpg.click_call_phone()
        # CheckPoint:1.提示“输入号码无效，请重新输入”
        flag = cpg.is_toast_exist("输入的号码无效，请重新输入")
        self.assertTrue(flag)

        cpg.click_call()

    # @tags('ALL', 'CMCC', 'Call')
    @unittest.skip("用例删除")
    def test_call_shenlisi_0052(self):
        """检查拨号盘拨号方式“设置”按钮跳转"""
        # 1.用户已登录和飞信：通话-拨号盘
        # 2.在输入框输入合法手机号
        # a.11位数内陆手机号
        # b.8位数香港手机号
        # Step:1.点击拨号按钮
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("15343039999")
        cpg.click_call_phone()
        time.sleep(2)
        # CheckPoint:1.顶部置灰文案为：呼叫（号码)，靠右显示“设置”按钮
        cpg.page_should_contain_text("呼叫 15343039999")
        cpg.page_should_contain_text("设置")
        # Step:2.点击设置按钮
        CallTypeSelectPage().click_setting()
        time.sleep(1)
        # CheckPoint:2.跳转到拨号方式选择：总是询问（默认）、优先使用和飞信电话、只用语音通话、只用普通电话、自动推荐
        cpg.page_should_contain_text("总是询问")
        cpg.page_should_contain_text("优先使用和飞信电话")
        cpg.page_should_contain_text("只用语音通话")
        cpg.page_should_contain_text("只用普通电话")
        cpg.page_should_contain_text("自动推荐")
        cpg.click_back_by_android(2)

        # 香港号码
        cpg.click_call()
        cpg.dial_number("92662789")
        cpg.click_call_phone()
        time.sleep(2)
        cpg.page_should_contain_text("呼叫 92662789")
        cpg.page_should_contain_text("设置")
        CallTypeSelectPage().click_setting()
        time.sleep(1)
        cpg.page_should_contain_text("总是询问")
        cpg.page_should_contain_text("优先使用和飞信电话")
        cpg.page_should_contain_text("只用语音通话")
        cpg.page_should_contain_text("只用普通电话")
        cpg.page_should_contain_text("自动推荐")
        cpg.click_back_by_android(2)

    def test_call_shenlisi_0053(self):
        """多方电话时长大于0时调起的通话方式选择【和飞信电话】右侧新增【设置为默认】按钮"""
        # 多方电话时长大于0且拨号方式设置为总是询问
        # Step:1、在拨号盘输入号码，点击通话按钮
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("15343039999")
        cpg.click_call_phone()
        time.sleep(2)
        # CheckPoint:1.调起的通话方式选择【和飞信电话】右侧新增【设置为默认】按钮
        cpg.page_should_contain_text("和飞信电话")
        cpg.page_should_contain_text("设置为默认")

        # Step:2.点击“设置为默认”
        CallTypeSelectPage().click_setting()

        # CheckPoint:2.可设置默认拨号方式为“和飞信电话”拨号设置并默认同步“优先使用和飞信”按钮，并弹出提示：可前往“我-设置-拨号设置”中进行设置
        cpg.select_dial_mode()
        cpg.is_toast_exist("可前往“我-设置-拨号设置”修改")
        self.assertTrue(MeSetDialWayPage().check_call_type(1))
        cpg.click_back_by_android(3)
        cpg.click_call()
        cpg.click_back_by_android()

    @staticmethod
    def tearDown_test_call_shenlisi_0053():
        Preconditions.make_already_in_call()
        CallPage().setting_dial_mode_and_go_back_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0064(self):
        """检查拨号盘搜索功能---内陆本地联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的内陆号本地已保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.click_call()
        time.sleep(2)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入11位数内陆号
        cpg.dial_number("13800138001")
        # CheckPoint:2.精确匹配出与拨号盘号码一致的手机号联系人
        cpg.page_should_contain_text("给个红包2")
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0065(self):
        """检查拨号盘搜索功能---内陆陌生联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的内陆号本地未保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.click_call()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入11位数内陆号
        cpg.dial_number("15343038867")
        # CheckPoint:2.通话记录列表弹出“新建联系人”“发送消息”按钮
        cpg.page_should_contain_text("新建联系人")
        cpg.page_should_contain_text("发送消息")
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0066 (self):
        """检查拨号盘搜索功能---香港本地联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的香港号本地已保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.click_call()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入8位数香港号
        cpg.dial_number("67656003")
        # CheckPoint:2.精确匹配出与拨号盘号码一致的手机号联系人
        cpg.page_should_contain_text("香港大佬")
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0067(self):
        """检查拨号盘搜索功能---香港陌生联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的香港号本地未保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.click_call()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入8位数香港号
        cpg.dial_number("67656000")
        # CheckPoint:2.通话记录列表弹出“新建联系人”“发送消息”按钮
        cpg.page_should_contain_text("新建联系人")
        cpg.page_should_contain_text("发送消息")
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0068(self):
        """检查从拨号盘进入到陌生人消息会话窗口"""
        # 1.1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘已输入陌生联系人A的手机号
        # 3.通话记录列表已弹出“新建联系人”“发送消息”按钮
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("15343038867")
        # Step:1.点击“发送消息”按钮
        cpg.click_send_message()
        chatpage = BaseChatPage()
        if chatpage.is_exist_dialog():
            chatpage.click_i_have_read()
        # CheckPoint:1.进入与陌生联系人A的消息回话窗口
        cpg.page_should_contain_text("说点什么...")

        cpg.click_back_by_android()
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0069(self):
        """检查从拨号盘新建联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘已输入陌生联系人A的手机号
        # 3.通话记录列表已弹出“新建联系人”“发送消息”按钮
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("15343038867")
        # Step:1.点击“新建联系人”按钮
        cpg.click_new_contact()
        time.sleep(2)
        cpg.hide_keyboard()
        # CheckPoint:1.跳转到新建联系人界面，电话栏自动填充联系人A的手机号，其它输入框为空
        cpg.page_should_contain_text("输入姓名")
        cpg.page_should_contain_text("15343038867")
        cpg.page_should_contain_text("输入公司")
        cpg.page_should_contain_text("输入职位")
        cpg.page_should_contain_text("输入邮箱")

        cpg.click_back_by_android()
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0070(self):
        """检查单聊富媒体面板-音频通话拨打"""
        # 1.登录和飞信：消息tab-单聊会话窗口-富媒体面板
        # 2.已弹出语音通话与视频通话按钮
        cpg = CallPage()
        ContactsPage().click_message_icon()
        Preconditions.enter_single_chat_page("给个红包2")
        BaseChatPage().click_more()
        ChatMorePage().click_voice_and_video_call()
        # Step:1.点击语音通话
        cpg.click_voice_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(1)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        time.sleep(1)
        # CheckPoint:1.直接呼出一对一语音通话
        cpg.page_should_contain_text("正在呼叫")
        cpg.wait_until(
            timeout=30,
            auto_accept_permission_alert=True,
            condition=lambda d: cpg.is_text_present("说点什么..."))
        # Step:2.点击视频电话
        BaseChatPage().click_more()
        ChatMorePage().click_voice_and_video_call()
        cpg.click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(1)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # Step:2.直接呼出一对一视频通话
        time.sleep(2)
        cpg.page_should_contain_text("视频通话呼叫中")

    # @tags('ALL', 'CMCC', 'Call')
    @unittest.skip("跳过")
    def test_call_shenlisi_0078(self):
        """检查呼叫界面手机号展示"""
        # 1.用户M为本地联系人
        # 2.用户N未为陌生联系人
        # Step:1..检查语音拨打用户M的呼叫界面名称展示
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("13800138001")
        cpg.click_call_phone()
        time.sleep(1)
        CallTypeSelectPage().click_call_by_voice()
        CallTypeSelectPage().click_sure()
        CallTypeSelectPage().click_sure()
        try:
            if cpg.is_text_present("现在去开启"):
                cpg.click_text("暂不开启")
        except:
            print("不存在开启悬浮框权限")
            pass
        time.sleep(1)
        # CheckPoint:1.展示把M保存在本地的名称
        cpg.page_should_contain_text("给个红包2")

        # Step:2.检查语音拨打用户N的呼叫界面名称展示
        cpg.wait_for_dial_pad()
        cpg.dial_number("15343038860")
        cpg.click_call_phone()
        time.sleep(1)
        CallTypeSelectPage().click_call_by_voice()
        time.sleep(1)
        try:
            if cpg.is_text_present("现在去开启"):
                cpg.click_text("暂不开启")
        except:
            print("不存在开启悬浮框权限")
            pass
        time.sleep(1)
        # CheckPoint:2.展示用户N的手机号
        cpg.page_should_contain_text("15343038860")
        cpg.wait_for_dial_pad()

        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0086(self):
        """检查语音通话记录-陌生联系人"""
        # 1.A已登录和飞信
        # 2.用户A已成功发起与用户B的语音通话
        # Step:1.用户A查看通话记录
        cpg = CallPage()
        cpg.click_call()
        time.sleep(1)
        cpg.select_type_start_call(calltype=1, text="13800138001")
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        cpg.wait_for_dial_pad()
        if not cpg.is_on_the_call_page():
            cpg.click_call()
        time.sleep(1)
        # CheckPoint:1.通话记录展示与用户B的语音通话记录，显示用户B的名称、通话类型【语音通话】、归属地。右侧显示通话时间以及时间节点图标
        cpg.page_should_contain_text("给个红包2")
        cpg.page_should_contain_text("语音通话")
        # cpg.page_should_contain_text("广东深圳")
        # cpg.page_should_contain_text("移动")
        self.assertTrue(cpg.is_exist_call_time())
        # Step:2.点击时间节点
        cpg.click_call_time()
        time.sleep(1)
        # CheckPoint:2.进入到用户B的通话profile
        self.assertTrue(cpg.is_exist_profile_name())
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0088(self):
        """检查语音通话记录-陌生联系人"""
        # 1.A已登录和飞信
        # 2.用户A已成功发起与用户B的语音通话
        # Step:1.用户A查看通话记录
        cpg = CallPage()
        cpg.click_call()
        time.sleep(1)
        cpg.select_type_start_call(calltype=1, text="13537795364")
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        cpg.wait_for_dial_pad()
        if not cpg.is_on_the_call_page():
            cpg.click_call()
        time.sleep(1)
        # CheckPoint:1.通话记录展示与用户B的语音通话记录，显示用户B的名称、通话类型【语音通话】、归属地。右侧显示通话时间以及时间节点图标
        cpg.page_should_contain_text("13537795364")
        cpg.page_should_contain_text("语音通话")
        # cpg.page_should_contain_text("广东深圳")
        # cpg.page_should_contain_text("移动")
        self.assertTrue(cpg.is_exist_call_time())
        # Step:2.点击时间节点
        cpg.click_call_time()
        time.sleep(1)
        # CheckPoint:2.进入到用户B的通话profile
        self.assertTrue(cpg.is_exist_profile_name())
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0145(self):
        """检查呼叫界面缩放按钮--未获取悬浮窗权限（仅安卓）"""
        # 1.已进入到语音呼叫界面
        # 2.系统未开启悬浮窗权限
        # 3.被叫还是被继续邀请中
        cpg = CallPage()
        cpg.create_call_entry("15343038867")
        cpg.click_call_time()
        ccdp = CallContactDetailPage()
        ccdp.click_voice_call()
        time.sleep(2)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # Step:1.点击缩放按钮
        ccdp.click_smart_voice_hide()
        time.sleep(2)

        # CheckPoint:1.通话控制管理页面消失，返回到发起呼叫的入口页，通话并未挂断
        self.assertTrue(cpg.is_on_this_messagepage())

        # CheckPoint：2.消息列表页有正在通话入口，显示为：你正在语音通话   未接通不显示时长
        cpg.page_should_contain_text("你正在语音通话")
        # Step:2.点击返回
        # Step：3.点击通话入口
        ccdp.click_voice_call_status()

        # CheckPoint：3.返回到呼叫界面
        cpg.page_should_contain_text("15343038867")
        cpg.is_on_this_messagepage()

        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0146(self):
        """检查呼叫中缩小悬窗呼叫结束，通话入口消息（仅安卓）"""
        # 1.已进入到语音呼叫界面
        # 2.系统未开启悬浮窗权限
        cpg = CallPage()
        cpg.create_call_entry("15343038867")
        cpg.click_call_time()
        ccdp = CallContactDetailPage()
        ccdp.click_voice_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # Step:1.点击缩放按钮
        ccdp.click_smart_voice_hide()
        time.sleep(2)

        # CheckPoint:1.通话控制管理页面消失，返回到发起呼叫的入口页，通话并未挂断
        self.assertTrue(cpg.is_on_this_messagepage())

        # CheckPoint：2.消息列表页有正在通话入口，显示为：你正在语音通话   未接通不显示时长
        cpg.page_should_contain_text("你正在语音通话")
        # Step:2.点击返回
        # Step:3.呼叫结束
        ccdp.is_exist_voice_call()

        # CheckPoint：3.通话入口消失
        cpg.page_should_not_contain_text("你正在语音通话")

        cpg.click_call()

    @staticmethod
    def setUp_test_call_shenlisi_0155():
        # 关闭WiFi，打开4G网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(4)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0155(self):
        """检查语音通话-未订购每月10G用户--4g弹出每月10G免流特权提示窗口"""
        # 1.客户端已登录
        # 2.未订购每月10G用户
        # 3.网络使用4G
        cpg = CallPage()
        # Step:1.发起语音通话
        cpg.select_type_start_call(calltype=1, text="13800138001")
        time.sleep(1)
        # CheckPoint:1.弹出每月10G免流特权提示窗口。
        cpg.page_should_contain_text("每月10G免流特权")
        # Step:2.查看界面
        # CheckPoint:2.加粗文案为：语音通话每分钟消耗约0.3MB流量，订购[每月10G]畅聊语音/视频通话。弹窗底部显示“继续拨打”、“订购免流特权”、“以后不再提示”
        cpg.page_should_contain_text("语音通话每分钟消耗约0.3MB流量，订购[每月10G]畅聊语音/视频通话")
        cpg.page_should_contain_text("继续拨打")
        cpg.page_should_contain_text("订购免流特权")
        cpg.page_should_contain_text("以后不再提示")
        # Step:3.点击“继续拨打”
        cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        time.sleep(1)
        # CheckPoint:3.点击后，直接呼叫
        cpg.page_should_contain_text("正在呼叫")
        # Step:4.再次点击语音通话
        cpg.wait_for_dial_pad()
        cpg.select_type_start_call(calltype=1, text="13800138001")
        # CheckPoint:4.继续弹出提示窗口
        cpg.page_should_contain_text("每月10G免流特权")
        cpg.click_back_by_android(2)

    @staticmethod
    def tearDown_test_call_shenlisi_0155():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)

    @staticmethod
    def setUp_test_call_shenlisi_0156():
        # 关闭WiFi，打开4G网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(4)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0156(self):
        """检查4g免流特权提示权订购免流特权提示窗口订购免流界面跳转---语音通话"""
        # 1.客户端已登录
        # 2.已弹出4g弹出每月10G免流特权提示窗口
        cpg = CallPage()
        cpg.select_type_start_call(calltype=1, text="13800138001")
        # 1.点击订购免流特权
        cpg.click_text("订购免流特权")
        # 1.跳转到【和飞信送你每月10G流量】H5页面
        cpg.wait_until(timeout=30, auto_accept_permission_alert=True,
                       condition=lambda d: cpg.is_text_present("和飞信送你每月10G流量"))
        cpg.page_should_contain_text("和飞信送你每月10G流量")
        # 2.点击返回按钮
        cpg.click_back_by_android()
        # 2.点击返回按钮，返回上一级
        cpg.page_should_contain_text("每月10G免流特权")
        cpg.click_back_by_android(2)

    @staticmethod
    def tearDown_test_call_shenlisi_0156():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)

    @staticmethod
    def setUp_test_call_shenlisi_0158():
        # 确保打开WiFi网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(6)

    # @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0158(self):
        """检查语音呼叫-未订购每月10G用户--用户在WiFi环境下不提示此类弹窗"""
        # 1.客户端已登录
        # 2.未订购每月10G用户
        # 3.网络使用WIFI
        # 1.发起语音通话
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("13800138001")
        cpg.click_call_phone()
        time.sleep(2)
        CallTypeSelectPage().click_call_by_voice()
        time.sleep(2)
        # 1.直接发起语音通话，没有弹窗
        cpg.page_should_not_contain_text("每月10G免流特权")
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        time.sleep(1)
        cpg.wait_for_dial_pad()
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0213(self):
        """检查视频通话记录——本地联系人"""
        # 1.A已登录和飞信
        # 2.用户A已成功发起与用户B的视频通话
        cpg = CallPage()
        cpg.click_multi_party_video()
        time.sleep(1)
        CalllogBannerPage().input_telephone("13800138001")
        cpg.hide_keyboard()
        time.sleep(1)
        cpg.click_text("给个红包2")
        time.sleep(1)
        cpg.click_text("呼叫")
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(1)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # Step:1.用户A查看通话记录
        cpg.wait_for_page_load()

        # CheckPoint:1.通话记录展示与用户B的视频通话记录，显示用户B的名称、通话类型【视频通话】、手机号/归属地
        cpg.page_should_contain_text("给个红包2")
        cpg.page_should_contain_text("视频通话")
        self.assertTrue(cpg.is_exist_call_time())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0215(self):
        """检查视频通话记录-陌生联系人"""
        # 1.A已登录和飞信
        # 2.用户A已成功发起与用户B的视频通话
        cpg = CallPage()
        cpg.click_multi_party_video()
        time.sleep(1)
        CalllogBannerPage().input_telephone("13537795364")
        cpg.hide_keyboard()
        time.sleep(1)
        cpg.click_text("未知号码")
        time.sleep(1)
        cpg.click_text("呼叫")
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(1)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # Step:1.用户A查看通话记录
        cpg.wait_for_page_load()

        # CheckPoint:1.通话记录展示与用户B的视频通话记录，显示用户B的名称、通话类型【视频通话】、手机号/归属地
        cpg.page_should_contain_text("13537795364")
        cpg.page_should_contain_text("视频通话")
        # cpg.page_should_contain_text("广东深圳")
        # cpg.page_should_contain_text("移动")
        self.assertTrue(cpg.is_exist_call_time())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0218(self):
        """检查呼叫本地联系人，呼叫界面展示名称+手机号"""
        # 1.已登录和飞信
        # 2.用户M为本地联系人
        # 3.已开启麦克风，相机权限
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_call_time()
        time.sleep(1)
        # Step:1.视频呼叫M，进入到呼叫界面
        CallContactDetailPage().click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # CheckPoint:1.头像下展示用户M的名称+手机号
        cpg.page_should_contain_text("13800138001")
        cpg.page_should_contain_text("给个红包2")
        CallContactDetailPage().wait_for_profile_name()
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0219(self):
        """检查呼叫陌生联系人，呼叫界面展示手机号+归属地"""
        # 1.已登录和飞信
        # 2.用户M为陌生联系人可获取到归属地
        # 3.用户N为陌生联系人无法获取归属地（香港号，198开头11位手机号）
        # 3.已开启麦克风，相机权限
        cpg = CallPage()
        cpg.create_call_entry("15343038867")
        cpg.click_call_time()
        time.sleep(1)
        # Step:1.视频呼叫M，进入到呼叫界面
        CallContactDetailPage().click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # CheckPoint:1.头像下展示用户M的手机号+归属地
        cpg.page_should_contain_text("15343038867")
        cpg.page_should_contain_text("湖南-株洲")
        CallContactDetailPage().wait_for_profile_name()
        cpg.click_back_by_android()

        # Step:2.视频呼叫N，进入到呼叫界面
        cpg = CallPage()
        cpg.create_call_entry("19823452586")
        cpg.click_call_time()
        time.sleep(1)
        # Step:2.视频呼叫N，进入到呼叫界面
        CallContactDetailPage().click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # CheckPoint:2.头像下展示用户M的手机号+未知归属地
        cpg.page_should_contain_text("19823452586")
        cpg.page_should_contain_text("未知归属地")
        CallContactDetailPage().wait_for_profile_name()
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0221(self):
        """检查呼叫界面缩放按钮--未获取悬浮窗权限（仅安卓）"""
        # 1.已进入到视频呼叫界面
        # 2.系统未开启悬浮窗权限
        # 3.被叫还是被继续邀请中
        cpg = CallPage()
        cpg.create_call_entry("15343038867")
        cpg.click_call_time()
        ccdp = CallContactDetailPage()
        ccdp.click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # Step:1.点击缩放按钮
        ccdp.click_switch()
        time.sleep(2)

        # CheckPoint:1.通话控制管理页面消失，返回到发起呼叫的入口页，通话并未挂断
        self.assertTrue(cpg.is_on_this_messagepage())

        # CheckPoint：2.消息列表页有正在通话入口，显示为：你正在视频通话   未接通不显示时长
        cpg.page_should_contain_text("你正在视频通话")
        # Step:2.点击返回
        # Step：3.点击通话入口
        ccdp.click_video_call_status()

        # CheckPoint：3.返回到呼叫界面
        cpg.page_should_contain_text("15343038867")
        cpg.is_on_this_messagepage()

        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0222(self):
        """检查呼叫中缩小悬窗呼叫结束，通话入口消息（仅安卓）"""
        # 1.已进入到视频呼叫界面
        # 2.系统未开启悬浮窗权限
        cpg = CallPage()
        cpg.create_call_entry("15343038867")
        cpg.click_call_time()
        ccdp = CallContactDetailPage()
        ccdp.click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # Step:1.点击缩放按钮
        ccdp.click_switch()
        time.sleep(2)

        # CheckPoint:1.通话控制管理页面消失，返回到发起呼叫的入口页，通话并未挂断
        self.assertTrue(cpg.is_on_this_messagepage())

        # CheckPoint：2.消息列表页有正在通话入口，显示为：你正在视频通话   未接通不显示时长
        cpg.page_should_contain_text("你正在视频通话")
        # Step:2.点击返回
        # Step:3.呼叫结束
        ccdp.is_exist_video_call()

        # CheckPoint：3.通话入口消失
        cpg.page_should_not_contain_text("你正在视频通话")

        cpg.click_call()

    @staticmethod
    def setUp_test_call_shenlisi_0231():
        # 关闭WiFi，打开4G网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(4)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0231(self):
        """检查视频呼叫-未订购每月10G用户--4g弹出每月10G免流特权提示窗口"""
        # 1.客户端已登录
        # 2.未订购每月10G用户
        # 3.网络使用4G
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_call_time()
        # Step:1.发起视频通话
        CallContactDetailPage().click_video_call()
        time.sleep(2)
        # CheckPoint:1.弹出每月10G免流特权提示窗口。
        cpg.page_should_contain_text("每月10G免流特权")
        # Step:2.查看界面
        # CheckPoint:2.加粗文案为：视频通话每分钟消耗约8MB流量，订购[每月10G]畅聊视频/视频通话。弹窗底部显示“继续拨打”、“订购免流特权”、“以后不再提示”
        cpg.page_should_contain_text("视频通话每分钟消耗约8MB流量，订购[每月10G]畅聊语音/视频通话")
        cpg.page_should_contain_text("继续拨打")
        cpg.page_should_contain_text("订购免流特权")
        cpg.page_should_contain_text("以后不再提示")
        # Step:3.点击“继续拨打”
        cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        time.sleep(1)
        # CheckPoint:3.点击后，直接呼叫
        cpg.page_should_contain_text("视频通话呼叫中")
        # Step:4.再次点击视频通话
        CallContactDetailPage().wait_for_profile_name()
        CallContactDetailPage().click_video_call()
        # CheckPoint:4.继续弹出提示窗口
        cpg.page_should_contain_text("每月10G免流特权")
        cpg.click_back_by_android(2)

    @staticmethod
    def tearDown_test_call_shenlisi_0231():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)

    @staticmethod
    def setUp_test_call_shenlisi_0232():
        # 关闭WiFi，打开4G网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(4)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0232(self):
        """检查4g免流特权提示权订购免流特权提示窗口订购免流界面跳转--视频通话"""
        # 1.客户端已登录
        # 2.已弹出4g弹出每月10G免流特权提示窗口
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_call_time()
        CallContactDetailPage().click_video_call()
        # 1.点击订购免流特权
        ChatSelectLocalFilePage().click_free_flow_privilege()
        # 1.跳转到【和飞信送你每月10G流量】H5页面
        cpg.wait_until(timeout=30, auto_accept_permission_alert=True,
                       condition=lambda d: cpg.is_text_present("和飞信送你每月10G流量"))
        cpg.page_should_contain_text("和飞信送你每月10G流量")
        # 2.点击返回按钮
        cpg.click_back_by_android()
        # 2.点击返回按钮，返回上一级
        cpg.page_should_contain_text("每月10G免流特权")
        cpg.click_back_by_android(2)

    @staticmethod
    def tearDown_test_call_shenlisi_0232():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)

    @staticmethod
    def setUp_test_call_shenlisi_0234():
        # 确保打开WiFi网络
        Preconditions.make_already_in_call()
        CalllogBannerPage().skip_multiparty_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(6)

    # @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0234(self):
        """检查视频呼叫-未订购每月10G用户--用户在WiFi环境下不提示此类弹窗"""
        # 1.客户端已登录
        # 2.未订购每月10G用户
        # 3.网络使用WIFI
        # 1.发起视频通话
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_call_time()
        CallContactDetailPage().click_video_call()
        time.sleep(2)
        # 1.直接发起语音通话，没有弹窗
        cpg.page_should_not_contain_text("每月10G免流特权")
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        time.sleep(1)
        CallContactDetailPage().wait_for_profile_name()
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0261(self):
        """检查视频通话--呼叫界面缩放按钮"""
        # 1.A已登录和飞信
        # 2.用户A进入到视频呼叫界面
        # 3.已开启“麦克风权限”、“相机权限”
        cpg = CallPage()
        cpg.create_call_entry("15343038867")
        cpg.click_call_time()
        ccdp = CallContactDetailPage()
        ccdp.click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # Step:1.用户A点击左上角的“缩放”按钮
        ccdp.click_switch()
        time.sleep(2)

        # CheckPoint:1.呼叫界面缩小至悬浮窗，文案显示“视频通话呼叫中”
        self.assertTrue(cpg.is_on_this_messagepage())
        cpg.page_should_contain_text("你正在视频通话")

        # Step:2.点击悬浮窗
        ccdp.click_video_call_status()

        # CheckPoint：2.返回到呼叫界面
        cpg.page_should_contain_text("视频通话呼叫中")
        cpg.is_on_this_messagepage()

        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0307(self):
        """检查断网无法发起视频通话"""
        # 1.已登录和飞信
        # 2.已开启“麦克风权限”
        # 3.当前已断网
        cpg = CallPage()
        self.test_call_shenlisi_0213()
        cpg.set_network_status(0)
        # 1.从单聊会话窗口发起视频通话
        ContactsPage().click_message_icon()
        Preconditions.enter_single_chat_page("给个红包2")
        BaseChatPage().click_more()
        ChatMorePage().click_voice_and_video_call()
        time.sleep(1)
        cpg.click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        self.assertTrue(cpg.is_toast_exist("当前网络不可用，请检查网络设置"))
        cpg.click_back_by_android()
        # 2.从拨号盘发起视频通话--6.2.9版本已取消拨号盘视频通话

        # 3.从通话记录-重拨视频通话
        cpg.click_call()
        time.sleep(1)
        cpg.click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        self.assertTrue(cpg.is_toast_exist("当前网络不可用，请检查网络设置"))

        # 4.从通话profile发起视频通话
        cpg.create_call_entry("13800138001")
        cpg.click_call_time()
        CallContactDetailPage().click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        self.assertTrue(cpg.is_toast_exist("当前网络不可用，请检查网络设置"))
        cpg.click_back_by_android()

        # 5.从profile发起视频通话
        # CheckPoint：1.视频通话发起失败，提示“当前网络不可用”
        cpg.enter_contact_details("给个红包2")
        CallContactDetailPage().click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        self.assertTrue(cpg.is_toast_exist("当前网络不可用，请检查网络设置"))
        cpg.click_back_by_android()
        cpg.click_call()

    @staticmethod
    def tearDown_test_call_shenlisi_0307():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0314(self):
        """检查通话界面发起多方视频"""
        # 1.客户端已登陆在：通话界面
        # 2.网络正常
        # 3.成员手机号有效
        # Step:1.点击【多方视频】按钮
        cpg = CallPage()
        cmvp = MultiPartyVideoPage()
        cpg.click_multi_party_video()
        time.sleep(2)
        # CheckPoint:1.跳转至发起视频-选择成员界面
        self.assertTrue(cmvp.is_on_multi_party_video_page())
        # Step:2.选择成员
        # 选择本地一个，号码搜索一个
        cmvp.click_contact_head()
        time.sleep(1)
        cmvp.input_contact_search("13537795364")
        cpg.click_text("未知号码")
        # CheckPoint:2.被选的成员接显示在已选成员列表
        self.assertTrue(cmvp.is_exist_contact_selection())
        # Step:3.点击【呼叫】按钮
        cmvp.click_tv_sure()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        GrantPemissionsPage().allow_contacts_permission()
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        time.sleep(2)
        # CheckPoint:3.转入多方视频拨通界面
        cpg.page_should_contain_text("关闭摄像头")

    @unittest.skip("跳过")
    # @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0317(self):
        """检查通话界面邀请多个非RCS用户（网内）发起多方视频"""
        # 1.客户端已登陆在：通话界面
        # 2.网络正常
        # 3.已邀请内网非RCS用户并进入到多方视频拨通界面
        cpg = CallPage()
        cmvp = MultiPartyVideoPage()
        cpg.click_multi_party_video()
        time.sleep(1)
        # 添加2个移动卡非和飞信用户成员
        cmvp.input_contact_search("13800138005")
        cmvp.click_contact_head()
        time.sleep(1)
        cmvp.input_contact_search("13800138006")
        cmvp.click_contact_head()
        # Step:1.查看界面
        cmvp.click_tv_sure()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        GrantPemissionsPage().allow_contacts_permission()
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        time.sleep(2)
        # CheckPoint:1.非RCS用户头像显示“未开通”，随后自动挂断
        # TODO 未显示"未开通"，用例待确认

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0324(self):
        """在通话界面邀请无效手机号发起多方视频"""
        # 1.客户端已登陆在：通话界面
        # 2.网络正常
        # 3.邀请无效手机号进入到多方视频通话
        cpg = CallPage()
        cmvp = MultiPartyVideoPage()
        # Step:1.【多方视频】按钮
        cpg.click_multi_party_video()
        time.sleep(2)
        # CheckPoint:1.跳转至发起视频-选择成员界面
        self.assertTrue(cmvp.is_on_multi_party_video_page())
        # Step:2.输入任意非手机号数字
        cmvp.input_contact_search("13800138005991")
        time.sleep(2)
        # CheckPoint:2.联系人选择器无法识别出无效手机号
        cpg.page_should_not_contain_text("本地联系人")
        cpg.page_should_not_contain_text("网络搜索")

        cpg.click_back_by_android()

    @unittest.skip("跳过")
    # @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0325(self):
        """在通话界面邀请单个非RCS用户发起视频通话"""
        # 1.客户端已登陆在：通话界面
        # 2.网络正常
        # Step:1.点击【多方视频】按钮
        cpg = CallPage()
        cmvp = MultiPartyVideoPage()
        cpg.click_multi_party_video()
        time.sleep(2)
        # CheckPoint:1.进入到联系人选择器界面
        self.assertTrue(cmvp.is_on_multi_party_video_page())
        # Step:2.邀请单个内网非RCS用户
        cmvp.input_contact_search("13800138005")
        cmvp.click_contact_head()
        cmvp.click_tv_sure()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        GrantPemissionsPage().allow_contacts_permission()
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        time.sleep(2)
        # CheckPoint:2.转1v1视频聊天界面
        cpg.page_should_contain_text("")
        # TODO
        # CheckPoint:3.转1v1视频聊天界面
        # Step:3.邀请单个异网非RCS用户
        # CheckPoint:4.转1v1视频聊天界面
        # Step:4.邀请单个香港非RCS用户

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0326(self):
        """检查无副号时通话记录列表页面"""
        # 1.用户已登录和飞信通话记录列表页面
        # 2.无副号
        cpg = CallPage()
        time.sleep(1)
        # Step:1，查看界面
        # CheckPoint:1.左上角显示“通话”，右边显示“视频”按钮，中间显示通话记录，右下方显示“多方电话”悬浮
        self.assertTrue(cpg.check_call_display())
        self.assertTrue(cpg.check_multiparty_video())
        self.assertTrue(cpg.check_free_call())
        # Step:2.点击拨号盘
        cpg.click_call()
        # CheckPoint:2.弹出拨号盘，顶部栏被遮挡
        self.assertFalse(cpg.check_call_display())
        self.assertFalse(cpg.check_multiparty_video())
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0328(self):
        """检查通通话列表为空"""
        # 1.用户已登录和飞信通话记录列表页面
        # 2.通讯录为空
        cpg = CallPage()
        time.sleep(1)
        # Step:1，查看界面
        # CheckPoint:1.界面logo提示“给你的好友打个电话吧”
        self.assertTrue(cpg.check_call_image())
        cpg.page_should_contain_text("高清通话，高效沟通")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0329(self):
        """检查通话记录展示"""
        # 1.用户已登录和飞信通话记录列表页面
        # 2.检查通话tab存在超一屏的通话记录
        cpg = CallPage()
        cpg.click_call()
        for i in range(10):
            callselect = CallTypeSelectPage()
            number = "1534303000" + str(i)
            print(number)
            cpg.dial_number(number)
            cpg.click_call_phone()
            callselect.click_call_by_general()
            time.sleep(1)
            cpg.hang_up_the_call()
        if cpg.is_on_the_dial_pad():
            cpg.click_call()
        time.sleep(1)
        # Step:1.查看界面
        # CheckPoint:1.通话记录按最近顺序展示
        self.assertTrue(cpg.get_call_history(index=0)[0:11] == "15343030009")
        self.assertTrue(cpg.get_call_history(index=1)[0:11] == "15343030008")
        self.assertTrue(cpg.get_call_history(index=2)[0:11] == "15343030007")
        self.assertTrue(cpg.get_call_history(index=3)[0:11] == "15343030006")
        self.assertTrue(cpg.get_call_history(index=4)[0:11] == "15343030005")

        # Step:2.滑动屏幕
        # CheckPoint:2.超过一屏的通话记录，可滑动
        #  向上滑动
        for i in range(2):
            cpg.swipe_by_percent_on_screen(50, 80, 50, 30, 800)
        cpg.page_should_contain_text("15343030000")
        #  向下滑动
        for i in range(2):
            cpg.swipe_by_percent_on_screen(50, 30, 50, 80, 800)
        cpg.page_should_contain_text("15343030009")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0347(self):
        """检查本地联系人通话profile左上角显示名称"""
        # 1.已登录和飞信：通话tab
        # 2.已存在与本地联系人的通话记录M
        # Step:1.点击记录M的时间节点
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_call_time()
        # CheckPoint:1.进入到M的通话profile界面
        time.sleep(1)
        self.assertTrue(cpg.is_exist_profile_name())
        # Step:2.查看左上角的名称
        ret = cpg.get_profile_name()
        # CheckPoint:2.左上角<按钮。以及M名称
        self.assertEqual(ret, "给个红包2")
        # Step:3.点击<按钮>
        CallContactDetailPage().click_back()
        time.sleep(2)
        # CheckPoint:3.返回到上一个界面
        self.assertTrue(cpg.is_on_the_call_page())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0348(self):
        """检查陌生联系人通话profile左上角显示手机号"""
        # 1.已登录和飞信：通话tab
        # 2.已存在与陌生联系人的通话记录M
        # Step:1.点击记录M的时间节点
        cpg = CallPage()
        cpg.create_call_entry("0731210086")
        cpg.click_call_time()
        # CheckPoint:1.进入到M的通话profile界面
        time.sleep(1)
        self.assertTrue(cpg.is_exist_profile_name())
        # Step:2.查看左上角的名称
        ret = cpg.get_profile_name()
        # CheckPoint:2.左上角<按钮。以及N的手机号
        self.assertEqual(ret, "0731210086")
        # Step:3.点击<按钮>
        CallContactDetailPage().click_back()
        time.sleep(2)
        # CheckPoint:3.返回到上一个界面
        self.assertTrue(cpg.is_on_the_call_page())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0350(self):
        """检查通话profile界面物理返回按钮"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        # Step:1.点击手机的物理“返回”按钮
        cpg = CallPage()
        cpg.create_call_entry("0731210086")
        cpg.click_call_time()
        time.sleep(2)
        self.assertTrue(cpg.is_exist_profile_name())
        cpg.click_back_by_android()
        time.sleep(1)
        # CheckPoint:1.返回值通话记录列表页面
        self.assertTrue(cpg.is_on_the_call_page())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0353(self):
        """检查通话profile界面可进入到消息会话窗口"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        # 本地联系人
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_call_time()
        time.sleep(1)
        self.assertTrue(cpg.is_exist_profile_name())
        # Step:1.点击消息按钮
        CallContactDetailPage().click_normal_message()

        # CheckPoint:1.进入到与该联系人的消息会话框。本地联系人左上角显示名称。陌生联系人，左上角显示手机号
        chatpage = BaseChatPage()
        flag = chatpage.is_exist_dialog()
        if flag:
            chatpage.click_i_have_read()
        cpg.page_should_contain_text("说点什么...")
        cpg.page_should_contain_text("给个红包2")
        cpg.click_back_by_android(2)

        # 陌生联系人
        Preconditions.make_already_in_call()
        cpg.create_call_entry("0731210086")
        cpg.click_call_time()
        time.sleep(1)
        self.assertTrue(cpg.is_exist_profile_name())
        # Step:1.点击消息按钮
        CallContactDetailPage().click_normal_message()
        # CheckPoint:1.进入到与该联系人的消息会话框。本地联系人左上角显示名称。陌生联系人，左上角显示手机号
        chatpage = BaseChatPage()
        flag = chatpage.is_exist_dialog()
        if flag:
            chatpage.click_i_have_read()
        cpg.page_should_contain_text("说点什么...")
        cpg.page_should_contain_text("0731210086")
        cpg.click_back_by_android(2)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0354(self):
        """检查通话profile界面发起普通电话"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        # 3.有效手机号
        # Step:1.点击电话按钮
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_call_time()
        CallContactDetailPage().click_normal_call()
        time.sleep(1)
        # CheckPoint:1.调起系统电话后
        flag = cpg.is_phone_in_calling_state()
        self.assertTrue(flag)
        cpg.hang_up_the_call()
        cpg.click_back_by_android(2)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0355(self):
        """检查通话profile界面发起语音通话"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        # 3.有效手机号
        # Step:1.点击语音通话按钮
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_call_time()
        CallContactDetailPage().click_voice_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        GrantPemissionsPage().allow_contacts_permission()
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # CheckPoint:1.发起1v1语音呼叫
        CallContactDetailPage().wait_for_profile_name()
        cpg.click_back_by_android()
        cpg.page_should_contain_text("语音通话")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0356(self):
        """检查通话profile界面发起视频通话"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        # 3.有效手机号
        # Step:1.点击视频通话
        cpg = CallPage()
        cpg.create_call_entry("13537795364")
        cpg.click_call_time()
        CallContactDetailPage().click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        GrantPemissionsPage().allow_contacts_permission()
        time.sleep(2)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        # CheckPoint:1.发起1v1视频呼叫
        CallContactDetailPage().wait_for_profile_name()
        cpg.click_back_by_android()
        cpg.page_should_contain_text("视频通话")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0357(self):
        """检查通话profile发起和飞信电话"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        # 3.有效手机号
        # Step:1.点击和飞信电话
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_call_time()
        CallContactDetailPage().click_dial_hefeixin()
        time.sleep(2)
        if cpg.is_text_present("我知道了"):
            # 点击‘我知道了’
            CalllogBannerPage().click_i_know()
        if cpg.is_exist_know():
            cpg.click_know()
        time.sleep(1)
        if cpg.is_text_present("暂不开启"):
            cpg.click_text("暂不开启")
        cpg.wait_until(timeout=30, auto_accept_permission_alert=True, condition=lambda d: cpg.is_text_present("和飞信电话"))
        # CheckPoint:1，发起和飞信电话，可收到本机回呼
        flag = cpg.is_phone_in_calling_state()
        self.assertTrue(flag)
        cpg.page_should_contain_text("和飞信电话")
        cpg.hang_up_the_call()
        CallContactDetailPage().wait_for_profile_name()
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0358(self):
        """检查本地联系人通话profile"""
        # 1.已登录和飞信-通话记录列表
        # 2.已进入到本地联系人A的通话profile
        # 3.用户A为RCS用户并保存至本地
        # 4.当前登录账号无副号
        # Step:1.查看界面
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_call_time()
        time.sleep(2)
        # CheckPoint:1.进功能有：星标、编辑、分享名片。消息、电话、语音通话、视频通话、和飞信电话高亮。页面显示：在和飞信电话按钮下显示公司、职位、邮箱（公司、职位、邮箱有则显示），通话记录。底部显示【分享名片】，点击调起联系人选择器
        self.assertTrue(CallContactDetailPage().is_exist_star())
        cpg.page_should_contain_text("编辑")
        cpg.page_should_contain_text("分享名片")
        cpg.page_should_contain_text("消息")
        cpg.page_should_contain_text("电话")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("视频通话")
        cpg.page_should_contain_text("和飞信电话")
        cpg.page_should_contain_text("拨出电话")
        CallContactDetailPage().click_share_card()
        time.sleep(2)
        cpg.page_should_contain_text("选择联系人")

        cpg.click_back_by_android(2)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0360(self):
        """检查陌生人通话profile"""
        # 1.已登录和飞信-通话记录列表
        # 2.已进入到陌生联系人B的通话profile
        # 3.用户B为RCS用户并为陌生人
        # 4.当前登录账号无副号
        # Step:1.查看界面
        cpg = CallPage()
        cpg.create_call_entry("13537795364")
        cpg.click_call_time()
        # CheckPoint:1.功能有：保存到通讯录。消息、电话、语音通话、视频通话、和飞信电话高亮。页面显示：在和飞信电话按钮下显示通话记录。底部显示【保存到通讯录】，点击进入到编辑页面
        time.sleep(2)
        cpg.page_should_contain_text("保存到通讯录")
        cpg.page_should_contain_text("消息")
        cpg.page_should_contain_text("电话")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("视频通话")
        cpg.page_should_contain_text("和飞信电话")
        cpg.page_should_contain_text("拨出电话")
        CallContactDetailPage().click_share_card()
        time.sleep(2)
        cpg.page_should_contain_text("新建联系人")

        cpg.click_back_by_android(3)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0364(self):
        """检查无效手机号profile无法发起语音通话"""
        # 1.联系人A：11位数内陆手机号（1322456546）
        # 2.联系人B：13位数手机号（132367849098）
        # 3.联系人C：无效区号+手机号（+85213260892669/+8667656003）
        # 4.联系人D：7位数香港无效手机号（6765600）
        # 5.联系人E：9位数香港无效手机号（676660056）
        # 6.联系人F：123456789012
        # 1.进入到联系人A的通话profile，发起语音通话
        # 2.进入到联系人B的通话profile，发起语音通话
        # 3.进入到联系人C的通话profile，发起语音通话
        # 4.进入到联系人D的通话profile，发起语音通话
        # 5.进入到联系人E的通话profile，发起语音通话
        # 6.进入到联系人F的通话profile，发起语音通话
        # 步骤1 - 6：发起语音通话失败，提示“号码有误
        lst = ["1322456546", "132367849098", "+85213260892669", "6765600", "676660056", "123456789012"]
        cpg = CallPage()
        ccdpg = CallContactDetailPage()
        for i in range(6):
            cpg.create_call_entry(str(lst[i]))
            cpg.click_call_time()
            ccdpg.click_voice_call()
            self.assertTrue(cpg.is_toast_exist("号码有误"))
            cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0365(self):
        """检查无效手机号profile无法发起视屏通话"""
        # 1.联系人A：11位数内陆手机号（1322456546）
        # 2.联系人B：13位数手机号（132367849098）
        # 3.联系人C：无效区号+手机号（+85213260892669/+8667656003）
        # 4.联系人D：7位数香港无效手机号（6765600）
        # 5.联系人E：9位数香港无效手机号（676660056）
        # 6.联系人F：123456789012
        # 1.进入到联系人A的通话profile，发起语音通话
        # 2.进入到联系人B的通话profile，发起语音通话
        # 3.进入到联系人C的通话profile，发起语音通话
        # 4.进入到联系人D的通话profile，发起语音通话
        # 5.进入到联系人E的通话profile，发起语音通话
        # 6.进入到联系人F的通话profile，发起语音通话
        # 步骤1 - 6：发起语音通话失败，提示“号码有误
        lst = ["1322456546", "132367849098", "+85213260892669", "6765600", "676660056", "123456789012"]
        cpg = CallPage()
        ccdpg = CallContactDetailPage()
        for i in range(6):
            cpg.create_call_entry(str(lst[i]))
            cpg.click_call_time()
            ccdpg.click_video_call()
            self.assertTrue(cpg.is_toast_exist("号码有误"))
            cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0366(self):
        """检查检查内陆固话profile发起语音通话提示号码无效"""
        # 1.已登录和飞信
        # 2.进入到内陆固号通话profile界面
        cpg = CallPage()
        cpg.create_call_entry("0731210086")
        cpg.click_call_time()
        # Step:1.点击语音通话
        ccdp = CallContactDetailPage()
        ccdp.click_voice_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        # CheckPoint:1.提示“号码有误”
        flag = cpg.is_toast_exist("号码有误")
        self.assertTrue(flag)
        # Step:2.点击视频通话
        ccdp.click_video_call()
        time.sleep(1)
        if cpg.is_text_present("继续拨打"):
            cpg.click_text("继续拨打")
        # CheckPoint:2.提示“号码有误”
        flag = cpg.is_toast_exist("号码有误")
        self.assertTrue(flag)
        cpg.click_back_by_android(2)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0369(self):
        """检查新建联系人功能--修改手机号"""
        # 1.已登录和飞信
        # 2.进入到陌生人通话profile
        cpg = CallPage()
        cpg.create_call_entry("0731210086")
        cpg.click_call_time()
        # Step:1.点击保存到本地通讯录按钮
        CallContactDetailPage().click_share_card()
        time.sleep(1)
        # CheckPoint:1.进入新建联系人界面
        cpg.page_should_contain_text("新建联系人")
        ncpg = NewOrEditContactPage()
        ncpg.hide_keyboard()
        # Step:2.编辑基础数据，修改手机号
        ncpg.input_name("中国移动")
        ncpg.input_contact_info(1, "13800138110")
        ncpg.input_contact_info(2, "中软国际")
        ncpg.input_contact_info(3, "自动化开发")
        # Step:3.点击右上角的保存按钮
        ncpg.click_save_or_sure()
        cpg.wait_until(timeout=15, auto_accept_permission_alert=True, condition=lambda d: cpg.is_text_present("和飞信电话"))
        # CheckPoint::3：跳转到联系人profile
        self.assertTrue(cpg.is_exist_profile_name())
        # Step:4.点击返回
        cpg.click_back_by_android()
        time.sleep(1)
        # CheckPoint:4：返回到通话记录列表
        self.assertTrue(cpg.check_multiparty_video())

    @staticmethod
    def tearDown_test_call_shenlisi_0369():
        """删除指定联系人"""
        ContactDetailsPage().delete_contact("中国移动")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0370(self):
        """检查新建联系人功能--不修改手机号"""
        # 1.已登录和飞信
        # 2.进入到陌生人通话profile
        cpg = CallPage()
        cpg.create_call_entry("0731210086")
        cpg.click_call_time()
        # Step:1.点击保存到本地通讯录按钮
        CallContactDetailPage().click_share_card()
        time.sleep(2)
        # CheckPoint:1.进入新建联系人界面
        cpg.page_should_contain_text("新建联系人")
        ncpg = NewOrEditContactPage()
        ncpg.hide_keyboard()
        # Step:2.编辑基础数据，不修改手机号
        ncpg.input_name("中国移动")
        ncpg.input_contact_info(2, "中软国际")
        ncpg.input_contact_info(3, "自动化开发")

        # Step:3.点击右上角的保存按钮
        ncpg.click_save_or_sure()
        cpg.wait_until(timeout=15, auto_accept_permission_alert=True, condition=lambda d: cpg.is_text_present("和飞信电话"))
        # CheckPoint::3：跳转到联系人profile
        self.assertTrue(cpg.is_exist_profile_name())
        # Step:4.点击返回
        cpg.click_back_by_android()
        time.sleep(1)
        # CheckPoint:4：返回到通话记录列表，更新通话记录，更新与该联系人通话记录的名称
        self.assertTrue(cpg.check_multiparty_video())
        cpg.page_should_contain_text("中国移动")

    @staticmethod
    def tearDown_test_call_shenlisi_0370():
        """删除指定联系人"""
        ContactDetailsPage().delete_contact("中国移动")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0371(self):
        """检查编辑本地联系人-修改手机号"""
        # 1.已登录和飞信
        # 2.进入到本地联系人通话profile
        cpg = CallPage()
        cpg.create_call_entry("13800138008")
        cpg.click_call_time()
        # Step:1.点击编辑按钮
        CallContactDetailPage().click_call_detail_edit()
        time.sleep(1)
        ncpg = NewOrEditContactPage()
        ncpg.hide_keyboard()
        # CheckPoint:1.进入编辑联系人界面
        self.assertTrue(ncpg.is_text_present("编辑联系人"))
        # Step:2.编辑基础数据，修改手机号
        ncpg.input_contact_info(1, "13800138009")
        ncpg.input_contact_info(2, "中软国际")
        ncpg.input_contact_info(3, "自动化开发")
        time.sleep(1)
        # Step:3.点击右上角的保存按钮
        ncpg.click_save_or_sure()
        cpg.wait_until(timeout=15, auto_accept_permission_alert=True, condition=lambda d: cpg.is_text_present("和飞信电话"))
        # CheckPoint3：跳转到联系人profile
        self.assertTrue(cpg.is_exist_profile_name())
        # Step:4.点击返回
        cpg.click_back_by_android()
        time.sleep(1)
        # CheckPoint4：返回到通话记录列表
        self.assertTrue(cpg.check_multiparty_video())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0372(self):
        """检查编辑本地联系人-修改名称、公司、职位、邮箱字段"""
        # 1.已登录和飞信
        # 2.进入到本地联系人通话profile
        cpg = CallPage()
        cpg.create_call_entry(text="13800138007")
        cpg.click_call_time()
        # 1.点击编辑按钮
        CallContactDetailPage().click_call_detail_edit()
        time.sleep(1)
        ncpg = NewOrEditContactPage()
        ncpg.hide_keyboard()
        # 1.进入编辑系人界面
        self.assertTrue(ncpg.is_text_present("编辑联系人"))
        # 2.编辑基础数据，不修改手机号
        ncpg.input_name("中软国际")
        ncpg.input_contact_info(2, "中软国际")
        ncpg.input_contact_info(3, "自动化开发")
        time.sleep(1)
        # 3.点击右上角的保存按钮
        ncpg.click_save_or_sure()
        cpg.wait_until(timeout=15, auto_accept_permission_alert=True, condition=lambda d: cpg.is_text_present("和飞信电话"))
        # 3：跳转到联系人通话profile
        self.assertTrue(cpg.is_exist_profile_name())
        # 4.点击返回
        cpg.click_back_by_android()
        time.sleep(1)
        # 4：返回到通话记录列表，更新通话记录，更新与该联系人通话记录的名称
        self.assertTrue(cpg.check_multiparty_video())
        cpg.page_should_contain_text("中软国际")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0373(self):
        """检查编辑联系人界面-删除功能"""
        # 1.已登录和飞信
        # 2.进入到编辑联系人界面
        cpg = CallPage()
        cpg.create_call_entry("13800138006")
        cpg.click_call_time()
        CallContactDetailPage().click_call_detail_edit()
        time.sleep(1)
        ncpg = NewOrEditContactPage()
        ncpg.hide_keyboard()
        # 1.点击删除联系人按钮
        ncpg.click_delete_number()
        ncpg.click_sure_delete()
        # 1.提示删除成功，跳转到通话记录列表，同时更新列表，被删除的联系人通话记录显示手机号
        time.sleep(1)
        flag = cpg.is_toast_exist("删除成功")
        self.assertTrue(flag)
        time.sleep(2)
        self.assertTrue(cpg.check_multiparty_video())
        cpg.page_should_contain_text("13800138006")

