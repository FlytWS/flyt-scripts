#!/usr/bin/python3

import subprocess

result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'device', 'wifi', 'list', '--rescan', 'yes'], capture_output=True, text=True)

# Check if the command was successful
if result.returncode == 0:
    # Save the output to a file
    with open('/etc/flyt/data/flyt-wifi-scan.json', 'w') as file:
        file.write(result.stdout)
else:
    print("Failed to list Wi-Fi networks. Error:", result.stderr)