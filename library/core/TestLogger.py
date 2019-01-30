import functools
import os
import re
import time

from library.core.utils.common import capture_screen_shot

_time = time.time
_localtime = time.localtime
_strftime = time.strftime


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
                template = '%(time)s - %(mobile)s - %(level)s - %(caseName)s - %(func)s%(args)s ' \
                           + '- %(description)s'
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
                        from library.core.utils import applicationcache
                        from library.core.utils import common
                        current_mobile = getattr(applicationcache, 'current_mobile', lambda: None)
                        mobile = current_mobile()
                        log_info = func.__doc__ if info is None else info

                        current_time = _time()
                        (current_time_int, current_time_fraction) = divmod(current_time, 1)
                        current_time_struct = _localtime(current_time_int)

                        timestamp = _strftime("%Y-%m-%dT%H:%M:%S.", current_time_struct) + "%03d" % (
                            int(current_time_fraction * 1000))
                        import inspect
                        received_args = inspect.getcallargs(func, *args, **kw)
                        if 'self' in received_args:
                            received_args.pop('self')
                        print(template % dict(time=timestamp,
                                              level=TestLogger.log_level,
                                              # caseName=getattr(TestLogger.current_test, '_testMethodName', None),
                                              caseName=common.get_test_id(TestLogger.current_test),
                                              func=common.get_method_fullname(func),
                                              mobile=mobile.__str__(),
                                              description=log_info if log_info else "no description",
                                              # args='[Args: {} {}]'.format(
                                              #     args[1:] if bool(args[:1]) and isinstance(args[0],
                                              #                                               BasePage) else args,
                                              #     kw)
                                              args='{}'.format(received_args),
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
        from library.core.utils import common
        TestLogger.current_test = test
        current_time = _time()
        (current_time_int, current_time_fraction) = divmod(current_time, 1)
        current_time_struct = _localtime(current_time_int)

        timestamp = _strftime("%Y-%m-%dT%H:%M:%S.", current_time_struct) + "%03d" % (
            int(current_time_fraction * 1000))
        if getattr(TestLogger.current_test, '_testMethodName', None):
            print(' - '.join(
                [
                    '\n' + timestamp,
                    # getattr(TestLogger.current_test.__class__, '__name__'),
                    TestLogger.log_level,
                    common.get_test_id(test),
                    '********** TEST START **********'
                ]
            ))

    @staticmethod
    def stop_test(test):
        TestLogger.current_test = None

    @staticmethod
    def test_fail(test, err):
        from library.core.utils import common
        current_time = _time()
        (current_time_int, current_time_fraction) = divmod(current_time, 1)
        current_time_struct = _localtime(current_time_int)

        timestamp = _strftime("%Y-%m-%dT%H:%M:%S.", current_time_struct) + "%03d" % (
            int(current_time_fraction * 1000))
        import sys
        sys.excepthook(*err)
        TestLogger.take_screen_shot()
        # print(common.convert_error_to_string(err))
        if getattr(test, '_testMethodName', None):
            print(' - '.join(
                [
                    timestamp,
                    TestLogger.log_level,
                    common.get_test_id(test),
                    '********** TEST FAIL **********'
                ]
            ))
        TestLogger.current_test = None

    @staticmethod
    def test_error(test, err):
        from library.core.utils import common
        current_time = _time()
        (current_time_int, current_time_fraction) = divmod(current_time, 1)
        current_time_struct = _localtime(current_time_int)

        timestamp = _strftime("%Y-%m-%dT%H:%M:%S.", current_time_struct) + "%03d" % (
            int(current_time_fraction * 1000))
        import sys
        sys.excepthook(*err)
        TestLogger.take_screen_shot()
        # print(common.convert_error_to_string(err))
        if getattr(test, '_testMethodName', None):
            print(' - '.join(
                [
                    timestamp,
                    TestLogger.log_level,
                    common.get_test_id(test),
                    '********** TEST ERROR **********'
                ]
            ))
        TestLogger.current_test = None

    @staticmethod
    def test_success(test):
        from library.core.utils import common
        current_time = _time()
        (current_time_int, current_time_fraction) = divmod(current_time, 1)
        current_time_struct = _localtime(current_time_int)

        timestamp = _strftime("%Y-%m-%dT%H:%M:%S.", current_time_struct) + "%03d" % (
            int(current_time_fraction * 1000))
        if getattr(test, '_testMethodName', None):
            print(' - '.join(
                [
                    timestamp,
                    TestLogger.log_level,
                    common.get_test_id(test),
                    '********** TEST SUCCESS **********'
                ]
            ))
        TestLogger.current_test = None

    @staticmethod
    def test_skip(test, reason):
        from library.core.utils import common
        current_time = _time()
        (current_time_int, current_time_fraction) = divmod(current_time, 1)
        current_time_struct = _localtime(current_time_int)

        timestamp = _strftime("%Y-%m-%dT%H:%M:%S.", current_time_struct) + "%03d" % (
            int(current_time_fraction * 1000))
        if getattr(test, '_testMethodName', None):
            print(' - '.join(
                [
                    timestamp,
                    TestLogger.log_level,
                    common.get_test_id(test),
                    '********** TEST SKIP ********** (原因：{})'.format(reason)
                ]
            ))
        TestLogger.current_test = None

    @staticmethod
    def take_screen_shot():
        current_time = _time()
        (current_time_int, current_time_fraction) = divmod(current_time, 1)
        current_time_struct = _localtime(current_time_int)

        timestamp = _strftime("%Y-%m-%dT%H:%M:%S.", current_time_struct) + "%03d" % (
            int(current_time_fraction * 1000))
        method_name = getattr(TestLogger.current_test, '_testMethodName', '')
        exception_time = re.sub(r'[:.]', '-', timestamp)
        file_name = "%(method)s - %(time)s.png" % {'method': method_name, 'time': exception_time}
        from library.core.utils import ConfigManager
        path = os.path.join(ConfigManager.get_screen_shot_path(), file_name)
        if capture_screen_shot(path):
            print(timestamp + ' - INFO - ' + "截图路径：" + path)
