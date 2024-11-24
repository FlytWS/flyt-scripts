import subprocess
import os

# Service Watchdog

def check_service(service_name):
    output = subprocess.run(["systemctl", "status", service_name], capture_output=True)
    status = output.stdout.decode().strip()
    if "inactive" in status:
        subprocess.run(["systemctl", "restart", service_name])
        print(f"{service_name} service has been restarted")


def check_service_pid(service_name, service_path):
    output = os.path.exists(service_path)
    if output == False:
        subprocess.run(["systemctl", "restart", service_name])
        print(f"{service_name} service has been restarted")


check_service("cron")
check_service("log2ram")
check_service("php8.2-fpm")
check_service("gpsd")
check_service("lm-sensors")
check_service("vnstat")
check_service("readsb")

check_service_pid("nginx", "/var/run/nginx.pid")