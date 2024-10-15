import threading
import time
import subprocess



def servicewatchdog():
    while True:
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




        time.sleep(300)



def boot():
    print('Boot')

    subprocess.call(["python3", "/etc/flyt/scripts/flyt-clear.py"])
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-access-key.py"])
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-serial.sh"])    
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-wifi-scan.py"])
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-wifi-manage.py"])
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-wifi-active.py"])    
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-request.py"])
    subprocess.call(["python3", "/etc/flyt/scripts/set-accesskey.sh"])    
    subprocess.call(["python3", "/etc/flyt/scripts/register-node.sh"])


def t10seconds():
    while True:
        print('T-10')
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-stats-2.py"])
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-gnss.py"])
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-wifi-manage.py"])
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-wifi-active.py"])
        time.sleep(10)



def t30seconds():
    while True:
        print('T-30')
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-stats-1.py"])
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-services.py"])
        #subprocess.call(["python3", "/etc/flyt/scripts/flyt-usb.py"])
        #subprocess.call(["python3", "/etc/flyt/scripts/get-stats-usb.sh"])
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-wifi-scan.py"])
        time.sleep(30)


def t60seconds():
    while True:
        print('T-60')
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-health.py"])
        time.sleep(60)


def t300seconds():
    while True:
        print('T-300')
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-stats-0.py"])
        time.sleep(300)


def t3600seconds():
    while True:
        print('T-3600')
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-update-html.py"])
        time.sleep(3600)


def t600seconds():
    while True:
        print('T-600')
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-update-html.py"])
        subprocess.call(["python3", "/etc/flyt/scripts/call-tower-gate.sh"])
        time.sleep(600)





thread0 = threading.Thread(target=boot)
thread0.start()

time.sleep(15)

thread1 = threading.Thread(target=servicewatchdog)
thread1.start()

time.sleep(30)

thread2 = threading.Thread(target=t10seconds)
thread2.start()

thread3 = threading.Thread(target=t30seconds)
thread3.start()

thread4 = threading.Thread(target=t300seconds)
thread4.start()

thread5 = threading.Thread(target=t3600seconds)
thread5.start()

thread6 = threading.Thread(target=t60seconds)
thread6.start()

thread7 = threading.Thread(target=t600seconds)
thread7.start()