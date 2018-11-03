import json
import re
from abc import *
from unicodedata import normalize

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.support.wait import WebDriverWait


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

    def __del__(self):
        quit_driver = getattr(self.driver, 'quit', lambda: None)
        try:
            print('Remove ' + self.__str__())
            quit_driver()
        except:
            pass

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
            if card_slot[n]['TYPE'] in self.supported_card_types():
                cards.append(card_slot[n])
            else:
                raise Exception('该手机不支持' + card_slot[n]['TYPE'] + '类型SIM卡（支持类型：{}）'
                                .format(self.supported_card_types()))
        return cards

    def get_cards(self, card_type):
        """返回指定类型卡手机号列表"""
        return [card['CARD_NUMBER'] for card in self._card_slot if card['TYPE'] == card_type]

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
            self._driver = webdriver.Remote(self._remote_url, self._desired_caps, self._browser_profile, self._proxy,
                                            self._keep_alive)
        elif not self.is_connection_created:
            self.driver.start_session(self._desired_caps)
        else:
            return

    def disconnect_mobile(self):
        self.driver.quit()

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

    def __str__(self):
        device_info = {
            "name": self.alis,
            "model": self.model_info["ReadableName"]
        }
        return json.dumps(device_info, ensure_ascii=False)
