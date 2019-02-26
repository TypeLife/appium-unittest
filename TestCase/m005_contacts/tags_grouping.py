import unittest
import uuid

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.call.multipartycall import MultipartyCallPage
from pages.call.mutivideo import MutiVideoPage
from pages.components import ContactsSelector
from pages.components.dialogs import SuspendedTips, MutiVideoTipsPage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
}


class Preconditions(object):
    """
    分解前置条件
    """

    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def make_already_in_one_key_login_page():
        """
        1、已经进入一键登录页
        :return:
        """
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            current_mobile().launch_app()
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
        one_key.wait_for_tell_number_load(60)
        login_number = one_key.get_login_number()
        one_key.click_one_key_login()
        one_key.click_read_agreement_detail()

        # 同意协议
        agreement = AgreementDetailPage()
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)
        return login_number

    @staticmethod
    def take_logout_operation_if_already_login():
        """已登录状态，执行登出操作"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

        me = MePage()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.click_setting_menu()

        setting = SettingPage()
        setting.scroll_to_bottom()
        setting.click_logout()
        setting.click_ok_of_alert()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def terminate_app():
        """
        强制关闭app,退出后台
        :return:
        """
        app_id = current_driver().desired_capability['appPackage']
        current_mobile().termiate_app(app_id)

    @staticmethod
    def background_app():
        """后台运行"""
        current_mobile().press_home_key()

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """
        前置条件：
        1.已登录客户端
        2.当前在消息页面
        """
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
    def create_contacts_if_not_exits(name, number):
        """
        导入联系人数据
        :param name:
        :param number:
        :return:
        """
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        try:
            contacts_page.wait_for_page_load()
            contacts_page.open_contacts_page()
        except:
            Preconditions.make_already_in_message_page(reset_required=False)
            contacts_page.open_contacts_page()
        # 创建联系人
        contacts_page.click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(name)
        if contact_search.is_contact_in_list(name):
            contact_search.click_back()
        else:
            contact_search.click_back()
            contacts_page.click_add()
            create_page = CreateContactPage()
            create_page.hide_keyboard_if_display()
            create_page.create_contact(name, number)
            detail_page.wait_for_page_load()
            detail_page.click_back_icon()


class TagsGroupingTest(TestCase):
    """通讯录 - 标签分组"""

    @classmethod
    def setUpClass(cls):
        # 创建联系人
        fail_time = 0
        import dataproviders

        while fail_time < 3:
            try:
                # 获取需要导入的联系人数据
                required_contacts = dataproviders.get_preset_contacts()

                # 连接手机
                Preconditions.connect_mobile('Android-移动')
                current_mobile().hide_keyboard_if_display()
                # 导入数据
                for name, number in required_contacts:
                    Preconditions.create_contacts_if_not_exits(name, number)

                # 推送resource文件到手机
                dataproviders.push_resource_dir_to_mobile_sdcard(Preconditions.connect_mobile('Android-移动'))
                return
            except:
                fail_time += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_TagsGrouping_0001(self):
        """无分组"""
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_label_grouping()
        lg = LabelGroupingPage()
        lg.wait_for_page_load()
        lg.delete_all_label()
        lg.assert_default_status_is_right()

        lg.wait_for_page_load()
        lg.click_back()
        conts_page.open_message_page()

    def setUp_test_Conts_TagsGrouping_0001(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_TagsGrouping_0002(self):
        """多个分组"""
        groups = [
            ['分组1'],
            ['分组2'],
            ['分组3'],
            ['分组4'],
            ['分组5'],
            ['分组6'],
            ['分组7'],
            ['分组8'],
            ['分组9'],
            ['分组10'],
            ['分组11'],
        ]
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_label_grouping()
        lg = LabelGroupingPage()
        lg.wait_for_page_load()
        for g in groups:
            lg.create_group(*g)
        lg.wait_for_page_load()
        lg.delete_label_groups(*groups)

        lg.wait_for_page_load()
        lg.click_back()
        conts_page.open_message_page()

    def setUp_test_Conts_TagsGrouping_0002(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_TagsGrouping_0003(self):
        """新建分组"""
        group_name = uuid.uuid4().__str__()
        groups = [
            [group_name, '给个红包1'],
        ]
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_label_grouping()
        lg = LabelGroupingPage()
        lg.wait_for_page_load()
        for g in groups:
            lg.create_group(*g)
        lg.wait_for_page_load()
        lg.delete_all_label()

        lg.wait_for_page_load()
        lg.click_back()
        conts_page.open_message_page()

    def setUp_test_Conts_TagsGrouping_0003(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_TagsGrouping_0004(self):
        """联系人选择器页面"""
        group_name = uuid.uuid4().__str__()

        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_label_grouping()
        lg = LabelGroupingPage()
        lg.click_new_create_group()
        lg.wait_for_create_label_grouping_page_load()
        real_name = lg.input_label_grouping_name(group_name)
        lg.click_sure()
        lg.wait_for_contacts_selector_page_load()
        lg.assert_contacts_selector_page_title_is_right()
        lg.assert_contacts_selector_page_display_ok_button()
        lg.assert_contacts_selector_search_box_place_holder_is_right()
        lg.assert_contacts_selector_page_contains_text('选择和通讯录联系人')
        lg.assert_contacts_selector_page_contains_alphabet_nav()

        lg.click_back()
        lg.click_back()
        lg.wait_for_page_load()
        lg.delete_label_groups(real_name)

        lg.wait_for_page_load()
        lg.click_back()
        conts_page.open_message_page()

    def setUp_test_Conts_TagsGrouping_0004(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_TagsGrouping_0006(self):
        """修改标签名称"""
        group_name = uuid.uuid4().__str__()

        # 进入标签分组列表页面
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_label_grouping()

        # 创建分组
        lg = LabelGroupingPage()
        old_group = lg.create_group(group_name)

        # 修改名字
        lg.wait_for_page_load()
        new_name = 'TestData001'
        actual = lg.rename_label_group(old_group, new_name)

        # 验证检查点
        self.assertEqual(new_name, actual, '检查点：标签名称修改成功')

        # 返回到标签分组页面并删除该用例创建的分组数据
        lg.wait_for_page_load()
        lg.delete_label_groups(actual)

        lg.wait_for_page_load()
        lg.click_back()
        conts_page.open_message_page()

    def setUp_test_Conts_TagsGrouping_0006(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_TagsGrouping_0007(self):
        """移除成员"""
        group_name = uuid.uuid4().__str__()
        members = ['给个红包1']
        # 进入标签分组列表页面
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_label_grouping()

        # 创建分组
        lg = LabelGroupingPage()
        real_name = lg.create_group(group_name, *members)

        # 修改名字
        lg.wait_for_page_load()
        lg.remove_group_members(real_name, *members)
        lg.wait_for_page_load()
        count = lg.get_group_member_count(real_name)

        # 验证检查点
        self.assertEqual(count, 0, '检查点：成员被移除')

        # 返回到标签分组页面并删除该用例创建的分组数据
        lg.wait_for_page_load()
        lg.delete_label_groups(real_name)

        lg.wait_for_page_load()
        lg.click_back()
        conts_page.open_message_page()

    def setUp_test_Conts_TagsGrouping_0007(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_TagsGrouping_0008(self):
        """删除标签"""
        group_name = uuid.uuid4().__str__()
        members = ['给个红包1']
        # 进入标签分组列表页面
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_label_grouping()

        # 创建分组
        lg = LabelGroupingPage()
        real_name = lg.create_group(group_name, *members)

        # 删除点取消
        lg.wait_for_page_load()
        lg.cancel_delete_label_groups(real_name)
        # 删除点确定
        lg.wait_for_page_load()
        lg.delete_label_groups(real_name)

        lg.wait_for_page_load()
        lg.click_back()
        conts_page.open_message_page()

    def setUp_test_Conts_TagsGrouping_0008(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_TagsGrouping_0009(self):
        """群发信息"""
        group_name = uuid.uuid4().__str__()
        members = [
            '给个红包1',
            '给个红包2',
        ]
        # 进入标签分组列表页面
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_label_grouping()

        # 创建分组
        lg = LabelGroupingPage()
        real_name = lg.create_group(group_name, *members)

        # 删除点取消
        lg.wait_for_page_load()
        lg.click_label_group(real_name)

        detail = LableGroupDetailPage()
        detail.click_send_group_info()

        chat = ChatWindowPage()
        if chat.is_tips_display():
            chat.directly_close_tips_alert()
        chat.send_img_msgs({'pic': (1,)})
        max_wait_time = 5  # in seconds
        try:
            chat.wait_for_msg_send_status_become_to('发送成功', max_wait_time)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(max_wait_time))

    def setUp_test_Conts_TagsGrouping_0009(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_TagsGrouping_0010(self):
        """多方电话"""
        group_name = uuid.uuid4().__str__()
        members = [
            '给个红包1',
            '给个红包2',
        ]
        # 进入标签分组列表页面
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_label_grouping()

        # 创建分组
        lg = LabelGroupingPage()
        real_name = lg.create_group(group_name, *members)

        # 进入分组
        lg.wait_for_page_load()
        lg.click_label_group(real_name)

        # 点击多方通话
        detail = LableGroupDetailPage()
        detail.click_multi_tel()

        # 选择联系人
        contacts_selector = ContactsSelector()
        contacts_selector.select_local_contacts(*members)

        mtc = MultipartyCallPage()
        mtc.ignore_tips_if_tips_display()

        # 检查点：进入多方通话主叫页面
        mtc.assert_caller_tips_is_display()

        # 等待来电
        mtc.wait_for_call_back(max_wait_time=16)
        # 挂断电话
        current_mobile().hang_up_the_call()

    def setUp_test_Conts_TagsGrouping_0010(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_TagsGrouping_0011(self):
        """多方视频"""
        group_name = uuid.uuid4().__str__()
        members = [
            '给个红包1',
            '给个红包2',
        ]
        # 进入标签分组列表页面
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_label_grouping()

        # 创建分组
        lg = LabelGroupingPage()
        real_name = lg.create_group(group_name, *members)

        # 进入分组
        lg.wait_for_page_load()
        lg.click_label_group(real_name)

        # 点击多方视频
        detail = LableGroupDetailPage()
        detail.click_multiparty_videos()

        # 选择联系人
        contacts_selector = ContactsSelector()
        current_mobile().wait_until(
            condition=lambda d: current_mobile().is_text_present('多方视频'),
            timeout=3,
        )
        contacts_selector.select_local_contacts(*members)

        tips = MutiVideoTipsPage()
        tips.go_on_if_tips_pop_out()

        tips1 = SuspendedTips()
        tips1.ignore_tips_if_tips_display()

        mtv = MutiVideoPage()
        mtv.wait_for_page_load()

    def setUp_test_Conts_TagsGrouping_0011(self):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @classmethod
    def tearDownClass(cls):
        try:
            Preconditions.connect_mobile('Android-移动')
            current_mobile().hide_keyboard_if_display()
            Preconditions.make_already_in_message_page()
            conts_page = ContactsPage()
            conts_page.open_contacts_page()
            conts_page.click_label_grouping()
            lg = LabelGroupingPage()
            lg.wait_for_page_load()
            lg.delete_all_label()
        except:
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    unittest.main()
