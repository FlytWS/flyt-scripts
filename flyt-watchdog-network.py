import os
import time
import subprocess

print('Flyt Watchdog Network')

def detect_file_changes(file_path, interval=1):
    last_modified = os.path.getmtime(file_path)
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            print("Activated Flyt Watchdog Network")
            subprocess.call(["python3", "/etc/flyt/scripts/flyt-stats-1.py"])
            last_modified = current_modified
        time.sleep(interval)


detect_file_changes("/etc/flyt/data/flyt-watchdog-network")