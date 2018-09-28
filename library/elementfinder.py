# -*- coding: utf-8 -*-
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement

from library.config import DriverCache
from selenium.webdriver import Remote


class ElementFinder:

    @staticmethod
    def find_element(by, parent=None):
        if isinstance(parent, SeleniumWebElement):
            element = parent.find_element(by[0], by[1])
        else:
            assert isinstance(DriverCache.current_driver, Remote)
            element = DriverCache.current_driver.find_element(by[0], by[1])
        return element

    @staticmethod
    def find_elements(by, parent=None):
        if isinstance(parent, SeleniumWebElement):
            elements = parent.find_elements(by[0], by[1])
        else:
            assert isinstance(DriverCache.current_driver, Remote)
            elements = DriverCache.current_driver.find_elements(by[0], by[1])
        return elements
