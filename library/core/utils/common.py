import inspect
import os
import re

import settings
from library.core.utils.applicationcache import MOBILE_DRIVER_CACHE


def open_or_create(path, mode='r'):
    if os.path.isfile(path):
        os.remove(path)
    dir_name, file_name = os.path.split(path)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    fp = open(path, mode)
    return fp


def get_log_file():
    log_date = re.sub(r'[:.]', '-', settings.NOW.__str__())
    file_path = os.path.join(settings.LOG_FILE_PATH, settings.NOW.date().__str__(), log_date + '.log')
    dir_name, file_name = os.path.split(file_path)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    fp = open(file_path, 'a', encoding='UTF-8')
    return fp


def write_str_to_log_file(s):
    with get_log_file() as log_file:
        log_file.write(s)


def write_lines_to_log_file(lines):
    with get_log_file() as log_file:
        log_file.writelines(lines)


def get_method_fullname(func):
    if inspect.ismethod(func):
        try:
            cls = func.__self__.__class__

        except:
            return func.__name__
        module = cls.__module__
        if module is None or module == str.__class__.__module__:
            return cls.__name__ + '.' + func.__name__
        return module + '.' + cls.__name__ + '.' + func.__name__
    elif inspect.isfunction(func):
        return func.__qualname__
    else:
        return func.__name__


def capture_screen_shot(path):
    if os.path.isfile(path):
        os.remove(path)
    dir_name, file_name = os.path.split(path)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    capture = getattr(MOBILE_DRIVER_CACHE.current.driver, 'get_screenshot_as_file', lambda p: None)
    result = capture(path)
    return result
