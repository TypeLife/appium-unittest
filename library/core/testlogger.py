import datetime
import functools


class TestLogger(object):
    current_test = None
    log_level = 'INFO'

    @staticmethod
    def log(info=None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kw):
                # info = description if description else func.__doc__
                template = '%(time)s - %(caseName)s - %(level)s - %(func)s - %(description)s'
                TestLogger.log_level = "INFO"
                try:
                    result = func(*args, **kw)
                    return result
                except Exception as error:
                    TestLogger.log_level = "ERROR"
                    raise error
                finally:
                    log_info = func.__doc__ if info is None else info
                    print(template % {'time': datetime.datetime.now().__str__(),
                                      'caseName': getattr(TestLogger.current_test, '_testMethodName', None),
                                      'level': TestLogger.log_level,
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
