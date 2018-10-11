from appium.webdriver.common.mobileby import MobileBy

# 通知栏
p_notification_m_message_e_verification_code = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("登录验证")')

# 公共模块
p_all_page_m_dialog_e_ok = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/btn_ok")')

# 引导页
p_welcome_m_main_e_start_to_use = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/splash_btn_thrid")')
# 权限列表页面
p_permission_list_m_list_e_submit = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/tv_submit")')
# 授权页面
p_permission_grant_m_dialog_e_dialog_box = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.packageinstaller:id/dialog_container")')
p_permission_grant_m_dialog_e_reject = (
    MobileBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.android.packageinstaller:id/permission_deny_button")')
p_permission_grant_m_dialog_e_allow = (
    MobileBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.android.packageinstaller:id/permission_allow_button")')
p_permission_grant_m_dialog_e_dialog_footer = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.packageinstaller:id/current_page_text")')

# 登录页
p_login_m_one_key_e_phone_number = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/tv_content")')
p_login_m_one_key_e_one_key_login = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/one_key_login")')
p_login_m_form_e_use_another_number_to_login = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/change_to_smslogin")')
p_sms_login_m_form_e_phone_number = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/edt_phone_number")')

p_sms_login_m_form_e_verification_code = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/edt_verify_sms")')
p_sms_login_m_form_e_get_verification_code = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/get_sms")')
p_sms_login_m_form_e_login = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/btnLogin")')

p_sms_login_m_dialog_e_i_know = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/btn_know")')

# Home-页脚
p_home_m_footer_e_message = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/tvMessage")')  # 消息
p_home_m_footer_e_call = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/tvCall")')  # 通话
p_home_m_footer_e_workbench = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/tvCircle")')  # 工作台
p_home_m_footer_e_address_book = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/tvContact")')  # 通讯录
p_home_m_footer_e_me = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/tvMe")')  # 我

# 主页 - 消息
p_message_m_top_e_add_button = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/action_add")')  # 加号
p_message_m_add_menu_e_new_message = (
    MobileBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.chinasofti.rcs:id/pop_navi_text").instance(0)')  # 新建消息
p_message_m_add_menu_e_free_sms = (
    MobileBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.chinasofti.rcs:id/pop_navi_text").instance(1)')  # 免费短信
p_message_m_add_menu_e_initiate_group_chat = (
    MobileBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.chinasofti.rcs:id/pop_navi_text").instance(2)')  # 发起群聊
p_message_m_add_menu_e_grouping_mass_message = (
    MobileBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.chinasofti.rcs:id/pop_navi_text").instance(3)')  # 分组群发
p_message_m_add_menu_e_take_a_scan = (
    MobileBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.chinasofti.rcs:id/pop_navi_text").instance(4)')  # 扫一扫

# 主页 - 我
p_home_m_me_e_setting = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/setting_app_text")')  # 设置

# 设置 - 首页
p_home_m_setting_home_e_quit = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/login_out_text")')  # 退出

# DEMO
p_demo_m_module_e_element = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resouceId("elementid")')


class SelectContactPage:
    """
    选择联系人
    """
    p_select_contact_m_search_e_search_box = (
        MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/contact_search_bar")')  # 搜索框

    p_select_contact_m_contact_list_e_contact = (
        MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/contact_list_item")')  # 联系人

    p_select_contact_m_contact_list_e_contact_name = (
        MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/contact_name")')  # 联系人- 姓名
    p_select_contact_m_contact_list_e_contact_number = (
        MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/contact_name")'  # 联系人 - 号码
    )


class MessageDetailPage:
    p_message_detail_m_dialog_e_is_read = (
        MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/btn_check")'
    )

    p_message_detail_m_dialog_e_ok_button = (
        MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/dialog_btn_ok")'
    )

    p_message_m_bottom_e_message_input_box = (
        MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/et_message")')

    p_message_detail_m_bottom_e_send_message_button = (
        MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.chinasofti.rcs:id/ib_send")')  # 发送
