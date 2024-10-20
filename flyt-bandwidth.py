import json
import subprocess

# Flyt Bandwidth

status = ""

try:
    output = subprocess.run(["vnstat", "--json"], capture_output=True)
    status = output.stdout.decode()
except:
	print("Error "+str(IOError))
	pass

with open("/etc/flyt/data/flyt-bandwidth.json", "w") as file:
    file.write(status)