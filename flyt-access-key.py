import json
import os
import random
import string
import time

print('Flyt Access Key')

# Flyt Access Key

def id_generator(size=48, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


if not os.path.exists("/etc/flyt/accesskey.json"):
    with open("/etc/flyt/accesskey.json", 'w') as file:
        file.write("{}")


with open("/etc/flyt/accesskey.json", "r") as jsonFile:
    data = json.load(jsonFile)


if "accesskey" in data:
    print ("Access Key Already Set")
else:
    timestamp = int(time.time())
    accesskey = id_generator()
    data["timestamp"] = timestamp
    data["accesskey"] = accesskey



with open("/etc/flyt/accesskey.json", "w") as jsonFile:
    json.dump(data, jsonFile)