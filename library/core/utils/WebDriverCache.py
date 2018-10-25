from appium import webdriver


class DriverCache:
    current_driver = None
    drivers = {}

    @staticmethod
    def register_driver(driver, alis):
        if alis:
            DriverCache.drivers[alis] = driver
        else:
            raise Exception('alis name(: {} ) must a readable name!'.format(alis))

    @staticmethod
    def get_driver(alis):
        DriverCache.current_driver = DriverCache.drivers.get(alis)
        return DriverCache.current_driver

    @staticmethod
    def open_app(server, desired_caps, alis=None):
        if alis in DriverCache.drivers.keys():
            raise Exception('Alis name(: {} ) has been registered'.format(alis))
        driver = webdriver.Remote(server, desired_caps)
        DriverCache.current_driver = driver
        if alis:
            DriverCache.register_driver(driver, alis)
        return DriverCache.current_driver

    @staticmethod
    def close_app():
        DriverCache.current_driver.close_app()

    @staticmethod
    def launch_app():
        DriverCache.current_driver.launch_app()

    @staticmethod
    def quit_current():
        if DriverCache.current_driver is not None:
            DriverCache.current_driver.quit()
            DriverCache.current_driver = None

    @staticmethod
    def quit_all():
        DriverCache.current_driver.close_app()
        for d in DriverCache.drivers.values():
            d.quit()