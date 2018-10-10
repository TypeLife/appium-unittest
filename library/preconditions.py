from library import config, keywords


class Preconditions(object):
    @staticmethod
    def open_and_login_app_using_on_key_login():
        # 打开app
        desired_caps = config.GlobalConfig.get_desired_caps()
        url = config.GlobalConfig.get_server_url()
        keywords.Android.open_app(url, desired_caps)

        keywords.GuidePage.jump_over_the_guide_page()
        keywords.PermissionListPage.accept_all_permission_in_list()
        keywords.Login.wait_for_one_key_login_page_load()
        # 登录
        keywords.Login.click_one_key_login()
        keywords.MessagePage.wait_for_message_page_load()
