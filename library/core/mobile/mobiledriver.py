import base64
import contextlib
import hashlib
import json
import re
from abc import *
from unicodedata import normalize

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException, TimeoutException, \
    NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from library.core.TestLogger import TestLogger


class MobileDriver(ABC):

    def __init__(self, alis_name, model_info, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None, keep_alive=False, card_slot=None):
        self._alis = alis_name
        self._model_info = model_info
        self._remote_url = command_executor
        self._desired_caps = self._init_capability(desired_capabilities)
        self._browser_profile = browser_profile
        self._proxy = proxy
        self._keep_alive = keep_alive
        self._card_slot = self._init_sim_card(card_slot)
        self._driver = None
        self.turn_off_reset()

    def __del__(self):
        if self.is_connection_created:
            self.driver.quit()

    @property
    def alis(self):
        return self._alis

    @property
    def model_info(self):
        return self._model_info

    def open_notifications(self):
        """打开通知栏"""
        if self.is_android():
            self.driver.open_notifications()
        else:
            # TODO IOS打开通知栏待实现
            pass

    def back(self):
        """返回"""
        self.driver.back()

    @property
    def driver(self):
        return self._driver

    @abstractmethod
    def total_card_slot(self):
        """卡槽数量，例如: 1、2"""
        raise NotImplementedError("This method must be implemented!")

    def _init_capability(self, caps):
        return caps

    def _init_sim_card(self, card_slot):
        """初始化手机SIM"""
        cards = []
        if not isinstance(card_slot, list):
            raise Exception('数据类型异常')
        for n in range(self.total_card_slot()):
            card = card_slot[n]
            if isinstance(card, dict):
                if card['TYPE'] in self.supported_card_types():
                    cards.append(card)
                else:
                    raise Exception('该手机不支持' + card_slot[n]['TYPE'] + '类型SIM卡（支持类型：{}）'
                                    .format(self.supported_card_types()))
        return cards

    def get_cards(self, card_type):
        """返回指定类型卡手机号列表"""
        return list([card['CARD_NUMBER'] for card in self._card_slot if card['TYPE'] == card_type])

    @abstractmethod
    def supported_card_types(self):
        """返回手机卡支持类型列表"""
        raise NotImplementedError("This method must be implemented!")

    @property
    def is_connection_created(self):
        if self.driver is None:
            return False
        else:
            try:
                t = self.driver.current_package
                return True
            except InvalidSessionIdException or WebDriverException:
                return False

    def connect_mobile(self):
        if self.driver is None:
            try:
                self._driver = webdriver.Remote(self._remote_url, self._desired_caps, self._browser_profile,
                                                self._proxy,
                                                self._keep_alive)
            except Exception as e:
                raise RuntimeError('无法连接到 appium server: {}'.format(self._remote_url))
        elif not self.is_connection_created:
            try:
                self.driver.start_session(self._desired_caps)
            except Exception as e:
                raise RuntimeError('无法连接到 appium server: {}'.format(self._remote_url))
        else:
            return

    def disconnect_mobile(self):
        if self.is_connection_created:
            self.driver.quit()

    def turn_on_reset(self):
        """开启重置app（在获取session之前有效）"""
        self._desired_caps['noReset'] = False

    def turn_off_reset(self):
        """关闭重置app（在获取session之前有效）"""
        self._desired_caps['noReset'] = True

    def is_platform(self, platform):
        if self.is_connection_created:
            platform_name = self.driver.desired_capabilities['platformName']
        else:
            platform_name = self._desired_caps['platformName']
        return platform.lower() == platform_name.lower()

    def is_ios(self):
        return self.is_platform('ios')

    def is_android(self):
        return self.is_platform('android')

    def launch_app(self):
        self.driver.launch_app()

    def terminate_app(self, app_id, **options):
        self.driver.terminate_app(app_id, **options)

    def background_app(self, seconds):
        self.driver.background_app(seconds)

    def activate_app(self, app_id):
        self.driver.activate_app(app_id)

    def reset_app(self):
        self.driver.reset()

    def press_home_key(self):
        """模拟手机HOME键"""
        if self.is_android():
            self.execute_shell_command('input', 'keyevent', 3)
        else:
            raise NotImplementedError('IOS 点击HOME键未实现')

    def execute_shell_command(self, command, *args):
        """
        Execute ADB shell commands (requires server flag --relaxed-security to be set)

        例：execute_shell_command('am', 'start', '-n', 'com.example.demo/com.example.test.MainActivity')

        :param command: 例：am,pm 等等可执行命令
        :param args: 例：am,pm 等可执行命令的参数
        :return:
        """
        script = {
            'command': command,
            'args': args
        }
        result = self.driver.execute_script('mobile:shell', script)
        print(result)
        return result

    @contextlib.contextmanager
    def listen_verification_code(self, max_wait_time=30):
        """监听验证码"""
        context = self._actions_before_send_get_code_request()
        code_container = []
        yield code_container
        code = self._actions_after_send_get_code_request(context, max_wait_time)
        if isinstance(code, list):
            code_container.append(code[0])
        elif isinstance(code, str):
            code_container.append(code)

    def _actions_before_send_get_code_request(self):
        """开始获取验证码之前的动作"""
        try:
            self.execute_shell_command('logcat', '-c')
        except Exception as e:
            print(e.__str__())

    def _actions_after_send_get_code_request(self, context, max_wait_time):
        """开始获取验证码之后的动作，结果为返回的验证码"""
        result = self.wait_until(
            condition=lambda d: re.findall(r'【登录验证】尊敬的用户：(\d+)',
                                           self.execute_shell_command('logcat', '-d', 'appium:D', 'MmsService:W', '*:S')
                                           ),
            timeout=max_wait_time
        )
        if result:
            return result[0]
        raise Exception("手机收不到验证码")

    def wait_until(self, condition, timeout=8, auto_accept_permission_alert=True):
        this = self

        def execute_condition(driver):
            """如果有弹窗，自动允许"""

            def get_accept_permission_handler(d):
                """获取允许权限弹窗的方法句柄"""
                try:
                    alert = d.switch_to.alert
                    return alert.accept
                except:
                    alert = this.get_elements((MobileBy.XPATH, '//android.widget.Button[@text="始终允许" or @text="允许"]'))
                    if not alert:
                        return False
                    return alert[0].click

            if auto_accept_permission_alert:
                if this.driver.current_activity in [
                    'com.android.packageinstaller.permission.ui.GrantPermissionsActivity',
                    '.permission.ui.GrantPermissionsActivity'
                ]:
                    need = True
                    while need:
                        try:
                            WebDriverWait(this.driver, 1).until(
                                get_accept_permission_handler
                            )()
                        except:
                            need = False
            return condition(driver)

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(execute_condition)

    def wait_condition_and_listen_unexpected(self, condition, timeout=8,
                                             auto_accept_permission_alert=True, unexpected=None, poll=0.2):
        this = self
        unexpect = unexpected

        def execute_condition(driver):
            """如果有弹窗，自动允许"""

            def get_accept_permission_handler(d):
                """获取允许权限弹窗的方法句柄"""
                try:
                    alert = d.switch_to.alert
                    return alert.accept
                except:
                    alert = this.get_elements((MobileBy.XPATH, '//android.widget.Button[@text="始终允许" or @text="允许"]'))
                    if not alert:
                        return False
                    return alert[0].click

            if auto_accept_permission_alert:
                if this.driver.current_activity in [
                    'com.android.packageinstaller.permission.ui.GrantPermissionsActivity',
                    '.permission.ui.GrantPermissionsActivity'
                ]:
                    need = True
                    while need:
                        try:
                            WebDriverWait(this.driver, 1).until(
                                get_accept_permission_handler
                            )()
                        except:
                            need = False

            if unexpected:
                if unexpected():
                    raise AssertionError("检查到页面报错")
            return condition(driver)

        wait = WebDriverWait(self.driver, timeout, poll)
        return wait.until(execute_condition)

    def _get_platform(self):
        try:
            platform_name = self.driver.desired_capabilities['platformName']
        except Exception as e:
            raise e
        return platform_name.lower()

    def _get_device_model(self):
        """获取设备型号"""
        platform = self._get_platform()
        if platform == 'android':
            model = self.execute_shell_command('getprop', 'ro.product.model')
            return model.strip()
        elif platform == 'ios':
            return 'ios'
        else:
            return 'other'

    def get_element(self, locator):
        return self.driver.find_element(*locator)

    def get_elements(self, locator):
        return self.driver.find_elements(*locator)

    def get_text(self, locator):
        """获取元素文本"""
        self.wait_until(
            condition=lambda d: self.get_elements(locator)
        )
        elements = self.get_elements(locator)
        if len(elements) > 0:
            return elements[0].text
        return None

    @TestLogger.log("获取控件属性")
    def get_element_attribute(self, locator, attr, wait_time=0):
        try:
            widget = self.wait_until(
                condition=lambda d: self.get_element(locator),
                timeout=wait_time
            )
            value = widget.get_attribute(attr)
            return value
        except TimeoutException:
            raise NoSuchElementException("找不到控件：{}".format(locator))

    def is_text_present(self, text):
        text_norm = normalize('NFD', text)
        source_norm = normalize('NFD', self.get_source())
        result = text_norm in source_norm
        return result

    def _is_element_present(self, locator):
        elements = self.get_elements(locator)
        return len(elements) > 0

    def _is_visible(self, locator):
        elements = self.get_elements(locator)
        if len(elements) > 0:
            return elements[0].is_displayed()
        return None

    def _is_clickable(self, locator):
        mapper = {
            'true': True,
            'false': False,
            'True': True,
            'False': False
        }
        element = self.get_element(locator)
        value = element.get_attribute('clickable')
        is_clickable = mapper[value.lower()]
        return is_clickable

    def _is_element_text_match(self, locator, pattern, full_match=True, regex=False):
        element = self.get_element(locator)
        actual = element.text
        if regex:
            if full_match:
                pt = re.compile(pattern)
                result = pt.fullmatch(actual)
            else:
                pt = re.compile(pattern)
                result = pt.search(actual)
        else:
            if full_match:
                result = pattern == actual
            else:
                result = pattern in actual
        if not result:
            return False
        return True

    def _is_enabled(self, locator):
        element = self.get_element(locator)
        return element.is_enabled()

    def get_source(self):
        return self.driver.page_source

    def click_element(self, locator, default_timeout=5):
        self.wait_until(
            condition=lambda d: self.get_element(locator),
            timeout=default_timeout
        ).click()
        # self.get_element(locator).click()

    def click_text(self, text, exact_match=False):
        if self._get_platform() == 'ios':
            if exact_match:
                _xpath = u'//*[@value="{}" or @label="{}"]'.format(text, text)
            else:
                _xpath = u'//*[contains(@label,"{}") or contains(@value, "{}")]'.format(text, text)
            self.get_element((MobileBy.XPATH, _xpath)).click()
        elif self._get_platform() == 'android':
            if exact_match:
                _xpath = u'//*[@{}="{}"]'.format('text', text)
            else:
                _xpath = u'//*[contains(@{},"{}")]'.format('text', text)
            self.get_element((MobileBy.XPATH, _xpath)).click()

    def input_text(self, locator, text, default_timeout=5):
        self.wait_until(
            condition=lambda d: self.get_element(locator),
            timeout=default_timeout
        ).send_keys(text)

    def select_checkbox(self, locator):
        """勾选复选框"""
        if not self.is_selected(locator):
            self.click_element(locator)

    def unselect_checkbox(self, locator):
        """去勾选复选框"""
        if self.is_selected(locator):
            self.click_element(locator)

    def is_selected(self, locator):
        el = self.get_element(locator)
        result = el.get_attribute("checked")
        if result.lower() == "true":
            return True
        return False

    def checkbox_should_be_selected(self, locator):
        # element = self.get_element(locator)
        if not self.is_selected(locator):
            raise AssertionError("Checkbox '{}' should have been selected "
                                 "but was not.".format(locator))
        return True

    def checkbox_should_not_be_selected(self, locator):
        # element = self.get_element(locator)
        if self.is_selected(locator):
            raise AssertionError("Checkbox '{}' should not have been selected "
                                 "but was not.".format(locator))
        return True

    def swipe_by_direction(self, locator, direction, duration=None):
        """
        在元素内滑动
        :param locator: 定位器
        :param direction: 方向（left,right,up,down）
        :param duration: 持续时间ms
        :return:
        """
        element = self.get_element(locator)
        rect = element.rect
        left, right = int(rect['x']) + 1, int(rect['x'] + rect['width']) - 1
        top, bottom = int(rect['y']) + 1, int(rect['y'] + rect['height']) - 1
        width = int(rect['width']) - 2
        height = int(rect['height']) - 2

        if self._get_platform() == 'android':
            if direction.lower() == 'left':
                x_start = right
                x_end = left
                y_start = (top + bottom) // 2
                y_end = (top + bottom) // 2
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'right':
                x_start = left
                x_end = right
                y_start = (top + bottom) // 2
                y_end = (top + bottom) // 2
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'up':
                x_start = (left + right) // 2
                x_end = (left + right) // 2
                y_start = bottom
                y_end = top
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'down':
                x_start = (left + right) // 2
                x_end = (left + right) // 2
                y_start = top
                y_end = bottom
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)

        else:
            if direction.lower() == 'left':
                x_start = right
                x_offset = width
                y_start = (top + bottom) // 2
                y_offset = 0
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'right':
                x_start = left
                x_offset = width
                y_start = -(top + bottom) // 2
                y_offset = 0
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'up':
                x_start = (left + right) // 2
                x_offset = 0
                y_start = bottom
                y_offset = -height
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'down':
                x_start = (left + right) // 2
                x_offset = 0
                y_start = top
                y_offset = height
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)

    def swipe_by_percent_on_screen(self, start_x, start_y, end_x, end_y, duration):
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        x_start = float(start_x) / 100 * width
        x_end = float(end_x) / 100 * width
        y_start = float(start_y) / 100 * height
        y_end = float(end_y) / 100 * height
        x_offset = x_end - x_start
        y_offset = y_end - y_start
        if self._get_platform() == 'android':
            self.driver.swipe(x_start, y_start, x_end, y_end, duration)
        else:
            self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)

    def assert_screen_contain_text(self, text):
        if not self.is_text_present(text):
            raise AssertionError("Page should have contained text '{}' "
                                 "but did not" % text)

    def assert_screen_should_not_contain_text(self, text):
        if self.is_text_present(text):
            raise AssertionError("Page should not have contained text '{}'" % text)

    def assert_screen_should_contain_element(self, locator):
        if not self._is_element_present(locator):
            raise AssertionError("Page should have contained element '{}' "
                                 "but did not".format(locator))

    def assert_should_not_contain_element(self, locator):
        if self._is_element_present(locator):
            raise AssertionError("Page should not have contained element {}".format(locator))

    def assert_element_should_be_disabled(self, locator):
        if self._is_enabled(locator):
            raise AssertionError("Element '{}' should be disabled "
                                 "but did not".format(locator))

    def assert_element_should_be_enabled(self, locator):
        if not self._is_enabled(locator):
            raise AssertionError("Element '{}' should be enabled "
                                 "but did not".format(locator))

    def assert_element_should_be_visible(self, locator):
        if not self.get_element(locator).is_displayed():
            raise AssertionError("Element '{}' should be visible "
                                 "but did not".format(locator))

    def assert_element_should_contain_text(self, locator, expected, message=''):
        actual = self.get_text(locator)
        if expected not in actual:
            if not message:
                message = "Element '{}' should have contained text '{}' but " \
                          "its text was '{}'.".format(locator, expected, actual)
            raise AssertionError(message)

    def assert_element_should_not_contain_text(self, locator, expected, message=''):
        actual = self.get_text(locator)
        if expected in actual:
            if not message:
                message = "Element {} should not contain text '{}' but " \
                          "it did.".format(locator, expected)
            raise AssertionError(message)

    def assert_element_text_should_be(self, locator, expected, message=''):
        element = self.get_element(locator)
        actual = element.text
        if expected != actual:
            if not message:
                message = "The text of element '{}' should have been '{}' but in fact it was '{}'." \
                    .format(locator, expected, actual)
            raise AssertionError(message)

    def assert_element_text_should_match(self, locator, pattern, full_match=True, regex=False):
        """断言元素内文本，支持正则表达式"""
        element = self.get_element(locator)
        actual = element.text
        if regex:
            if full_match:
                pt = re.compile(pattern)
                result = pt.fullmatch(actual)
            else:
                pt = re.compile(pattern)
                result = pt.search(actual)
        else:
            if full_match:
                result = pattern == actual
            else:
                result = pattern in actual
        if not result:
            raise AssertionError(
                "Expect is" + " match regex pattern" if regex else "" + ": " + pattern + "\n"
                                                                   + "Actual is: " + actual + '\n')

    def run_app_in_background(self, seconds=5):
        """让 app 进入后台运行seconds 秒"""
        self.driver.background_app(seconds)

    def get_network_status(self):
        """获取网络链接状态"""
        return self.driver.network_connection

    def set_network_status(self, status):
        """设置网络
        Connection types are specified here:
        https://code.google.com/p/selenium/source/browse/spec-draft.md?repo=mobile#120
        Value (Alias)      | Data | Wifi | Airplane Mode
        -------------------------------------------------
        0 (None)           | 0    | 0    | 0
        1 (Airplane Mode)  | 0    | 0    | 1
        2 (Wifi only)      | 0    | 1    | 0
        4 (Data only)      | 1    | 0    | 0
        6 (All network on) | 1    | 1    | 0

        class ConnectionType(object):
            NO_CONNECTION = 0
            AIRPLANE_MODE = 1
            WIFI_ONLY = 2
            DATA_ONLY = 4
            ALL_NETWORK_ON = 6

        """
        self.driver.set_network_connection(status)

    def push_file(self, to_path, file_path):
        """推送apk到手机"""
        with open(file_path, 'rb') as f:
            content = f.read()
            mda = hashlib.md5(content).hexdigest()
        b64 = str(base64.b64encode(content), 'UTF-8')
        self.driver.push_file(to_path, b64)
        if self.is_android():
            # 安卓使用shell命令验证MD5
            mdb = self.execute_shell_command('md5sum', '-b', to_path).strip()
            return mda == mdb
        else:
            # TODO IOS MD5验证待实现
            return True

    @TestLogger.log('隐藏键盘')
    def hide_keyboard(self, key_name=None, key=None, strategy=None):
        """隐藏键盘"""
        self.driver.hide_keyboard(key_name, key, strategy)

    @TestLogger.log('发送短信')
    def send_sms(self, to, content, card_index=0):
        if self.is_android():
            self.terminate_app('com.android.mms')
            self.execute_shell_command('am', 'start', '-a', 'android.intent.action.SENDTO', '-d', 'sms:', '-e',
                                       'sms_body', content, '--ez', 'exit_on_sent', 'true')
            self.execute_shell_command('input', 'text', to)
            self.click_element([MobileBy.XPATH, '//*[@content-desc="发送"]'])
        elif self.is_ios():
            # TODO IOS发短信功能待实现
            pass
        else:
            pass

    def set_clipboard_text(self, text, label=None):
        self.driver.set_clipboard_text(text, label)

    @TestLogger.log("粘贴")
    def paste(self):
        pass

    def __str__(self):
        device_info = {
            "name": self.alis,
            "model": self.model_info["ReadableName"]
        }
        return json.dumps(device_info, ensure_ascii=False)
