import json
import psutil


# Stats Medium Cycle

data = {}

#Temperature
try:
    if not hasattr(psutil, "sensors_temperatures"):
            print("Temperature Not Supported")
    else:
            temps = psutil.sensors_temperatures()
            if not temps:
                    #sys.exit("Unable To Read Any Temperature")
                    print("Unable to read temperature")
            for name, entries in temps.items():
                    for entry in entries:
                            data[f"temperature_label_{name}"] = entry.label or name
                            data[f"temperature_current_{name}"] = entry.current
                            data[f"temperature_high_{name}"] = entry.high
                            data[f"temperature_critical_{name}"] = entry.critical
except:
    print("Unable to read temperature")



#Network
try:
    d = psutil.net_if_addrs()
    for n in d.keys():
        for addr in d[n]:
            if addr.family == 2:
                netifaddrindex = "".join(n.split())
                data[f"network_label_{netifaddrindex}"] = n
                data[f"network_address_{netifaddrindex}"] = addr.address
                data[f"network_netmask_{netifaddrindex}"] = addr.netmask
                data[f"network_broadcast_{netifaddrindex}"] = addr.broadcast

except:
    print("Unable to read network")




# Storage
try:
    partitions = psutil.disk_partitions()
    for partition in partitions:

        data[f"storage_partition_device_{partition.device}"] = partition.device
        data[f"storage_partition_mountpoint_{partition.device}"] = partition.mountpoint
        data[f"storage_partition_filesystem_{partition.device}"] = partition.fstype
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        data[f"storage_usage_total_{partition.device}"] = partition_usage.total
        data[f"storage_usage_used_{partition.device}"] = partition_usage.used
        data[f"storage_usage_free_{partition.device}"] = partition_usage.free
        data[f"storage_usage_percentage_{partition.device}"] = partition_usage.percent
        
except:
    print("Unable to read storage")




with open("/etc/flyt/data/flyt-stats-1.json", "w") as jsonFile:
    json.dump(data, jsonFile, ensure_ascii = False)