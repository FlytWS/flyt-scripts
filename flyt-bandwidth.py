import json
import subprocess

# Flyt Bandwidth


data = {}


# vnstat
try:
    output = subprocess.run(["vnstat", "--json"], capture_output=True)
    status = output.stdout.decode().strip()
    data['vnstat'] = status
	#data["vnstat"] = stat
except:
	print("Error "+str(IOError))
	pass


with open("/etc/flyt/data/flyt-bandwidth.json", "w") as jsonFile:
    json.dump(data, jsonFile)