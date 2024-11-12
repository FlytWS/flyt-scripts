#!/usr/bin/env python

import os
import json


# Flyt System Variables

data = {}

try:
    data["flyt_core_version"] = os.environ['FLYT_CORE_VERSION']
except:
    print("Unable to read FLYTCOREVERSION")


try:
    data["flyt_device_name"] = os.environ['BALENA_DEVICE_NAME_AT_INIT']
except:
    print("Unable to read BALENA_DEVICE_NAME_AT_INIT")


try:
    data["flyt_host_os"] = os.environ['BALENA_HOST_OS_VERSION']
except:
    print("Unable to read BALENA_HOST_OS_VERSION")

    

with open("/etc/flyt/data/flyt-system-variables.json", "w") as jsonFile:
    json.dump(data, jsonFile, ensure_ascii = False)