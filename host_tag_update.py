import json
import os
import requests
import sys

import pprint

from datadog import initialize, api

DD_API_KEY = os.getenv('DD_API_KEY', '')
DD_APP_KEY = os.getenv('DD_APP_KEY', '')

options = {
    'api_key': DD_API_KEY,
    'app_key': DD_APP_KEY
}

initialize(**options)

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

#hn = input('Enter hostname: ')
my_hostname = raw_input('Enter hostname: ')

tags = api.Tag.get(my_hostname)['tags']

tagset = []
for tag in tags:
    keep = query_yes_no("Keep this tag: '{}'?".format(tag))
    if keep:
        tagset.append(tag)

print("Updated tagset:")
print(tagset)
update = query_yes_no("Proceed updating tagset?  This will overwrite all current tags.")
if update:
    api.Tag.update(my_hostname, tags=tagset)
