from library.core.utils.mobilemanager import MobileManager

MOBILE_DRIVER_CACHE = MobileManager()


def current_mobile():
    return MOBILE_DRIVER_CACHE.current


def current_driver():
    return MOBILE_DRIVER_CACHE.current.driver


def switch_to_mobile(alis):
    return MOBILE_DRIVER_CACHE.switch(alis)
