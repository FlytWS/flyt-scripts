#!/usr/bin/env python

import json
import subprocess
import re


devices = []
device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb", universal_newlines=True)
for i in df.split('\n'):
    if i:
        _inf = device_re.match(i)
        if _inf:
            dinfo = _inf.groupdict()
            dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
            devices.append(dinfo)



with open("/etc/flyt/data/flyt-usb-raw", 'w+') as file:
    file.write(df)

with open("/etc/flyt/data/flyt-usb-parse.json", "w") as jsonFile:
    json.dump(devices, jsonFile)
    
    

dt = subprocess.check_output("usb-devices | cut -d: -f2", universal_newlines=True)

with open("/etc/flyt/data/flyt-usb-dump", 'w+') as file:
    file.write(dt)