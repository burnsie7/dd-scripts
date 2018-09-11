import sys
import os

from argparse import ArgumentParser

from datadog import initialize, api

parser = ArgumentParser(description='script template')
parser.add_argument('--api-key', help='Datadog API key', required=False)
parser.add_argument('--app-key', help='Datadog APP key', required=False)
parser.add_argument('--my_arg', help='My Arg', required=False)

args = parser.parse_args()

options = {
    'api_key': args.api_key if args.api_key else os.environ.get('DD_API_KEY'),
    'app_key': args.app_key if args.app_key else os.environ.get('DD_APP_KEY'),
}

initialize(**options)


class MainClass(object):

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def main(self):
        pass

MainClass().main()
