### delete all dashes

from datadog import initialize, api

API_KEY = '<api_key>'
APP_KEY = '<api_key>'
initialize(api_key=API_KEY, app_key=APP_KEY)

timeboards = api.Timeboard.get_all()
for dash in timeboards['dashes']:
  api.Timeboard.delete(dash['id'])

screenboards = api.Screenboard.get_all()
for dash in screenboards['screenboards']:
  api.Screenboard.delete(dash['id'])
