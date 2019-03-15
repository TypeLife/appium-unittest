import inspect
import os
import re
import sys
import traceback
from io import StringIO

import settings
from library.core.utils.connectioncache import NoConnection

_ERROR_HOLDERS_FQN = ("unittest.suite._ErrorHolder", "unittest2.suite._ErrorHolder")
_ENCODING = sys.stdin.encoding if sys.stdin.encoding else "UTF-8"


class FlushingStringIO(StringIO, object):
    encoding = _ENCODING  # stdout must have encoding

    def __init__(self, flush_function):
        super(FlushingStringIO, self).__init__()

        self._flush_function = flush_function
        self.encoding = _ENCODING

    def _flush_to_flush_function(self):
        self._flush_function(self.getvalue())
        self.seek(0)
        self.truncate()

    def write(self, str):
        super(FlushingStringIO, self).write(str)

        if '\n' in str:
            self._flush_to_flush_function()

    def flush(self, *args, **kwargs):
        self._flush_to_flush_function()
        return super(FlushingStringIO, self).flush(*args, **kwargs)


def open_or_create(path, mode='r'):
    if os.path.isfile(path):
        os.remove(path)
    dir_name, file_name = os.path.split(path)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    fp = open(path, mode)
    return fp


def get_log_file():
    file_path = settings.LOG_FILE_PATH
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


def get_class_fullname(something):
    if inspect.isclass(something):
        cls = something
    else:
        cls = something.__class__

    module = cls.__module__
    if module is None or module == str.__class__.__module__:
        return cls.__name__
    return module + '.' + cls.__name__


def get_test_id(test):
    if isinstance(test, str):
        return test
    elif test is None:
        return "No_Test"
    test_class_fullname = get_class_fullname(test)
    test_id = test.id()

    if test_class_fullname in _ERROR_HOLDERS_FQN:
        return re.sub(r'^(.*) \((.*)\)$', r'\2.\1', test_id)

    # Force test_id for doctests
    if test_class_fullname != "doctest.DocTestCase":
        desc = test.shortDescription()
        test_method_name = getattr(test, "_testMethodName", "")
        if desc and desc != test_id and desc != test_method_name:
            return "%s (%s)" % (test_id, desc.replace('.', '_'))

    return test_id


def convert_error_to_string(err, frames_to_skip_from_tail=0):
    try:
        exctype, value, tb = err
        trace = traceback.format_exception(exctype, value, tb)
        if frames_to_skip_from_tail:
            trace = trace[:-frames_to_skip_from_tail]
        return ''.join(trace)
    except Exception:
        tb = traceback.format_exc()
        return "*FAILED TO GET TRACEBACK*: " + tb


def capture_screen_shot(path):
    from library.core.utils import applicationcache
    if os.path.isfile(path):
        os.remove(path)
    dir_name, file_name = os.path.split(path)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    if not isinstance(applicationcache.current_mobile(), NoConnection):
        capture = getattr(applicationcache.current_driver(), 'get_screenshot_as_file', lambda p: None)
        try:
            result = capture(path)
            return result
        except:
            return
    return
