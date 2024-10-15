import json
import subprocess


# Flyt Services

with open("/etc/flyt/data/flyt-services.json", "r") as jsonFile:
    data = json.load(jsonFile)


# cron
try:
	stat = subprocess.check_output(["systemctl", "show", "cron", "-p", "ActiveState"], text=True)
	data["cron"] = stat
except:
	data["cron"] = "NotFound"
	pass



# lm-sensors
try:
	stat = subprocess.check_output(["systemctl", "show", "lm-sensors", "-p", "ActiveState"], text=True)
	data["lm-sensors"] = stat
except:
	data["lm-sensors"] = "NotFound"
	pass



# vnstat
try:
	stat = subprocess.check_output(["systemctl", "show", "vnstat", "-p", "ActiveState"], text=True)
	data["vnstat"] = stat
except:
	data["vnstat"] = "NotFound"
	pass



# php8.2-fpm
try:
	stat = subprocess.check_output(["systemctl", "show", "php8.2-fpm", "-p", "ActiveState"], text=True)
	data["php8.2-fpm"] = stat
except:
	data["php8.2-fpm"] = "NotFound"
	pass


# nginx
try:
	stat = subprocess.check_output(["systemctl", "show", "nginx", "-p", "ActiveState"], text=True)
	data["nginx"] = stat
except:
	data["nginx"] = "NotFound"
	pass


# readsb
try:
	stat = subprocess.check_output(["systemctl", "show", "readsb", "-p", "ActiveState"], text=True)
	data["readsb"] = stat
except:
	data["readsb"] = "NotFound"
	pass


# vector
try:
	stat = subprocess.check_output(["systemctl", "show", "vector", "-p", "ActiveState"], text=True)
	data["vector"] = stat
except:
	data["vector"] = "NotFound"
	pass


# tar1090
try:
	stat = subprocess.check_output(["systemctl", "show", "tar1090", "-p", "ActiveState"], text=True)
	data["tar1090"] = stat
except:
	data["tar1090"] = "NotFound"
	pass


# graphs1090
try:
	stat = subprocess.check_output(["systemctl", "show", "graphs1090", "-p", "ActiveState"], text=True)
	data["graphs1090"] = stat
except:
	data["graphs1090"] = "NotFound"
	pass




with open("/etc/flyt/data/flyt-services.json", "w") as jsonFile:
    json.dump(data, jsonFile)
