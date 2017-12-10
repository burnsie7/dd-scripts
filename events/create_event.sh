#!/bin/sh
# Make sure you replace the API and/or APP key below
# with the ones for your account

curl  -X POST -H "Content-type: application/json" \
-d '{
      "title": "Test Email Event",
      "text": "Testing",
      "priority": "normal",
      "tags": ["cmscustomerid:6789", "something_else:sdfsd"],
      "alert_type": "info"
  }' \
'https://app.datadoghq.com/api/v1/events?api_key=<api key>'
