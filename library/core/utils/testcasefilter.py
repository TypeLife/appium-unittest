import json
import os
import unittest
from json import JSONDecodeError

TEST_CASE_TAG_ENVIRON = 'RUN_TAG'


class FilterResult:
    RUN = True
    NOT_RUN = False


def set_tags(*args):
    tag_types = set()
    for arg in args:
        tag_types.add(str(arg))
    env_value = json.dumps(list(tag_types), ensure_ascii=False).upper()
    os.environ[TEST_CASE_TAG_ENVIRON] = env_value


def tags(*args):
    flags = set()
    for arg in args:
        real_tag = str(arg).upper()
        flags.add(real_tag)
    if (TEST_CASE_TAG_ENVIRON not in os.environ) or (not os.environ[TEST_CASE_TAG_ENVIRON]):
        return unittest.skipIf(not FilterResult.RUN, '')
    try:
        case_tags = json.loads(os.environ[TEST_CASE_TAG_ENVIRON])
        if not isinstance(case_tags, list):
            return unittest.skipIf(not FilterResult.RUN, '')
        if flags.issuperset(set(case_tags)):
            return unittest.skipIf(not FilterResult.RUN, '')
        else:
            return unittest.skip("用例类型:{}; ".format(flags) + '当前执行:{}.'.format(case_tags))
    except JSONDecodeError:
        return unittest.skipIf(not FilterResult.RUN, '')
