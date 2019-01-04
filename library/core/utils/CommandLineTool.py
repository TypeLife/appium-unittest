import argparse
import json
import os

from library.core.utils.testcasefilter import TEST_CASE_TAG_ENVIRON


def parse_and_store_command_line_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('--suite', '-s', action='append')  # 测试套件路径
    parser.add_argument('--include', '-i', action='append')  # 匹配的用例标签
    parser.add_argument('--melp', '-m')
    args = parser.parse_args()
    if args.include:
        include = json.dumps(args.include, ensure_ascii=False).upper()
        os.environ[TEST_CASE_TAG_ENVIRON] = include
    return args
