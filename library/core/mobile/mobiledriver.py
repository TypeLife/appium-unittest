import json
from abc import *

from appium import webdriver
from selenium.common.exceptions import InvalidSessionIdException


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
                t = self.driver.device_time
                return True
            except InvalidSessionIdException:
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
        return self.driver.execute_script('mobile:shell', script)

    def __str__(self):
        device_info = {
            "name": self.alis,
            "model": self.model_info["ReadableName"]
        }
        return json.dumps(device_info, ensure_ascii=False)
