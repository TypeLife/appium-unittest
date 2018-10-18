from appium import webdriver

from library import config


class Base(object):
    @property
    def driver(self):
        assert isinstance(config.DriverCache.current_driver, webdriver.Remote)
        return config.DriverCache.current_driver

    def get_element(self, by):
        return self.driver.find_element(by=by[0], value=by[1])

    def click(self, by):
        self.get_element(by).click()

    def input(self, by, text):
        self.get_element(by).send_keys(text)

    def long_press(self, by, seconds):
        # self.get_element(by).
        pass
