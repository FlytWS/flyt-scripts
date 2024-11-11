import threading
import time
import subprocess



def boot():
    print('Boot')

    subprocess.call(["python3", "/etc/flyt/scripts/flyt-watchdog-services.py"])
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-clear.py"])
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-access-key.py"])
    subprocess.call(["bash", "/etc/flyt/scripts/flyt-serial.sh"])
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-wifi-scan.py"])
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-wifi-manage.py"])
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-wifi-active.py"])    
    #subprocess.call(["python3", "/etc/flyt/scripts/flyt-request.py"])  
    subprocess.call(["bash", "/etc/flyt/scripts/register-node.sh"])
    #subprocess.call(["python3", "/etc/flyt/scripts/flyt-watchdog-network.py"])
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-ecc-key.py"])
    subprocess.call(["python3", "/etc/flyt/scripts/flyt-angry-purple-tiger.py"])    



def t5seconds():
    while True:
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-stats-2.py"])
        time.sleep(5)



def t10seconds():
    while True:
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-gnss.py"])
        time.sleep(10)



def t30seconds():
    while True:
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-stats-1.py"])
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-services.py"])
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-usb.py"])
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-bandwidth.py"])
        time.sleep(30)


def t60seconds():
    while True:
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-health.py"])
        time.sleep(60)


def t300seconds():
    while True:
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-watchdog-services.py"])
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-stats-0.py"])
        time.sleep(300)


def t3600seconds():
    while True:
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-update-html.py"])
        subprocess.call(["python3", "/etc/flyt/scripts/flyt-update-scripts.py"])
        time.sleep(3600)


def t600seconds():
    while True:
        subprocess.call(["bash", "/etc/flyt/scripts/call-tower-gate.sh"])
        time.sleep(600)




time.sleep(5)

thread0 = threading.Thread(target=boot)
thread0.start()

time.sleep(30)

thread1 = threading.Thread(target=t5seconds)
thread1.start()

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