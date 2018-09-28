from appium.webdriver.common.mobileby import MobileBy

p_welcome_m_main_e_start_to_use = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageButton")')
p_login_m_form_e_account = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").index(0)')
p_login_m_form_e_password = (
    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").index(1)')

# 权限列表页面
p_permission_list_m_list_e_submit = (MobileBy.ID, 'com.chinasofti.rcs:id/tv_submit')
# 授权页面
p_permission_grant_m_dialog_e_dialog_box = (MobileBy.ID, 'com.android.packageinstaller:id/dialog_container')
p_permission_grant_m_dialog_e_reject = (MobileBy.ID, 'com.android.packageinstaller:id/permission_deny_button')
p_permission_grant_m_dialog_e_allow = (MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button')
p_permission_grant_m_dialog_e_dialog_footer = (MobileBy.ID, 'com.android.packageinstaller:id/current_page_text')
