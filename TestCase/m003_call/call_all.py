import preconditions
from library.core.TestCase import TestCase
from selenium.common.exceptions import TimeoutException
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.call import *
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
        """进入通话界面"""
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
    def skip_multiparty_call():
        """跳过多方通话引导页面"""
        cbg = CalllogBannerPage()
        if cbg.is_on_the_calllog_banner_page():
            cbg.multiparty_call()
            if cbg.is_text_present("始终允许"):
                CallPage().click_allow_button()

    @staticmethod
    def select_dial_mode():
        """进入拨号方式选择"""
        Preconditions.make_already_in_call()
        MessagePage().open_me_page()
        MePage().click_setting_menu()
        SettingPage().click_dial_setting()
        MeSetDialPage().click_dial_mode()

    @staticmethod
    def setting_dial_mode_and_go_back_call():
        """设置拨号方式为总是询问，并返回call界面"""
        cpg = CallPage()
        Preconditions.select_dial_mode()
        MeSetDialWayPage().click_call_type_alaways_ask()
        cpg.click_back_by_android(times=3)
        cpg.click_call()

class CallAll(TestCase):
    """
    模块：通话
    文件位置：全量/ 7.通话（拨号盘、多方视频-非RCS、视频通话、语音通话）全量测试用例-申丽思.xlsx
    表格：通话（拨号盘、多方视频-非RCS、视频通话、语音通话）
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
        Preconditions.skip_multiparty_call()
        CallPage().delete_all_call_entry()

    # def default_tearDown(self):
    #     pass

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0004(self):
        """检查拨号盘展开"""
        cpg = CallPage()
        # Step:1.点击“拨号盘"按钮
        cpg.click_call()
        # CheckPoint:1.拨号盘展示，输入框提示“直接拨号或者开始搜索”，菜单栏被隐藏
        cpg.page_should_contain_text('直接拨号或开始搜索')
        cpg.page_should_not_contain_text('多方通话')
        cpg.click_back_by_android()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0007(self):
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
    def test_call_0008(self):
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
    def test_call_0009(self):
        """检查输入框有内容时拨号盘可切换到其它模块"""
        # Step:1.切换至其它模块后又返回到拨号盘
        cpg = CallPage()
        cpg.click_call()
        time.sleep(1)
        cpg.dial_number("153")
        # CheckPoint:1.收起时切换到其他的模块，内容不清除，正常显示
        cpg.page_should_contain_text("153")
        # Step:2. 切换为消息
        cpg.click_message()
        # CheckPoint:2.收起时切换到其他的模块，内容不清除，正常显示
        cpg.page_should_not_contain_text("153")
        # Step:3. 切换为拨号盘
        cpg.click_call()
        # CheckPoint:3.收起时切换到其他的模块，内容不清除，正常显示
        cpg.page_should_contain_text("153")
        # 清除拨号盘，返回通话界面
        cpg.press_delete()
        cpg.click_call()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0010(self):
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
    def test_call_0011(self):
        """检查拨号盘“多方电话”按键可点击"""
        # Step:1.点击按键“多方电话”
        cpg = CallPage()
        cpg.click_multiparty_call_by_home()
        time.sleep(2)
        # CheckPoint:1.调起联系人多方电话联系人选择器
        cpg.page_should_contain_text("选择和通讯录联系人")
        cpg.click_back()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0012(self):
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

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0014(self):
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
    def test_call_0015(self):
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
    def test_call_0016(self):
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
    def test_call_0017(self):
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
    def test_call_0018(self):
        """检查杀掉进程会清除拨号盘的数值"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘存在数值
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("*53")

        # Step:1.杀掉进程，再次进入到和飞信-拨号盘
        preconditions.force_close_and_launch_app()
        time.sleep(2)
        # CheckPoint:1.杀死进程在进入，输入内容被清除，拨号盘默认收起
        cpg.click_call()
        cpg.page_should_not_contain_text("*53")
        flag = cpg.check_call_phone()
        self.assertFalse(flag)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0020(self):
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
    def test_call_0022(self):
        """检查拨号盘精确搜索功能---内陆本地联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的内陆号本地已保存
        cpg = CallPage()
        Preconditions.setting_dial_mode_and_go_back_call()
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
    def test_call_0023(self):
        """检查拨号盘精确搜索功能---内陆陌生联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的内陆号本地未保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        Preconditions.setting_dial_mode_and_go_back_call()
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
    def test_call_0024(self):
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
    def test_call_0025(self):
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
    def test_call_0026(self):
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
    def test_call_0027(self):
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

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0031(self):
        """检查本网用户登录，在拨号盘拨打手机号拨号方式推荐---多方时长>0"""
        # 1.异网用户已登录在通话--拨号盘
        # 2.拨号方式设置“总是询问”
        # 3.多方时长>0
        # 4.在拨号盘输入手机号
        # Step:1.点击【拨号】按钮
        # CheckPoint:1弹出拨号方式依次显示“和飞信电话（免费）、语音通话（免流量）、普通电话”
        cpg = CallPage()
        callselect = CallTypeSelectPage()
        Preconditions.setting_dial_mode_and_go_back_call()
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

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0049(self):
        """检查拨号盘取消拨号方式"""
        # 1.用户已登录和飞信：通话-拨号盘
        # 2.已弹出拨号方式
        cpg = CallPage()
        cpg.click_call()
        # Step:1.点击“取消”按钮
        cpg.click_back_by_android()
        # CheckPoint:1.拨号方式收起，停留在输入号码的拨号盘页
        cpg.page_should_not_contain_text("直接拨号或开始搜索")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0050(self):
        """拨号盘呼叫和飞信通话"""
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

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0051(self):
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

        #香港号码
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

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0061(self):
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
    def test_call_0062(self):
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
    def test_call_0063(self):
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
    def test_call_0064(self):
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
    def test_call_0065(self):
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
    def test_call_0066(self):
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
    def test_call_0315(self):
        """检查本地联系人通话profile左上角显示名称"""
        # 1.已登录和飞信：通话tab
        # 2.已存在与陌生联系人的通话记录M
        # Step:1.点击记录M的时间节点
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("0731210086")
        cpg.click_call_phone()
        # CallTypeSelectPage().click_call_by_general()
        GrantPemissionsPage().allow_contacts_permission()
        time.sleep(2)
        cpg.click_call_end()
        time.sleep(2)
        cpg.click_call_time()
        # CheckPoint:1.进入到M的通话profile界面
        time.sleep(1)
        self.assertTrue(cpg.is_exist_profile_name())
        # Step:2.查看左上角的名称
        ret = cpg.get_profile_name()
        # CheckPoint:2.左上角<按钮。以及M名称
        self.assertEqual(ret, "0731210086")
        # Step:3.点击<按钮>
        cpg.click_back()
        time.sleep(1)
        # CheckPoint:3.返回到上一个界面
        self.assertTrue(cpg.is_on_the_call_page())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0316(self):
        """检查通话profile界面物理返回按钮"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        # Step:1.点击手机的物理“返回”按钮
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("0731210086")
        cpg.click_call_phone()
        GrantPemissionsPage().allow_contacts_permission()
        time.sleep(2)
        cpg.click_call_end()
        time.sleep(2)
        cpg.click_call_time()
        time.sleep(1)
        self.assertTrue(cpg.is_exist_profile_name())
        cpg.click_back_by_android()
        time.sleep(1)
        # CheckPoint:1.返回值通话记录列表页面
        self.assertTrue(cpg.is_on_the_call_page())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0319(self):
        """检查通话profile界面可进入到消息会话窗口"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        #本地联系人
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("13800138001")
        cpg.click_call_phone()
        GrantPemissionsPage().allow_contacts_permission()
        time.sleep(2)
        CallTypeSelectPage().click_call_by_general()
        time.sleep(2)
        cpg.click_call_end()
        time.sleep(2)
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
        cpg.click_back_by_android(3)

        #陌生联系人
        cpg.click_call()
        cpg.dial_number("0731210086")
        cpg.click_call_phone()
        GrantPemissionsPage().allow_contacts_permission()
        time.sleep(2)
        cpg.click_call_end()
        time.sleep(2)
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
        cpg.click_back_by_android(3)

    @tags('ALL', 'CMCC', 'Call')
    def test_call_0320(self):
        """检查通话profile界面发起普通电话"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        # 3.有效手机号
        # Step:1.点击电话按钮
        cpg = CallPage()
        cpg.click_call()
        cpg.dial_number("13800138001")
        cpg.click_call_phone()
        GrantPemissionsPage().allow_contacts_permission()
        time.sleep(2)
        CallTypeSelectPage().click_call_by_general()
        cpg.click_call_end()
        cpg.click_call_time()
        CallContactDetailPage().click_normal_call()
        time.sleep(1)
        # CheckPoint:1.调起系统电话后
        flag = cpg.is_phone_in_calling_state()
        self.assertTrue(flag)
        cpg.hang_up_the_call()
        cpg.click_back_by_android(2)

