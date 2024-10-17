import json
import psutil


# Stats Fast Cycle

data = {}


#Boot
try:
    data["boot_timestamp"] = psutil.boot_time()
except:
    print("Unable to read boot")

    

#CPU
try:
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            data[f"cpu_usage_percent_core_{i}"] = percentage
    data["cpu_usage_percent"] = psutil.cpu_percent()
except:
    print("Unable to read cpu")


#RAM
try:
    svmem = psutil.virtual_memory()
    data["memory_available"] = svmem.available
    data["memory_used"] = svmem.used
    data["memory_percent"] = svmem.percent
except:
    print("Unable to read ram")


#SWAP
try:
    swap = psutil.swap_memory()
    data["swap_total"] = swap.total
    data["swap_available"] = swap.free
    data["swap_used"] = swap.used
    data["swap_percent"] = swap.percent
except:
    print("Unable to read swap")


#Network
try:
    net_io = psutil.net_io_counters()
    data[f"network_counter_since_boot_bytes_sent"] = net_io.bytes_sent
    data[f"network_counter_since_boot_bytes_received"] = net_io.bytes_recv
except:
    print("Unable to read network")



# Get IO statistics since boot
try:
    disk_io = psutil.disk_io_counters()
    data[f"storage_counter_since_boot_bytes_read"] = disk_io.read_bytes
    data[f"storage_counter_since_boot_bytes_write"] = disk_io.write_bytes
except:
    print("Unable to read storage")




    
with open("/etc/flyt/data/flyt-stats-2.json", "w") as jsonFile:
    json.dump(data, jsonFile, ensure_ascii = False)