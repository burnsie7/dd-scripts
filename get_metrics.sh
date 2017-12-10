#!/bin/sh
# Make sure you replace the API and/or APP key below
# with the ones for your account

api_key=<my_api_key>
app_key=<my_app_key>

from_time=$(date -v -1d +%s)

curl -G \
    "https://app.datadoghq.com/api/v1/metrics" \
    -d "api_key=${api_key}" \
    -d "application_key=${app_key}" \
    -d "from=${from_time}"  | jq '.' | cat
