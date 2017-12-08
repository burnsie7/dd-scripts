import os
import sys
import time

import requests

from argparse import ArgumentParser

from datadog import initialize, api

parser = ArgumentParser(description='script template')
parser.add_argument('--api-key', help='Datadog API key', required=False)
parser.add_argument('--app-key', help='Datadog APP key', required=False)
parser.add_argument('--my_arg', help='My Arg', required=False)

args = parser.parse_args()

API_KEY = args.api_key if args.api_key else os.environ.get('DD_API_KEY'),
APP_KEY = args.app_key if args.app_key else os.environ.get('DD_APP_KEY'),

options = {
    'api_key': API_KEY,
    'app_key': APP_KEY
}

initialize(**options)


class MainClass(object):

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def main(self, api_key, app_key):
        from_time = int(time.time() - (24*60*60))
        # Only supported via shell
        url = 'https://app.datadoghq.com/api/v1/metrics?from=%s&api_key=%s&application_key=%s' % (from_time, api_key, app_key)
        r = requests.get(url)
        if r.status_code == 200:
            custom_metrics = []
            metrics = r.json()['metrics']
            print(len(metrics))
            for metric in metrics:
                if metric.startswith('aws') or metric.startswith('memcache') or metric.startswith('mysql'):
                    pass
                else:
                    custom_metrics.append(metric)
            print(len(custom_metrics))
        check_metric = custom_metrics[0]
        r = api.Metadata.get(metric_name=check_metric)
        print(r)
        pass

MainClass().main(API_KEY[0], APP_KEY[0])
