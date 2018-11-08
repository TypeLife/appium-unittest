import argparse
import json
import os

from library.core.utils.testcasefilter import TEST_CASE_TAG_ENVIRON


def parse_and_store_command_line_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('--include', '-i', action='append')
    parser.add_argument('--melp', '-m')
    args = parser.parse_args()
    if args.include:
        include = json.dumps(args.include)
        os.environ[TEST_CASE_TAG_ENVIRON] = include
