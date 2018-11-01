from abc import ABC, abstractmethod
from appium import webdriver


class Mobile(ABC):

    def __init__(self, alis_name, model_info, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None, keep_alive=False, card_slot=None):
        self._alis = alis_name
        self._model_info = model_info
        self._remote_url = command_executor
        self._desired_caps = desired_capabilities
        self._browser_profile = browser_profile
        self._proxy = proxy
        self._keep_alive = keep_alive
        self._card_slot = card_slot
        self._driver = None

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
    def card_number(self):
        raise NotImplementedError("This method must be implemented!")

    @property
    def is_online(self):
        if self.driver is None:
            return False
        else:
            # session失效的情况暂时不做判断
            return True

    @property
    def card_types(self):
        types = []
        if self._card_slot is None:
            return types

        for card in self._card_slot.values():
            if card is not None and 'TYPE' in card:
                types.append(card['TYPE'])
        return types

    def connect_mobile(self):
        self._driver = webdriver.Remote(self._remote_url, self._desired_caps, self._browser_profile, self._proxy,
                                        self._keep_alive)

    def disconnect_mobile(self):
        self.driver.quit()
