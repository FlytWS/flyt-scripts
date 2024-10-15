import subprocess

# Flyt Clear

with open("/etc/flyt/data/flyt-stats-0.json", 'w+') as file:
    file.write("{}")

with open("/etc/flyt/data/flyt-stats-1.json", 'w+') as file:
    file.write("{}")    

with open("/etc/flyt/data/flyt-stats-2.json", 'w+') as file:
    file.write("{}")    

with open("/etc/flyt/data/flyt-gnss.json", 'w+') as file:
    file.write("{}")

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
    
with open("/etc/flyt/data/flyt-usb.json", 'w+') as file:
    file.write("{}")    
    
with open("/etc/flyt/data/flyt-usb", 'w+') as file:
    file.write("")

with open("/etc/flyt/data/flyt-wifi-scan.json", 'w+') as file:
    file.write("")

with open("/etc/flyt/data/flyt-wifi-manage.json", 'w+') as file:
    file.write("")

with open("/etc/flyt/data/flyt-wifi-active.json", 'w+') as file:
    file.write("")
    
    
subprocess.call(['chmod', '-R', '777', '/etc/flyt/data'])
subprocess.call(['chmod', '-R', '777', '/etc/flyt/scripts'])
