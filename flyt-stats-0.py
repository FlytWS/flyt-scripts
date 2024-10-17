import json
import psutil
import platform


# Stats Slow Cycle

data = {}


#Platform
try:
    uname = platform.uname()
    data["platform_system"] = uname.system
    data["platform_node"] = uname.node
    data["platform_release"] = uname.release
    data["platform_version"] = uname.version
    data["platform_machine"] = uname.machine
    data["platform_processor"] = uname.processor
except:
    print("Unable to read platform")



#CPU
try:
    data["cpu_cores"] = psutil.cpu_count(logical=False)
    cpufreq = psutil.cpu_freq()
    data["cpu_frequency_min"] = cpufreq.min
    data["cpu_frequency_max"] = cpufreq.max
    data["cpu_frequency_current"] = cpufreq.current
except:
    print("Unable to read cpu")

#RAM
try:
    svmem = psutil.virtual_memory()
    data["memory_total"] = svmem.total
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




#Network Counters
try:
    net_io = psutil.net_io_counters()
    data[f"network_counter_since_boot_bytes_sent"] = net_io.bytes_sent
    data[f"network_counter_since_boot_bytes_received"] = net_io.bytes_recv
except:
    print("Unable to read network counters")




# Storage Counters
try:
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    data[f"storage_counter_since_boot_bytes_read"] = disk_io.read_bytes
    data[f"storage_counter_since_boot_bytes_write"] = disk_io.write_bytes

except:
    print("Unable to read storage counters")



    
with open("/etc/flyt/data/flyt-stats-0.json", "w") as jsonFile:
    json.dump(data, jsonFile, ensure_ascii = False)