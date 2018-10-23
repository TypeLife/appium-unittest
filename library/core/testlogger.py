import datetime
import functools
import os
import re

from library import settings, config


class TestLogger(object):
    current_test = None
    log_level = 'INFO'

    @staticmethod
    def log(info=None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kw):
                # info = description if description else func.__doc__
                template = '%(time)s - %(className)s - %(level)s - %(caseName)s - %(func)s - %(description)s'
                TestLogger.log_level = "INFO"
                try:
                    result = func(*args, **kw)
                    return result
                except Exception as error:
                    TestLogger.log_level = "ERROR"
                    TestLogger.take_screen_shot()
                    raise error
                finally:
                    log_info = func.__doc__ if info is None else info
                    print(template % {'time': datetime.datetime.now().__str__(),
                                      'className': getattr(TestLogger.current_test.__class__, '__name__'),
                                      'level': TestLogger.log_level,
                                      'caseName': getattr(TestLogger.current_test, '_testMethodName', None),
                                      'func': func.__name__,
                                      'description': log_info if log_info else "no description"})

            return wrapper

        return decorator

    @staticmethod
    def set_current_test(test):
        TestLogger.current_test = test

    @staticmethod
    def reset_current_test():
        TestLogger.current_test = None

    @staticmethod
    def start_test(test):
        TestLogger.current_test = test
        if getattr(TestLogger.current_test, '_testMethodName', None):
            print(' - '.join(
                [
                    '\n' + datetime.datetime.now().__str__(),
                    getattr(TestLogger.current_test, '_testMethodName', None),
                    TestLogger.log_level,
                    '********** TEST START **********'
                ]
            ))

    @staticmethod
    def stop_test():
        if getattr(TestLogger.current_test, '_testMethodName', None):
            print(' - '.join(
                [
                    datetime.datetime.now().__str__(),
                    getattr(TestLogger.current_test, '_testMethodName', None),
                    TestLogger.log_level,
                    '********** TEST END **********'
                ]
            ))
        TestLogger.current_test = None

    @staticmethod
    def take_screen_shot():
        method_name = getattr(TestLogger.current_test, '_testMethodName', '')
        exception_time = re.sub(r':|\.', '-', datetime.datetime.now().__str__())
        file_name = "%(method)s - %(time)s.png" % {'method': method_name, 'time': exception_time}
        path = os.path.join(settings.SCREEN_SHOT_PATH, file_name)
        if capture_screen_shot(path):
            print(datetime.datetime.now().__str__() + ' - INFO - ' + "截图路径：" + path)


def capture_screen_shot(path):
    if os.path.isfile(path):
        os.remove(path)
    dir_name, file_name = os.path.split(path)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    result = config.DriverCache.current_driver.get_screenshot_as_file(path)
    return result
