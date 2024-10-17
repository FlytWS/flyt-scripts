import json
import subprocess


# Service Stats

data = {}

def check_service(service_name):
    try:
        output = subprocess.run(["systemctl", "status", service_name], capture_output=True)
        status = output.stdout.decode().strip()
        if "inactive" in status:
            data[service_name] = "inactive"
        else:
            data[service_name] = "running"
    except:
        data[service_name] = "notfound"


check_service("cron")
check_service("gpsd")
check_service("lm-sensors")
check_service("vnstat")
check_service("readsb")
check_service("vector")
check_service("tar1090")
check_service("graphs1090")



    
with open("/etc/flyt/data/flyt-services.json", "w") as jsonFile:
    json.dump(data, jsonFile)