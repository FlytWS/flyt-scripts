import gpsd
import time
import json
import os

# Flyt GNSS

gpsdar = {}

try:
    # Connect to the local gpsd
    gpsd.connect()

    time.sleep(4)
    
    packet = None
    
    # Get gps position
    packet = gpsd.get_current()


    gpsdar['device']=gpsd.device()
    gpsdar['mode']=packet.mode
    if packet.sats > 0:
        gpsdar['satellites']=packet.sats
    else:
        gpsdar['satellites']=0

    if packet.mode >= 2:

        gpsdar['latitude']=str(packet.lat)
        gpsdar['longitude']=str(packet.lon)
        gpsdar['time']=str(packet.time)
        gpsdar['error']=packet.error
        gpsdar['position_precision']=str(packet.position_precision())


    if packet.mode >= 3:

        gpsdar['altitude']=str(packet.alt)


    if packet.lat == 0.0 and packet.lon == 0.0:
        gpsdar['latitude']=str('')
        gpsdar['longitude']=str('')


    #print(json.dumps(gpsdar))

    with open('/etc/flyt/data/flyt-gnss.json', 'w') as f:
        print(json.dumps(gpsdar), file=f)
    


except:

    print("GNSS Receiver Not Found")

    with open("/etc/flyt/data/flyt-gnss.json", 'w+') as file:
        file.write("{}")

    os.system('killall -KILL gpsd')
    os.system('systemctl restart gpsd') 