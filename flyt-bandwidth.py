import json
import subprocess

# Flyt Bandwidth


with open("/etc/flyt/data/flyt-bandwidth.json", "r") as jsonFile:
    data = json.load(jsonFile)


# vnstat
try:
	stat = subprocess.call(["vnstat", "--json"])
	data["vnstat"] = stat
except:
	print("Error "+str(IOError))
	pass



with open("/etc/flyt/data/flyt-bandwidth.json", "w") as jsonFile:
    json.dump(data, jsonFile)
