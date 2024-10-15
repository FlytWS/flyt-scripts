# Service Watchdog
print('Starting Service Watchdog')

# cron
try:
    stat = subprocess.call(["systemctl", "is-active", "--quiet", "cron"])
    if(stat == 0):
        print("cron is active")
    else:
        print ("Starting cron")
        subprocess.call(["systemctl", "start", "cron"])
except:
    print("Error "+str(IOError))
    pass



# php8.2-fpm
try:
    stat = subprocess.call(["systemctl", "is-active", "--quiet", "php8.2-fpm"])
    if(stat == 0):
        print("php8.2-fpm is active")
    else:
        print ("Starting php8.2-fpm")
        subprocess.call(["systemctl", "start", "php8.2-fpm"])
except:
    print("Error "+str(IOError))
    pass


# nginx
try:
    stat = subprocess.call(["systemctl", "is-active", "--quiet", "nginx"])
    if(stat == 0):
        print("nginx is active")
    else:
        print ("Starting nginx")
        subprocess.call(["systemctl", "start", "nginx"])
except:
    print("Error "+str(IOError))
    pass



# gpsd
try:
    stat = subprocess.call(["systemctl", "is-active", "--quiet", "gpsd"])
    if(stat == 0):
        print("gpsd is active")
    else:
        print ("Starting gpsd")
        subprocess.call(["systemctl", "start", "gpsd"])
except:
    print("Error "+str(IOError))
    pass



# lm-sensors
try:
    stat = subprocess.call(["systemctl", "is-active", "--quiet", "lm-sensors"])
    if(stat == 0):
        print("lm-sensors is active")
    else:
        print ("Starting lm-sensors")
        subprocess.call(["systemctl", "start", "lm-sensors"])
except:
    print("Error "+str(IOError))
    pass



# vnstat
try:
    stat = subprocess.call(["systemctl", "is-active", "--quiet", "vnstat"])
    if(stat == 0):
        print("vnstat is active")
    else:
        print ("Starting vnstat")
        subprocess.call(["systemctl", "start", "vnstat"])
except:
    print("Error "+str(IOError))
    pass