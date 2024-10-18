import subprocess
import os

# Flyt Clear

with open("/etc/flyt/data/flyt-stats-0.json", 'w+') as file:
    file.write("{}")

with open("/etc/flyt/data/flyt-stats-1.json", 'w+') as file:
    file.write("{}")    

with open("/etc/flyt/data/flyt-stats-2.json", 'w+') as file:
    file.write("{}")    

with open("/etc/flyt/data/flyt-gnss.json", 'w+') as file:
    file.write("{}")

if not os.path.exists("/etc/flyt/data/flyt-location.json"):
    with open("/etc/flyt/data/flyt-location.json", 'w+') as file:
        file.write("{}")

with open("/etc/flyt/data/flyt-bandwidth.json", 'w+') as file:
    file.write("{}")

with open("/etc/flyt/data/flyt-health.json", 'w+') as file:
    file.write("{}")

with open("/etc/flyt/data/flyt-network.json", 'w+') as file:
    file.write("{}")

with open("/etc/flyt/data/flyt-services.json", 'w+') as file:
    file.write("{}")    
    
with open("/etc/flyt/data/flyt-usb-parse.json", 'w+') as file:
    file.write("{}")
    
with open("/etc/flyt/data/flyt-usb-raw", 'w+') as file:
    file.write("")
    
with open("/etc/flyt/data/flyt-usb-dump", 'w+') as file:
    file.write("")
    
with open("/etc/flyt/data/flyt-usb", 'w+') as file:
    file.write("")

with open("/etc/flyt/data/flyt-wifi-scan.json", 'w+') as file:
    file.write("")

with open("/etc/flyt/data/flyt-wifi-manage.json", 'w+') as file:
    file.write("")

with open("/etc/flyt/data/flyt-wifi-active.json", 'w+') as file:
    file.write("")
    
with open("/etc/flyt/data/flyt-watchdog-network", 'w+') as file:
    file.write("")
    
subprocess.call(['chmod', '-R', '777', '/etc/flyt/data'])
