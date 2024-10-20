import json
import subprocess

# Flyt Bandwidth


data = {}


# vnstat
try:
	stat = subprocess.check_output("vnstat", "--json")
	#data["vnstat"] = stat
except:
	print("Error "+str(IOError))
	pass


with open("/etc/flyt/data/flyt-bandwidth.json", "w") as file:
    file.write(stat)
