import settings


# class ConfigStored:
#     server_url = settings.APPIUM_SETTING["REMOTE_URL"]
#     desired_caps = settings.DEFAULT_DESIRED_CAPABILITY


# def set_desired_caps(caps):
#     ConfigStored.desired_caps = caps


# def get_desired_caps():
#     return ConfigStored.desired_caps


# def set_server_url(url):
#     ConfigStored.server_url = url


# def get_server_url():
#     return ConfigStored.server_url


def get_project_path():
    return settings.PROJECT_PATH


def get_html_report_path():
    return settings.REPORT_HTML_PATH


def get_test_case_root():
    return settings.TEST_CASE_ROOT


def get_screen_shot_path():
    return settings.SCREEN_SHOT_PATH
