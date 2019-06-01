import time
from appium.webdriver.common.mobileby import MobileBy
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions, ContactsPage, CallPage, ContactSecltorPage, \
    SelectContactsPage, CalllogBannerPage, MessagePage, SearchPage, LabelGroupingPage
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags


class Preconditions(LoginPreconditions):
    """前置条件"""


class MsgAllPrior(TestCase):

    @staticmethod
    def setUp_test_call_wangqiong_0057():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0057(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.click_one_contact('联系人3')
        selectcontacts.click_one_contact('联系人4')
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))
        time.sleep(3)
        # 接听和飞信电话  为自动接听
        callcontact._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(6)
        callcontact.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0059(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.click_one_contact('联系人3')
        selectcontacts.click_one_contact('联系人4')
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))
        time.sleep(5)
        # 接听和飞信电话  为自动接听
        callcontact._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(3)
        callcontact.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(4)
        # 挂断电话返回到通话页面
        self.assertTrue(callcontact._is_element_present((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall")))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0063(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.click_one_contact('联系人3')
        selectcontacts.click_one_contact('联系人4')
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 点击多方通话详情
        call_page.click_element((MobileBy.XPATH,
                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.view.ViewGroup/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.LinearLayout[2]'),
                                auto_accept_permission_alert=False)

        time.sleep(3)
        # 再次呼叫并接听和飞信电话
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/call_again'))
        time.sleep(5)
        # 挂断电话
        callcontact._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        callcontact.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(3)
        # 挂断电话回到多方通话界面
        self.assertTrue(callcontact._is_element_present((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall")))

    @staticmethod
    def setUp_test_call_wangqiong_0071():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0071(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组1')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组1')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('联系人3')
            b = labellist.is_contacter_in_lable('联系人4')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    labellist.click_one_contact('联系人3')
                if not b:
                    labellist.click_one_contact('联系人4')
                labellist.click_sure()
        else:
            labellist.click_one_contact('联系人3')
            labellist.click_one_contact('联系人4')
            labellist.click_sure()
            labellist.select_group('分组1')
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))
        labellist.click_one_contact('联系人3')
        labellist.click_one_contact('联系人4')
        time.sleep(3)
        labellist.click_sure()
        time.sleep(8)
        # 接听和飞信电话后挂断电话
        labellist._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        labellist.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @staticmethod
    def setUp_test_call_wangqiong_0073():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0073(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组1')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组1')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('联系人3')
            b = labellist.is_contacter_in_lable('联系人4')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    labellist.click_one_contact('联系人3')
                if not b:
                    labellist.click_one_contact('联系人4')
                labellist.click_sure()
        else:
            labellist.click_one_contact('联系人3')
            labellist.click_one_contact('联系人4')
            labellist.click_sure()
            labellist.select_group('分组1')
        # 进入群发消息界面并点击多方通话

        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_second_colum'),
                                auto_accept_permission_alert=False)
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_multicall'),
                                auto_accept_permission_alert=False)
        labellist.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and ' + '@text="多方电话"]'))
        time.sleep(3)
        labellist.click_one_contact('联系人3')
        labellist.click_one_contact('联系人4')
        time.sleep(3)
        labellist.click_sure()
        time.sleep(8)
        # 接听和飞信电话后挂断电话
        labellist._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        labellist.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @staticmethod
    def setUp_test_call_wangqiong_0080():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0080(self):
        # 通讯录界面搜索姓名
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("联系人3")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("联系人3")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '联系人3')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))

    @staticmethod
    def setUp_test_call_wangqiong_0081():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18351994357')
        contactspage.create_contacts_if_not_exits('联系人4', '18351994307')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0081(self):
        # 通讯录界面搜索姓名
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("联系人")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("联系人3")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '联系人')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))

    @staticmethod
    def setUp_test_call_wangqiong_0086():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0086(self):
        # 通讯录界面搜索姓名
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("18311111111")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("联系人3")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '18311111111')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))
        call_page.click_back()
        call_page.click_back()

        # 打开拨号键
        call_page.click_call()
        call_page.dial_number('18311111111')
        self.assertTrue(current_mobile().is_text_present('联系人3'))
        # 选择联系人正常展示
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' + '@text="联系人3"]'))

    @staticmethod
    def setUp_test_call_wangqiong_0087():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0087(self):
        # 通讯录界面搜索姓名
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(3)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '1')
        call_page.hide_keyboard()

        # 输入11位数字进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '18311111111')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))
        # 点击搜素到的结果
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]'))

        call_page.click_back()

        # 打开拨号键
        call_page.click_call()
        call_page.dial_number('18311111111')
        self.assertTrue(current_mobile().is_text_present('联系人3'))
        # 选择联系人正常展示
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' + '@text="联系人3"]'))

    @staticmethod
    def setUp_test_call_wangqiong_0088():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0088(self):
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(3)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '18312345678')
        call_page.hide_keyboard()

        # 校验是否搜索到未知号码
        SelectContactsPage().is_present_unknown_member()
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="18312345678(未知号码)"]'))
        time.sleep(3)
        call_page.click_back()

    @staticmethod
    def setUp_test_call_wangqiong_0119():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0119(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('联系人3')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @staticmethod
    def setUp_test_call_wangqiong_0120():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0120(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('联系人')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @staticmethod
    def setUp_test_call_wangqiong_0126():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0126(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('18311111111')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @staticmethod
    def setUp_test_call_wangqiong_0127():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0127(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        # 输入9位数 查看是否正匹配到数据
        contact_search.input_search_keyword('18311111')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0145(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.click_one_contact('联系人3')
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        time.sleep(4)
        callcontact = CalllogBannerPage()
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(2)
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' +
                                       '@text="联系人3"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

