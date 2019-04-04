import time
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
import preconditions
from pages.contacts.ContactDetails import ContactDetailsPage
from pages.contacts.ContactDetails import add

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

    @staticmethod
    def create_contacts(name, number):
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
                   # Preconditions.create_contacts_if_not_exits(name, number)
                   Preconditions.create_contacts(name, number)

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
        try:
            current_mobile().hide_keyboard_if_display()
            Preconditions.make_already_in_message_page()
            cdp=ContactDetailsPage()
            cdp.delete_all_contact()
        except:
            traceback.print_exc()

class Tag_Group(TestCase):

    @staticmethod
    def setUp_test_contacts_quxinli_0352():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0352(self):
        """新建分组,检查元素"""
        GroupPage=GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        GroupPage.click_new_group()
        time.sleep(1)
        GroupPage.check_if_contains_element('为你的分组创建一个名称')
        GroupPage.check_if_contains_element('请输入标签分组名称')
        GroupPage.check_if_contains_element('标题新建分组')
        GroupPage.check_if_contains_element()

    @staticmethod
    def setUp_test_contacts_quxinli_0353():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0353(self):
        """新建分组,标签分组名称为空"""
        GroupPage=GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        GroupPage.click_new_group()
        GroupPage.click_sure_element()
        time.sleep(3)
        GroupPage.check_if_contains_element()

    @staticmethod
    def setUp_test_contacts_quxinli_0354():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0354(self):
        """新建分组,标签分组名称输入空格"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        GroupPage.click_coordinate()
        GroupPage.click_coordinate()
        GroupPage.click_coordinate()
        GroupPage.click_sure_element()
        time.sleep(2)
        GroupPage.check_if_contains_element()

    @staticmethod
    def setUp_test_contacts_quxinli_0355():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0355(self):
        """新建分组,标签分组名称输入9个汉字"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        GroupPage.input_content()
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        GroupPage.page_should_contain_text('选择和通讯录联系人')

    def tearDown_test_contacts_quxinli_0355(self):
        GroupPage = GroupListPage()
        GroupPage.click_back()
        GroupPage.click_back()
        GroupPage.delete_group()

    def tearDown_test_contacts_quxinli_0355(self):
        Preconditions.reset_and_relaunch_app()

    @staticmethod
    def setUp_test_contacts_quxinli_0356():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0356(self):
        """新建分组,标签分组名称输入10个汉字"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        GroupPage.input_content(text="祝一路顺风和幸福美满")
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        GroupPage.page_should_contain_text('选择和通讯录联系人')

    def tearDown_test_contacts_quxinli_0356(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='祝一路顺风和幸福美满')

    @staticmethod
    def setUp_test_contacts_quxinli_0357():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0357(self):
        """新建分组,标签分组名称输入11个汉字"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(1)
        try:
            GroupPage.input_content(text="祝一路顺风和幸福美满啊")
            flag=False
        except:
            print("分组名不能超过10个汉字.")
            flag=True
        self.assertTrue(flag)


    @staticmethod
    def setUp_test_contacts_quxinli_0358():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0358(self):
        """新建分组,标签分组名称输入29个数字"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(1)
        self.message='1'*29
        GroupPage.input_content(text=self.message)
        time.sleep(1)
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        time.sleep(1)
        GroupPage.page_should_contain_text('选择和通讯录联系人')
        GroupPage.click_back_button(times=2)

    def tearDown_test_contacts_quxinli_0358(self):
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name=self.message)

    @staticmethod
    def setUp_test_contacts_quxinli_0368():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0368(self):
        """新建分组,已添加分组后标签分组列表展示"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.new_group(name='aaa')
        GroupPage.new_group(name='bbb')
        y0=GroupPage.get_element_text_y()
        y1=GroupPage.get_element_text_y(text='aaa')
        y2=GroupPage.get_element_text_y(text='bbb')
        self.assertTrue(y0<y1<y2)

    def tearDown_test_contacts_quxinli_0368(self):
        GroupPage = GroupListPage()
        time.sleep(2)
        GroupPage.delete_group(name='aaa')
        time.sleep(1)
        GroupPage.delete_group(name='bbb')

    @staticmethod
    def setUp_test_contacts_quxinli_0369():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0369(self):
        """新建分组,已添加分组后标签分组列表展示"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.new_group()
        GroupPage.click_text('aaa')
        time.sleep(2)
        GroupPage.click_text('知道了')
        time.sleep(1)
        GroupPage.page_should_not_contain_text('知道了')
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.click_text('添加成员')
        time.sleep(1)
        GroupPage.page_should_contain_text('选择和通讯录联系人')

    def tearDown_test_contacts_quxinli_0369(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')


    @staticmethod
    def setUp_test_contacts_quxinli_0370():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0370(self):
        """新建分组,分组详情操作界面"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.new_group()
        time.sleep(1)
        GroupPage.click_text('aaa')
        time.sleep(2)
        GroupPage.click_text('知道了')
        time.sleep(1)
        GroupPage.page_contain_element()
        GroupPage.page_contain_element('群发信息')
        GroupPage.page_contain_element('多方电话')
        GroupPage.page_contain_element('多方视频')
        GroupPage.page_contain_element('设置')
        GroupPage.page_contain_element('aaa')

    def tearDown_test_contacts_quxinli_0370(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0371():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0371(self):
        """新建分组,标签分组添加成员页面"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group()
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.click_text('添加成员')
        time.sleep(1)
        GroupPage.page_contain_element('搜索或输入手机号')
        GroupPage.page_contain_element('选择联系人')
        GroupPage.page_contain_element('确定')
        GroupPage.page_contain_element('选择和通讯录联系人')

    def tearDown_test_contacts_quxinli_0371(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0372():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0372(self):
        """新建分组,标签分组添加成员页面"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.click_text('添加成员')
        time.sleep(1)
        GroupPage.click_search_box()
        time.sleep(1)
        GroupPage.input_search_text()
        time.sleep(1)
        GroupPage.page_should_contain_element1()
        GroupPage.click_text('大佬2')
        time.sleep(1)
        GroupPage.page_contain_element('搜索或输入手机号')
        GroupPage.page_contain_element('选择和通讯录联系人')

    def tearDown_test_contacts_quxinli_0372(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0373():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0373(self):
        """新建分组,标签分组添加成员页面"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.click_text('添加成员')
        time.sleep(1)
        GroupPage.click_search_box()
        time.sleep(1)
        GroupPage.input_search_text(text='13802885230')
        time.sleep(1)
        GroupPage.page_not_contain_element('联系人头像')

    def tearDown_test_contacts_quxinli_0373(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0374():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0374(self):
        """标签分组添加成员-选择本地联系人"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.add_member()

    def tearDown_test_contacts_quxinli_0374(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0375():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0375(self):
        """标签分组添加成员-选择本地联系人不可选成员"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.add_member()
        flag=GroupPage.add_member(times=2)
        self.assertTrue(flag==2)

    def tearDown_test_contacts_quxinli_0375(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        GroupPage.delete_group(name='aaa')


    @staticmethod
    def setUp_test_contacts_quxinli_0387():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0387(self):
        """分组详情操作界面-分组只有一个人员点击群发消息"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.add_member()
        GroupPage.send_message_to_group()
        GroupPage.page_contain_element(locator='大佬2')

    def tearDown_test_contacts_quxinli_0387(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0388():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0388(self):
        """分组详情操作界面-分组有多个人员点击群发消息"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.add_member(name='dalao2')
        time.sleep(2)
        GroupPage.add_member(name='dalao1')
        time.sleep(1)
        GroupPage.send_message_to_group()
        time.sleep(1)
        GroupPage.page_contain_element(locator='多方通话_图标')
        GroupPage.page_contain_element(locator='分组联系人')
        GroupPage.page_contain_element(locator='富媒体面板')
        GroupPage.page_contain_element(locator='aaa')

    def tearDown_test_contacts_quxinli_0388(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0389():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0389(self):
        """分组详情操作界面-群发消息-发送消息"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.add_member(name='dalao2')
        time.sleep(2)
        message='aa aa'*20
        GroupPage.send_message_to_group(message)
        time.sleep(1)
        GroupPage.page_contain_element('已转短信送达')
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.send_express_to_group()
        time.sleep(1)
        GroupPage.page_not_contain_element('发送失败')
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.send_picture_to_group()
        time.sleep(1)
        GroupPage.page_not_contain_element('发送失败')
        time.sleep(1)

    def tearDown_test_contacts_quxinli_0389(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')


    @staticmethod
    def setUp_test_contacts_quxinli_0394():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0394(self):
        """分组详情操作界面-群发消息-分组联系人图标"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.add_member(name='dalao2')
        time.sleep(2)
        GroupPage.add_member(name='dalao1')
        time.sleep(1)
        GroupPage.enter_group_message()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬1")
        time.sleep(1)
        GroupPage.click_star_icon()
        GroupPage.is_toast_exist("已成功添加为星标联系人")
        time.sleep(1)
        GroupPage.click_star_icon()
        GroupPage.is_toast_exist("已取消添加为星标联系人")
        GroupPage.click_star_icon()
        GroupPage.click_back_button(times=3)
        time.sleep(2)
        GroupPage.click_back_button(times=2)

        time.sleep(1)
        GroupPage.page_contain_element(locator='星标')

    def tearDown_test_contacts_quxinli_0394(self):
        GroupPage = GroupListPage()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')


    @staticmethod
    def setUp_test_contacts_quxinli_0395():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0395(self):
        """分组详情操作界面-群发消息-分组联系人图标"""
        GroupPage = GroupListPage()
        cdp=ContactDetailsPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.add_member(name='dalao2')
        time.sleep(2)
        GroupPage.add_member(name='dalao1')
        time.sleep(1)
        GroupPage.enter_group_message()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬1")
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        cdp.change_mobile_number()
        time.sleep(1)
        cdp.click_sure_icon()
        time.sleep(1)
        GroupPage.is_toast_exist("保存成功")
        cdp.is_text_present('138 0013 8006')

    def tearDown_test_contacts_quxinli_0395(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0396():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(5)
        preconditions.launch_app()
    #    Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0396(self):
        """分组联系人进入Profile页-编辑-删除联系人"""
        GroupPage = GroupListPage()
        cdp=ContactDetailsPage()
        time.sleep(1)
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.tap_sure_box()
        time.sleep(1)
        GroupPage.add_member(name='dalao5')
        time.sleep(2)
        GroupPage.add_member(name='dalao6')
        time.sleep(1)
        GroupPage.enter_group_message()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬5")
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        cdp.hide_keyboard()
        cdp.page_up()
        cdp.change_delete_number()
        cdp.click_sure_delete()
        time.sleep(1)
        GroupPage.is_toast_exist("删除成功")
        time.sleep(1)

    def tearDown_test_contacts_quxinli_0396(self):
        GroupPage = GroupListPage()
     #   GroupPage.click_back_button(times=2)
        GroupPage.click_back_by_android(times=2)
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0397():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        #Preconditions.make_already_in_message_page()
        Preconditions.background_app()
        time.sleep(5)


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0397(self):
        """“分组详情操作”界面-多方电话"""
        GroupPage = GroupListPage()
        cdp=ContactDetailsPage()
        preconditions.launch_app()
        time.sleep(1)
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        GroupPage.add_member(name='dalao6')
        time.sleep(2)
        GroupPage.add_member(name='dalao7')
        time.sleep(1)
        GroupPage.enter_mutil_call()
        time.sleep(1)
        GroupPage.click_text("大佬6")
        time.sleep(2)
        cdp.send_call_number()
        cdp.cancel_permission()
        cdp.cancel_call()

    def tearDown_test_contacts_quxinli_0397(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0398():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.background_app()
        time.sleep(5)
        #Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0398(self):
        """“分组详情操作”界面-多方视频"""
        GroupPage = GroupListPage()
        cdp = ContactDetailsPage()
        preconditions.launch_app()
        time.sleep(2)
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        GroupPage.add_member(name='dalao7')
        time.sleep(1)
        GroupPage.enter_mutil_video_call()
        time.sleep(1)
        GroupPage.click_text("大佬7")
        time.sleep(2)
        cdp.send_call_number()
        cdp.cancel_permission()
        cdp.end_video_call()

    def tearDown_test_contacts_quxinli_0398(self):
        GroupPage = GroupListPage()
        time.sleep(1)
        SelectOneGroupPage().click_back_by_android()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0407():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0407(self):
        """“分组设置-特殊符号标签名称
        auther:严顺华
        """
        GroupPage = GroupListPage()
        cdp = ContactDetailsPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='*@!#')
        GroupPage.click_back_button(times=2)
        GroupPage.page_should_contain_text(text='*@!#')

    def tearDown_test_contacts_quxinli_0407(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='*@!#')

    @staticmethod
    def setUp_test_contacts_quxinli_0408():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0408(self):
        """“分组设置-各种标签名称
        auther:严顺华
        """
        GroupPage = GroupListPage()
        cdp = ContactDetailsPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='*@!#123好')
        GroupPage.click_back_button(times=2)
        GroupPage.page_should_contain_text(text='*@!#123好')

    def tearDown_test_contacts_quxinli_0408(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='*@!#123好')

    @staticmethod
    def setUp_test_contacts_quxinli_0409():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0409(self):
        """“分组设置-各种标签名称删除
        auther:严顺华
        """
        GroupPage = GroupListPage()
        cdp = ContactDetailsPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.delete_label_name(name='*@!#123好')
        GroupPage.page_should_contain_text(text="请输入标签分组名称")
        GroupPage.click_back_button(times=3)

    def tearDown_test_contacts_quxinli_0409(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='*@!#123好')

    @staticmethod
    def setUp_test_contacts_quxinli_0414():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0414(self):
        """分组设置-搜索移除成员
        auther:严顺华
        """
        GroupPage = GroupListPage()
        cdp = ContactDetailsPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.tap_sure_box()
        GroupPage.add_member(name='dalao7')
        time.sleep(2)
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        GroupPage.click_settings_button()
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.search_menber_text(text='dalao7')
        time.sleep(1)
        GroupPage.click_text('大佬7')
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.page_should_not_contain_text("大佬7")

    def tearDown_test_contacts_quxinli_0414(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=3)
        GroupPage.delete_group(name='aaa')


    @staticmethod
    def setUp_test_contacts_quxinli_0415():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0415(self):
        """分组设置-删除标签
        auther:严顺华
        """
        GroupPage = GroupListPage()
        cdp = ContactDetailsPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.new_group(name='ccc')
        GroupPage.delete_group(name='ccc')
        GroupPage.click_back_by_android(times=2)


    @staticmethod
    def setUp_test_contacts_quxinli_0416():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
      #  Preconditions.make_already_in_message_page()
        Preconditions.background_app()
        time.sleep(3)


    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0416(self):
        """分组详情操作页面进入Profile页"""
        GroupPage = GroupListPage()
        preconditions.launch_app()
        time.sleep(2)
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        GroupPage.add_member(name='dalao2')
        time.sleep(2)
        GroupPage.add_member(name='dalao3')
        time.sleep(1)
        GroupPage.click_send_message_to_group()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬3")
        time.sleep(1)
        GroupPage.page_contain_element(locator='语音通话')
        GroupPage.page_contain_element(locator='视频通话')
        GroupPage.page_contain_element(locator='分享名片')
        GroupPage.click_share_button()
        time.sleep(1)
        SelectContactsPage().click_select_one_group()
        time.sleep(1)
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('给个红包1')
        SelectOneGroupPage().select_one_group_by_name('给个红包1')
        SelectOneGroupPage().click_share_business_card()
        time.sleep(2)
        GroupPage.click_innvation_button()

    def tearDown_test_contacts_quxinli_0416(self):
        GroupPage = GroupListPage()

        GroupPage.background_app(seconds=10)
        time.sleep(10)
        preconditions.launch_app()
        time.sleep(1)
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0417():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
       # Preconditions.make_already_in_message_page()
        Preconditions.background_app()
        time.sleep(5)

    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0417(self):
        """分组详情操作页面进入Profile页_星标
        auther:严顺华"""
        GroupPage = GroupListPage()
        preconditions.launch_app()
        time.sleep(2)
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        GroupPage.add_member(name='dalao2')
        time.sleep(2)
        GroupPage.add_member(name='dalao3')
        time.sleep(1)
        GroupPage.enter_group_message()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬3")
        time.sleep(1)
        GroupPage.click_star_icon()
        GroupPage.is_toast_exist("已成功添加为星标联系人")
        time.sleep(1)
        GroupPage.click_star_icon()
        GroupPage.is_toast_exist("已取消添加为星标联系人")
        GroupPage.click_star_icon()
       # GroupPage.click_back_button(times=3)
        GroupPage.click_back_by_android(times=3)
        time.sleep(2)
       # GroupPage.click_back_button(times=2)
        GroupPage.click_back_by_android(times=2)

        time.sleep(1)
        GroupPage.page_contain_element(locator='星标')

    def tearDown_test_contacts_quxinli_0417(self):
        GroupPage = GroupListPage()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')


    @staticmethod
    def setUp_test_contacts_quxinli_0421():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0421(self):
        """安卓手机：手机系统本地新建分组名称超过30个字符的分组
        auther:严顺华"""
        GroupPage = GroupListPage()
        GroupPage.open_contacts_page()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        name="a"*30
        GroupPage.new_group(name=name)
        GroupPage.click_text(name)
        time.sleep(1)
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='aaa')
        GroupPage.click_back_button(times=2)
        time.sleep(1)
        GroupPage.page_should_contain_text(text='aaa')
        GroupPage.click_text("aaa")
        time.sleep(1)
        GroupPage.tap_sure_box()
        time.sleep(1)
        GroupPage.add_member(name='dalao2')
        time.sleep(2)
        GroupPage.add_member(name='dalao3')
        time.sleep(1)
        GroupPage.click_settings_button()
        time.sleep(1)
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.click_text('大佬2')
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.page_should_not_contain_text("大佬2")


    def tearDown_test_contacts_quxinli_0421(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=3)
        time.sleep(1)
        GroupPage.delete_group(name='aaa')

if __name__ == '__main__':
    unittest.main()
