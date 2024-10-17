import json
import subprocess

# Flyt Bandwidth


data = {}


# vnstat
try:
	stat = subprocess.call(["vnstat", "--json"])
	data["vnstat"] = stat
except:
	print("Error "+str(IOError))
	pass


with open("/etc/flyt/data/flyt-bandwidth.json", "w") as jsonFile:
    json.dump(data, jsonFile)
