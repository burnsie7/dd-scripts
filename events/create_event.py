from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)

title = "My Example Event"
text = 'These are the details'
tags = ['example-tag:123xyz']

api.Event.create(title=title, text=text, tags=tags)
