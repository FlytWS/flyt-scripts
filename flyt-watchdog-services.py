import subprocess

# Service Watchdog
print('Starting Service Watchdog')


def check_service(service_name):
    output = subprocess.run(["systemctl", "status", service_name], capture_output=True)
    status = output.stdout.decode().strip()
    if "inactive" in status:
        subprocess.run(["systemctl", "restart", service_name])
        print(f"{service_name} service has been restarted")
    else:
        print(f"{service_name} service is running")



check_service("cron")
check_service("php8.2-fpm")
check_service("nginx")
check_service("gpsd")
check_service("lm-sensors")
check_service("vnstat")