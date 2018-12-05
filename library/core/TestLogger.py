import datetime
import functools
import os
import re

from library.core.utils import ConfigManager, common
from library.core.utils.common import capture_screen_shot


class TestLogger(object):
    current_test = None
    log_level = 'INFO'
    _do_log = True

    @staticmethod
    def log(info=None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kw):
                # info = description if description else func.__doc__
                template = '%(time)s - %(className)s - %(level)s - %(caseName)s - %(func)s ' \
                           + '- [%(mobile)s]%(description)s - %(args)s'
                TestLogger.log_level = "INFO"
                turn_on = False
                try:
                    if TestLogger._do_log:
                        turn_on = True
                        TestLogger._do_log = False
                    result = func(*args, **kw)
                    return result
                except Exception as error:
                    TestLogger.log_level = "ERROR"
                    raise error

                finally:
                    if turn_on:
                        TestLogger._do_log = True
                        # from library.core.BasePage import BasePage
                        from library.core.utils import applicationcache as cache
                        mobile = cache.current_mobile()
                        log_info = func.__doc__ if info is None else info
                        print(template % dict(time=datetime.datetime.now().__str__(),
                                              className=getattr(TestLogger.current_test.__class__, '__name__'),
                                              level=TestLogger.log_level,
                                              caseName=getattr(TestLogger.current_test, '_testMethodName', None),
                                              func=common.get_method_fullname(func),
                                              mobile=mobile.__str__(),
                                              description=log_info if log_info else "no description",
                                              # args='[Args: {} {}]'.format(
                                              #     args[1:] if bool(args[:1]) and isinstance(args[0],
                                              #                                               BasePage) else args,
                                              #     kw)
                                              args='[Args: {} {}]'.format(args, kw),
                                              )
                              )
                        TestLogger.log_level = "INFO"

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
                    getattr(TestLogger.current_test.__class__, '__name__'),
                    TestLogger.log_level,
                    getattr(TestLogger.current_test, '_testMethodName', None),
                    '********** TEST START **********'
                ]
            ))

    @staticmethod
    def stop_test(test):
        if getattr(TestLogger.current_test, '_testMethodName', None):
            print(' - '.join(
                [
                    datetime.datetime.now().__str__(),
                    getattr(test.__class__, '__name__'),
                    TestLogger.log_level,
                    getattr(test, '_testMethodName', None),
                    '********** TEST FINISHED **********'
                ]
            ))
        TestLogger.current_test = None

    @staticmethod
    def test_fail(test):
        TestLogger.take_screen_shot()
        if getattr(test, '_testMethodName', None):
            print(' - '.join(
                [
                    datetime.datetime.now().__str__(),
                    getattr(test.__class__, '__name__'),
                    TestLogger.log_level,
                    getattr(test, '_testMethodName', None),
                    '********** TEST FAIL **********'
                ]
            ))
        TestLogger.current_test = None

    @staticmethod
    def test_error(test):
        TestLogger.take_screen_shot()
        if getattr(test, '_testMethodName', None):
            print(' - '.join(
                [
                    datetime.datetime.now().__str__(),
                    getattr(test.__class__, '__name__'),
                    TestLogger.log_level,
                    getattr(test, '_testMethodName', None),
                    '********** TEST ERROR **********'
                ]
            ))
        TestLogger.current_test = None

    @staticmethod
    def test_success(test):
        if getattr(test, '_testMethodName', None):
            print(' - '.join(
                [
                    datetime.datetime.now().__str__(),
                    getattr(test.__class__, '__name__'),
                    TestLogger.log_level,
                    getattr(test, '_testMethodName', None),
                    '********** TEST SUCCESS **********'
                ]
            ))
        TestLogger.current_test = None

    @staticmethod
    def take_screen_shot():
        method_name = getattr(TestLogger.current_test, '_testMethodName', '')
        exception_time = re.sub(r'[:.]', '-', datetime.datetime.now().__str__())
        file_name = "%(method)s - %(time)s.png" % {'method': method_name, 'time': exception_time}
        path = os.path.join(ConfigManager.get_screen_shot_path(), file_name)
        if capture_screen_shot(path):
            print(datetime.datetime.now().__str__() + ' - INFO - ' + "截图路径：" + path)

# def capture_screen_shot(path):
#     if os.path.isfile(path):
#         os.remove(path)
#     dir_name, file_name = os.path.split(path)
#     if not os.path.isdir(dir_name):
#         os.makedirs(dir_name)
#     capture = getattr(DriverCache.current_driver, 'get_screenshot_as_file', lambda p: None)
#     result = capture(path)
#     return result
