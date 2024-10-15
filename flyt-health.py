import json

# Flyt Health

with open("/etc/flyt/data/flyt-health.json", "r") as jsonFile:
    data = json.load(jsonFile)


## Consider doing this in hmtl/php only as script difficult to
# update for new USB devices
data["radio"] = ""
data["network"] = ""
data["temperature"] = ""
data["activity"] = ""
data["node"] = ""
data["gnss"] = ""


with open("/etc/flyt/data/flyt-health.json", "w") as jsonFile:
    json.dump(data, jsonFile)
