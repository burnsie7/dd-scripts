import datetime
import time
import requests
import simplejson

from datadog import initialize, api

ORG_KEYS = {
    'main': {'api_key': '4xxxxxx9','app_key': 'a21bxxxxxxxf'},
    'beta': {'api_key': '7xxxxxxf', 'app_key': 'df6xxxxxxx97'},
    'prod': {'api_key': 'cxxxxxxd', 'app_key': '62bxxxxxxxda'},
    'prod0': {'api_key': 'xxxxxxe2', 'app_key': '17xxxxxxx3b2'},
    'tap': {'api_key': '78xxxxxx', 'app_key': '4934xxxxxxx2'},
}

hosts_up = []
hosts_recent = []
host_count_check_up = 0
host_usage_history = []

# get host count for all orgs, including parent
now = int(time.time())
host_query = "sum:aws.ec2.host_ok{*}+sum:datadog.agent.running{!cloud_provider:aws}"
USAGE_URL = 'https://app.datadoghq.com/api/v1/usage/'

def build_standard_url(endpoint, dd_keys):
    # Example date format for hour: 2018-03-14T09
    start = datetime.datetime.now() - datetime.timedelta(hours=48)
    start_hr = start.strftime('%Y-%m-%dT%H')
    end = datetime.datetime.now() - datetime.timedelta(hours=47)
    end_hr = end.strftime('%Y-%m-%dT%H')
    url = USAGE_URL + endpoint + dd_keys + '&start_hr=' + start_hr + '&end_hr=' + end_hr
    return url, start_hr

def get_usage_metrics(url):
    usage_metrics = []
    try:
        usage_metrics = requests.get(url).json().get('usage', None)
    except requests.exceptions.MissingSchema:
        print('Invalid URL format: {}'.format(url))
    except requests.exceptions.ConnectionError:
        print('Could not connect to url: {}'.format(url))
    except simplejson.scanner.JSONDecodeError:
        print('The response did not contain JSON data')
    return usage_metrics

def format_standard_metrics(metrics, start_hr, tags):
    metric_list = []
    for metric_dict in metrics:
        try:
            for k, v in metric_dict.iteritems():
                if k == 'hour':
                    if v != start_hr:
                        print('Incorrect hour for metrics. Aborting metric submission.')
                        return
                else:
                    metric_name = 'datadog.usage.' + k
                    metric_list.append({'metric': metric_name, 'points': v, 'tags': tags})
        except AttributeError:
            print('Metrics are not in dict format')
    return metric_list

for key, value in ORG_KEYS.iteritems():
    print('checking value of %s' % key)
    initialize(**value)
    try:
        # get count of hosts reporting metrics, excluding muted hosts
        last_value = 0
        query_result = api.Metric.query(start=now - 300, end=now, query=host_query)
        if query_result.get('errors', None):
            print(query_result['errors'])
            host_count_check_up = 3
        else:
            series = query_result.get('series', None)
            if series:
                pointlist = series[0].get('pointlist', None)
                if pointlist and pointlist[0][1]:
                    last_value = pointlist[0][1]
        hosts_recent.append({'metric': 'datadog.hosts.recent', 'points': last_value, 'tags': ["env:{}".format(key)]})

        # get host up count for all hosts for last 2 hours including muted hosts
        up_count = 0
        host_res = api.Hosts.totals()
        if host_res.get('errors', None):
            print(host_res['errors'])
            host_count_check_up = False
        up_count = host_res['total_up']
        hosts_up.append({'metric': 'datadog.hosts.up', 'points': up_count, 'tags': ["env:{}".format(key)]})

        # get the usage metrics from 48 hours ago
        dd_keys = '?api_key=' + value['api_key'] + '&application_key=' + value['app_key']
        url, start_hr = build_standard_url('hosts', dd_keys)
        metrics = get_usage_metrics(url)
        tags = ["env:{}".format(key)]
        metrics_list = format_standard_metrics(metrics, start_hr, tags)
        if len(metrics_list):
            host_usage_history.append(metrics_list)
        else:
            print('No usage metrics available for endpiont: {}'.format(key))

    except Exception as e:
        print(e)
        host_count_check_up = 3

# submit active host count to parent org
initialize(**ORG_KEYS['main'])
for i in hosts_up:
    metric = i['metric']
    points = i['points']
    tags = i['tags']
    api.Metric.send(metric=metric, points=points, tags=tags)

for i in hosts_recent:
    metric = i['metric']
    points = i['points']
    tags = i['tags']
    api.Metric.send(metric=metric, points=points, tags=tags)

for metric_list in host_usage_history:
    api.Metric.send(metric_list)

api.ServiceCheck.check(check='datadog.host_count_check', host_name='temp', status=host_count_check_up)
