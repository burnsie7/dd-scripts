import json
from pprint import pprint

source_dash = json.load(open('swfgv5.json'))
new_dash = json.load(open('aws_rds.json'))

source_widgets = source_dash['widgets']
new_widgets = new_dash['widgets']

source_max_x = get_max_x(source_widgets)
update_x(new_widgets, source_max_x)
export_widgets(new_widgets, 'export_rds.json')

def export_widgets(widgets, filename):
    for widget in widgets:
    with open(filename, 'w') as outfile:
        json.dump(widgets, outfile, indent=4, sort_keys=True)

def get_max_x(widgets):
    max_x = 0
    for w in widgets:
        x = w['x']
        wd = w['width']
        if max_x < (x + wd):
            max_x = x + wd
    return max_x

def update_x(widgets, x):
    for w in widgets:
        w['x'] = w['x'] + x
        if w['y'] < 2:
            w['y'] = 0
