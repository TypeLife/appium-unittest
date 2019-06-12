import time
from appium.webdriver.common.mobileby import MobileBy
from library.core.utils.applicationcache import current_mobile
from pages.components import ContactsSelector
from preconditions.BasePreconditions import LoginPreconditions, ContactsPage, CallPage, ContactSecltorPage, \
    SelectContactsPage, CalllogBannerPage, MessagePage, SearchPage, LabelGroupingPage, GroupListPage, \
    GroupListSearchPage, LableGroupDetailPage
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from preconditions.BasePreconditions import LoginPreconditions, ContactsPage, CallPage, \
     CalllogBannerPage, ContactListSearchPage, CallContactDetailPage, SingleChatPage, ContactDetailsPage\
     , CallTypeSelectPage


class Preconditions(LoginPreconditions):
    """前置条件"""
    # contacts_name_1 = LoginPreconditions.get_contacts_by_row_linename(0, 'contacts_name')
    # telephone_num_1 = LoginPreconditions.get_contacts_by_row_linename(0, 'telephone_num')
    # contacts_name_2 = LoginPreconditions.get_contacts_by_row_linename(1, 'contacts_name')
    # telephone_num_2 = LoginPreconditions.get_contacts_by_row_linename(1, 'telephone_num')

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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0146(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人1', '18312345678')
        contactspage.create_contacts_if_not_exits('联系人2', '18323456789')
        contactspage.create_contacts_if_not_exits('联系人3', '13812345678')
        contactspage.create_contacts_if_not_exits('联系人4', '13823456789')
        contactspage.create_contacts_if_not_exits('联系人5', '13811111111')
        contactspage.create_contacts_if_not_exits('联系人6', '13822222222')
        contactspage.create_contacts_if_not_exits('联系人7', '13833333333')
        contactspage.create_contacts_if_not_exits('联系人8', '13844444444')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('联系人1')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人1"]'))
        selectcontacts.search('联系人2')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人2"]'))
        selectcontacts.search('联系人3')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人3"]'))
        selectcontacts.search('联系人4')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人4"]'))
        selectcontacts.search('联系人5')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人5"]'))
        selectcontacts.search('联系人6')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人6"]'))
        selectcontacts.search('联系人7')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人7"]'))
        selectcontacts.search('联系人8')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人8"]'))
        time.sleep(5)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
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
        time.sleep(3)
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallTime" and ' +
                                       '@text="刚刚"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0147(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人1', '18312345678')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        time.sleep(4)
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('联系人1')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人1"]'))
        selectcontacts.search('18311111111')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18322222222')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18333333333')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18333333333')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18344444444')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18355555555')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18366666666')
        selectcontacts.click_unknown_member()

        time.sleep(5)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
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
        time.sleep(4)
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallTime" and ' +
                                       '@text="刚刚"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

    @staticmethod
    def setUp_test_call_wangqiong_0155():
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
        # 进入群聊分组页签
        contactspage.open_group_chat_list()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0155(self):
        # 创建标签分组
        grouppage = GroupListPage()
        # 创建群聊1
        grouppage.create_group_chats_if_not_exits('群聊1', ["联系人3", "联系人4"])
        # 进入群聊的多方电话
        grouppage.click_group('群聊1')
        grouppage.click_mult_call_icon()
        time.sleep(3)
        grouppage.click_element((MobileBy.XPATH, "//*[@text='多方电话']"))

        # 选择成员进行多方电话

        time.sleep(10)

    @staticmethod
    def setUp_test_call_wangqiong_0157():
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
        # 进入群聊分组页签
        contactspage.open_group_chat_list()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0157(self):
        # 创建标签分组
        grouppage = GroupListPage()
        # 创建群聊1
        grouppage.create_group_chats_if_not_exits('群聊1', ["联系人3", "联系人4"])
        # 进入群聊的多方电话
        grouppage.click_search_input()
        groupserch = GroupListSearchPage()
        groupserch.input_search_keyword('群聊1')
        # 点击群聊1
        groupserch.click_group('群聊1')
        grouppage.click_mult_call_icon()
        time.sleep(3)
        grouppage.click_element((MobileBy.XPATH, "//*[@text='多方电话']"))

        contactselect = ContactsSelector()
        # 选择自己进行多方电话,弹框该联系人不可选择,呼叫按钮任然置灰
        contactselect.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/index_text'))
        current_mobile().assert_element_should_be_disabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

    @staticmethod
    def setUp_test_call_wangqiong_0171():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        # contactspage.create_contacts_if_not_exits('A联系人', '18311111111')
        # contactspage.create_contacts_if_not_exits('B联系人', '18322222222')
        # contactspage.create_contacts_if_not_exits('C联系人', '18333333333')
        # contactspage.create_contacts_if_not_exits('D联系人', '18344444444')
        # contactspage.create_contacts_if_not_exits('E联系人', '18355555555')
        # contactspage.create_contacts_if_not_exits('F联系人', '18366666666')
        # contactspage.create_contacts_if_not_exits('G联系人', '18377777777')
        # contactspage.create_contacts_if_not_exits('H联系人', '18388888888')
        # contactspage.create_contacts_if_not_exits('I联系人', '18399999999')
        # contactspage.create_contacts_if_not_exits('J联系人', '13822222222')
        # contactspage.create_contacts_if_not_exits('K联系人', '13811111111')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0171(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组A')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组A')

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

        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.create_group('分组A', ["A联系人", "B联系人", "C联系人"])
        # labellist.create_group('分组A', ['A联系人', 'B联系人', 'C联系人', 'D联系人', 'E联系人', 'F联系人', 'G联系人', 'H联系人', 'I联系人', 'J联系人', 'K联系人'])
        labellist.click_label_group('分组A')
        # 进入多方通话
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))
        # 查看时长
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs: id/multi_time_tip'))
        self.assertTrue(labellist.is_text_present((MobileBy.XPATH, '//*[contains(@text, "分钟")]')))

        # 按照字母滑动
        contact = ContactsPage()
        contact.click_element(
            ('xpath', '//*[@resource-id="com.chinasofti.rcs:id/indexbarview"]'))
        elements = contact.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'))
        for i in range(len(elements)):
            elements[i].click()
        # 判断右侧字符是否按顺序排列
        current_mobile().is_right_letters_sorted()

    @staticmethod
    def setUp_test_call_wangqiong_0179():
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
    def test_call_wangqiong_0179(self):
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
            # 新建分组 选择分组成员
            labellist.click_one_contact('联系人3')
            labellist.click_one_contact('联系人4')
            labellist.click_sure()
            labellist.select_group('分组1')
        # 点击多方电话
        labeldeatilpage = LableGroupDetailPage()
        labeldeatilpage.click_multi_tel()

        # 通过11位号码选择联系人 看是否能精准匹配到联系人
        from pages import SelectLocalContactsPage

        selectpage = SelectLocalContactsPage()
        selectpage.search('18311111111')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "联系人3")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0180():
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
    def test_call_wangqiong_0180(self):
        # 创建标签分组
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '联系人3', '联系人4')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('联系人3')
        b = labelpage.is_contacter_in_lable('联系人4')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                labelpage.click_one_contact('联系人3')
            if not b:
                labelpage.click_one_contact('联系人4')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入1位数 查看是否能模糊匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('1')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "联系人3")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0181():
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
    def test_call_wangqiong_0181(self):
        # 创建标签分组
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '联系人3', '联系人4')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('联系人3')
        b = labelpage.is_contacter_in_lable('联系人4')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                labelpage.click_one_contact('联系人3')
            if not b:
                labelpage.click_one_contact('联系人4')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入全名 查看是否能精准匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('联系人3')
        time.sleep(3)
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0182():
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
    def test_call_wangqiong_0182(self):
        # 创建标签分组
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '联系人3', '联系人4')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('联系人3')
        b = labelpage.is_contacter_in_lable('联系人4')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                labelpage.click_one_contact('联系人3')
            if not b:
                labelpage.click_one_contact('联系人4')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入非全名 查看是否能模糊匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('联系人')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "联系人3")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0193():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0193(self):
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
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_element((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall"))
        # 选择指定联系人 点击呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('联系人3')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]'))
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
            callcontact.get_source()
        if not callcontact._is_element_present((MobileBy.XPATH, "//*[contains(@text, '我')]")):
            callcontact.click_element((MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button'), 1,
                                      False)

        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(6)
        callpage = CallPage()
        callpage.hang_up_hefeixin_call()
        time.sleep(3)
        #
        # 挂断电话回到多方通话界面
        self.assertTrue(callcontact._is_element_present((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall")))

    @staticmethod
    def setUp_test_call_wangqiong_0033():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0033(self):
        """本网用户各和飞信电话入口，可成功发起呼叫"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        # 1.在通讯录（群聊、单聊/标签分组）profile页，点击：和飞信电话（免费），发起呼叫（呼叫成功后挂断）
        contactspage.click_search_box()
        contact = ContactListSearchPage()
        contact.input_search_keyword(contactname1)
        contact.click_contact(contactname1)
        # 点击和飞信电话,呼叫成功后挂断
        callcontactdetail = CallContactDetailPage()
        callcontactdetail.call_fetion_call()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 挂断和飞信电话
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()
        time.sleep(2)
        # 2.在通讯录（群聊、单聊/标签分组）profile页，进入消息页面发起和飞信电话
        callcontactdetail.click_normal_message()
        # 存在用户须知？ 存在则同意
        time.sleep(2)
        from pages.components import ChatNoticeDialog
        chatnotice = ChatNoticeDialog()
        if chatnotice.is_exist_tips():
            chatnotice.accept_and_close_tips_alert()
        singlechat = SingleChatPage()
        time.sleep(2)
        singlechat.click_action_call()
        singlechat.click_hefeixinfree_call_631()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 挂断和飞信电话
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()
        time.sleep(2)
        # 返回到联系页面
        singlechat.click_back()
        contactdetail = ContactDetailsPage()
        contactdetail.click_back_icon()
        # 返回到联系人页面
        contact.click_back()
        time.sleep(2)

        # 3.进入通话页签 输入数字进行拨打和飞信电话
        Preconditions.enter_call_page()

        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击拨号键，输入号码并拨打,选择'和飞信电话（免费）'
        callpage.click_call()
        callpage.dial_number('18311111111')
        time.sleep(2)
        callpage.click_call_phone()
        calltype = CallTypeSelectPage()
        calltype.click_call_by_app_631()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 挂断和飞信电话
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()
        time.sleep(2)
        callpage.click_call()

        # Checkpoint：拨打的通话记录为飞信通话 进入通话详情页，标题为飞信通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(5)
        callpage.click_ganggang_call_time()
        # 查看详情页面是否是飞信电话？
        time.sleep(5)
        callpage.is_hefeixin_page('飞信电话')

    @staticmethod
    def setUp_test_call_wangqiong_0172():
        """标签分组-多方电话选择器-支持组员名称号码搜索"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        contactname3 = Preconditions.contacts_name_3
        contactnum3 = Preconditions.telephone_num_3
        contactname4 = Preconditions.contacts_name_4
        contactnum4 = Preconditions.telephone_num_4
        contactname5 = Preconditions.contacts_name_5
        contactnum5 = Preconditions.telephone_num_5
        contactname6 = Preconditions.contacts_name_6
        contactnum6 = Preconditions.telephone_num_6
        contactname7 = Preconditions.contacts_name_7
        contactnum7 = Preconditions.telephone_num_7
        contactname8 = Preconditions.contacts_name_8
        contactnum8 = Preconditions.telephone_num_8
        contactname9 = Preconditions.contacts_name_9
        contactnum9 = Preconditions.telephone_num_9
        contactname10 = Preconditions.contacts_name_10
        contactnum10 = Preconditions.telephone_num_10
        contactname11 = Preconditions.contacts_name_11
        contactnum11 = Preconditions.telephone_num_11
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        contactspage.create_contacts_if_not_exits_631(contactname3, contactnum3)
        contactspage.create_contacts_if_not_exits_631(contactname4, contactnum4)
        contactspage.create_contacts_if_not_exits_631(contactname5, contactnum5)
        contactspage.create_contacts_if_not_exits_631(contactname6, contactnum6)
        contactspage.create_contacts_if_not_exits_631(contactname7, contactnum7)
        contactspage.create_contacts_if_not_exits_631(contactname8, contactnum8)
        contactspage.create_contacts_if_not_exits_631(contactname9, contactnum9)
        contactspage.create_contacts_if_not_exits_631(contactname10, contactnum10)
        contactspage.create_contacts_if_not_exits_631(contactname11, contactnum11)
        # 进入标签分组页签
        contactspage.click_label_grouping_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0172(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        # 存在老的分组 则删除
        labellist.delete_label_groups('分组A')
        time.sleep(2)
        labellist.create_group('分组A', Preconditions.contacts_name_1, Preconditions.contacts_name_2,
                               Preconditions.contacts_name_3, Preconditions.contacts_name_4, Preconditions.contacts_name_5,
                               Preconditions.contacts_name_6, Preconditions.contacts_name_7, Preconditions.contacts_name_8,
                               Preconditions.contacts_name_9, Preconditions.contacts_name_10, Preconditions.contacts_name_11)
        labellist.click_label_group('分组A')
        # 选择成员进行多方通话
        labellist.click_third_image_call()
        # CheckPoint： 选择成员成功发起呼叫
        labellist.select_local_contacts(Preconditions.contacts_name_1, Preconditions.contacts_name_2)
        # 存在悬浮权限提醒，暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 挂断多方通话
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_call_wangqiong_0194():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0194(self):
        """多方电话联系人选择器支持搜索正确陌生内地固号"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        # callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 点击搜索框搜索联系人 查看搜索结果，点击呼叫
        contactselect = SelectContactsPage()
        contactselect.search('+860206631888')
        # checkpoint： 查看+860206631888 匹配结果，没有匹配结果
        contactselect.page_should_not_contain_text('未知号码')
        # 清空搜索栏
        contactselect.clear_serchbar_keyword()
        # checkpoint： 搜索0206631885 查看匹配结果“未知号码”、并点击呼叫
        contactselect.search('0206631885')
        contactselect.is_present_unknown_member()
        contactselect.click_unknown_member()
        # 呼叫
        time.sleep(2)
        contactselect.click_sure_bottom()
        # 是否存在‘我知道了’ ，点击
        time.sleep(2)
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()

        # checkpoint: 可以正常可以挂断飞信电话
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_call_wangqiong_0204():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0204(self):
        """网络信号正常，发起多方电话流程正常"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        contactname3 = Preconditions.contacts_name_3
        contactnum3 = Preconditions.telephone_num_3
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        contactspage.create_contacts_if_not_exits_631(contactname3, contactnum3)

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1, contactname2, contactname3)
        #  调试用，可删除
        # contactselect.select_local_contacts(contactname1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # Checkpoint：当前页面是否是系统通话页面 如果是返回到主界面
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 进入手机home页
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(2)
        # 点击进入通话会控页，未接听前，联系人状态为呼叫中
        callpage.click_back_to_call_631()
        time.sleep(2)
        # 当前页面呼叫人状态为‘呼叫中’
        multipage = MultipartyCallPage()
        multipage.assert_caller_status_is_display()
        # 挂断和飞信
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_call_wangqiong_0210():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0210(self):
        """多方电话呼叫中---网络正常下，会控界面显示正常"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        contactname3 = Preconditions.contacts_name_3
        contactnum3 = Preconditions.telephone_num_3
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        contactspage.create_contacts_if_not_exits_631(contactname3, contactnum3)
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1, contactname2, contactname3)
        # 调试用，可删除
        # contactselect.select_local_contacts(contactname1)

        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 进入手机home页
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(2)
        # 点击进入通话会控页，未接听前，联系人状态为呼叫中
        callpage.click_back_to_call_631()
        time.sleep(1)
        # Checkpoint：1.当前页面呼叫人状态为‘呼叫中’
        multipage = MultipartyCallPage()
        multipage.assert_caller_status_is_display()
        # Checkpoint：2.右上角存在隐藏符号
        multipage.assert_hide_icon_is_display()
        # Checkpoint：3.+号展示最多9人
        multipage.assert_caller_max_count_is_display()
        # Checkpoint：4.展示我（主叫）
        multipage.assert_caller_me_is_display()
        time.sleep(1)
        # 挂断和飞信
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_call_wangqiong_0211():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0211(self):
        """多方电话呼叫中时--网络正常下，会控界面点击顶部可返回至系统通话页"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        contactname3 = Preconditions.contacts_name_3
        contactnum3 = Preconditions.telephone_num_3
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        contactspage.create_contacts_if_not_exits_631(contactname3, contactnum3)
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1, contactname2, contactname3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # Checkpoint：当前页面是否是系统通话页面 如果是返回手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 进入手机home页
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(2)
        # 点击进入通话会控页，未接听前，联系人状态为呼叫中
        callpage.click_back_to_call_631()
        time.sleep(1)
        # 当前页面呼叫人状态为‘呼叫中’
        multipage = MultipartyCallPage()
        multipage.assert_caller_status_is_display()
        # 挂断和飞信
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_call_wangqiong_0262():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0262(self):
        """会控界面：“未接听”状态的成员，可支持重新拨号、移除成员、取消成功"""
        """前置条件：保证contactnum1为真实号码 ，contactnum2为非真实现网手机"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631('联系人2', '18311111111')

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search(contactname1)
        selectcontacts.click_contact_by_name(contactname1)
        selectcontacts.search('联系人2')
        selectcontacts.click_contact_by_name('联系人2')
        time.sleep(2)
        selectcontacts.click_sure_bottom()
        time.sleep(2)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 判断当前是否在系统通话界面,是的话进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 进入手机home页
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(2)
        # 点击进入通话会控页，
        callpage.click_back_to_call_631()
        time.sleep(2)
        # checkpoint1：点击未接通 展示页面含有未接通
        multipage = MultipartyCallPage()
        multipage.click_not_access()
        multipage.page_should_contain_text('联系人2 未接通')
        # checkpoint2: 点击取消,回收弹框
        multipage.click_cancel()
        multipage.page_should_not_contain_text('联系人2 未接通')
        # checkpoint3: 再次点击未接通,点击重新呼叫，回到会控页面，且联系人2状态变为呼叫中
        multipage.click_not_access()
        multipage.click_call_again()

        # checkpoint3: 点击取消
        multipage.click_not_access()
        multipage.click_cancel()

    @staticmethod
    def setUp_test_call_wangqiong_0266():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0266(self):
        """发起多方电话呼叫邀请中，可点击会控界面挂断按钮，结束多方电话通话"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search(contactname1)
        selectcontacts.click_contact_by_name(contactname1)
        selectcontacts.search(contactname2)
        selectcontacts.click_contact_by_name(contactname2)
        time.sleep(2)
        selectcontacts.click_sure_bottom()
        time.sleep(2)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 判断当前是否在系统通话界面,是的话进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 进入手机home页
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(2)
        # 点击进入通话会控页，
        callpage.click_back_to_call_631()
        time.sleep(2)
        # checkpoint1：会控页面飞信电话挂断，系统电话也挂断
        callpage.hang_up_hefeixin_call_631()
        time.sleep(6)
        message = MessagePage()
        self.assertTrue(message.is_on_this_page())

    @staticmethod
    def setUp_test_call_wangqiong_0267():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0267(self):
        """发起多方电话呼叫邀请中，可点击系统电话挂断，结束多方电话通话"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击飞信电话图标
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # Checkpoint：当前页面是否是系统通话页面 如果是挂断，多方通话一起挂断，返回到通话页签
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 挂断之后回到通话页面
        time.sleep(2)
        callpage.hang_up_the_call()
        time.sleep(5)
        self.assertTrue(callpage.is_on_the_call_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0288(self):
        """多人的多方电话--通话记录详情页各信息显示正常。"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1, contactname2)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

        # Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信电话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是多方电话？
        callpage.is_hefeixin_page('飞信电话')
        time.sleep(3)
        # Checkpoint：详情页是否有‘再次呼叫’、‘一键建群’
        self.assertTrue(callpage.page_should_contain_text('再次呼叫'))
        self.assertTrue(callpage.page_should_contain_text('一键建群'))

    @staticmethod
    def setUp_test_call_wangqiong_0289():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0289(self):
        """发起1人的多方电话--通话记录详情页各信息显示正常。"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击飞信电话图标
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

        # Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信电话通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是和飞信电话？
        callpage.is_hefeixin_page('飞信电话')
        time.sleep(3)
        # Checkpoint：详情页是否有‘再次呼叫’
        self.assertTrue(callpage.page_should_contain_text('再次呼叫'))

    @staticmethod
    def setUp_test_call_wangqiong_0291():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0291(self):
        """多方通话记录详情页--再次呼叫，网络正常重新呼叫多方电话"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        contactname2 = Preconditions.contacts_name_2
        contactnum2 = Preconditions.telephone_num_2
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击飞信电话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1, contactname2)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

        # Checkpoint：拨打的通话记录为多方电话 进入通话详情页，标题为多方电话通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是多方电话？
        callpage.is_hefeixin_page('飞信电话')

        # 点击‘再次呼叫’
        callpage.click_mutil_call_again()
        suspend.ignore_tips_if_tips_display()
        # Checkpoint：当前是否是和飞信通话会控页
        time.sleep(2)
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_call_wangqiong_0292():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0292(self):
        """发起1人的多方电话--再次呼叫，网络正常重新呼叫和飞信电话"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts(contactname1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

        # Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        callpage.is_hefeixin_page('飞信电话')

        # 点击‘再次呼叫’
        callpage.click_mutil_call_again()
        suspend.ignore_tips_if_tips_display()
        # Checkpoint：当前是否是和飞信通话会控页
        time.sleep(2)
        callpage.hang_up_hefeixin_call_631()



