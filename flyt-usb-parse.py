#!/usr/bin/env python

"""
Parse the output of lsusb to extract detailed information about
the alternate settings supported by USB Video Class compliant
devices.

Usage:
sudo lsusb -v | ./analyze-lsusb.py
-> converts the entire lsusb output to JSON

sudo lsusb -v | ./analyze-lsusb.py --json
sudo lsusb -v | ./analyze-lsusb.py --yaml
sudo lsusb -v | ./analyze-lsusb.py --txt
-> converts individual webcam entires into JSON/YAML/TXT,
   generating a file for each webcam found
"""

import json
import subprocess
import sys


ONE = 1
MANY = 2

arity = {
    "Device Descriptor": ONE,
    "Configuration Descriptor": MANY,
    "Interface Descriptor": MANY,
    "Endpoint Descriptor": MANY,
    "Hub Descriptor": ONE,
    " Hub Port Status": ONE,
    "Binary Object Store Descriptor": ONE,
    "USB 2.0 Extension Device Capability": ONE,
    "SuperSpeed USB Device Capability": ONE,
    "SuperSpeedPlus USB Device Capability": ONE,
    "Container ID Device Capability": ONE,
    "Interface Association": MANY,
    "VideoControl Interface Descriptor": MANY,
    "VideoStreaming Interface Descriptor": MANY,
    "AudioControl Interface Descriptor": MANY,
    "AudioStreaming Interface Descriptor": MANY,
    "AudioStreaming Endpoint Descriptor": MANY,
    "Device Qualifier (for other device speed)": ONE,
    "CDC Header": ONE,
    "CDC Union": ONE,
    "CDC Ethernet": ONE,
}


def split_nodes(lines):
    assert not lines[0].startswith("  ")
    nodes = []
    current_node = lines.pop(0)
    current_subnodes = []
    # The "END" is just a sentinel so that we don't have to make
    # a special case for the last entry in the list.
    for line in lines + ["END"]:
        if line.startswith("  "):
            current_subnodes.append(line[2:])
        else:
            # Hack to work around weird stuff with "HID Device Descriptor:"
            if current_node.startswith("iInterface"):
                current_subnodes = []
            if current_subnodes:
                current_node = [current_node, split_nodes(current_subnodes)]
            nodes.append(current_node)
            current_node = line
            current_subnodes = []
    return nodes


def make_tree(nodes):
    tree = {}
    for node in nodes:
        if type(node) == str:
            key, *maybe_value = node.split("  ", 1)
            tree[key] = maybe_value[0].strip() if maybe_value else True
        elif type(node) == list:
            assert len(node) == 2
            key = node[0]
            if (
                key.startswith("bm")
                or key.startswith("wHubCharacteristic")
                or key.startswith("wSpeedsSupported")
                or key.startswith("bFunctionalitySupport")
                or key.startswith("Device Status:")
                or key.startswith("bFlags")
                or key.startswith("wChannelConfig")
            ):
                # bitmasks
                node_arity = ONE
                key, raw_value = key.split(" ", 1)
                node[1].insert(0, "raw_value  " + raw_value.strip())
            elif key.endswith(":"):
                key = key[:-1]
                node_arity = arity[key]
            else:
                raise ValueError("Don't know how to handle group key: {}".format(key))
            if node_arity == ONE:
                assert key not in tree
                tree[key] = make_tree(node[1])
            else:  # arity[key] == MANY:
                if key not in tree:
                    tree[key] = []
                tree[key].append(make_tree(node[1]))
        else:
            raise ValueError("Wrong node type: {}".format(type(node)))
    return tree


def parse(device):
    lines = device.split("\n")
    lines = [line for line in lines if "Warning: Descriptor too short" not in line]
    assert lines[0].startswith("Bus")
    nodes = split_nodes(lines[1:])
    tree = make_tree(nodes)
    return tree






devices = []
# input_file = sys.stdin
input_file = subprocess.check_output("lsusb").encode()
for device in input_file.split("\n\n"):
    device = device.strip()
    tree = parse(device)
    devices.append(tree)


if len(sys.argv) == 1:
    json.dump(devices, sys.stdout)
    exit(0)


reports = []
for device in devices:
    descriptor = device["Device Descriptor"]
    interfaces = descriptor["Configuration Descriptor"][0]["Interface Descriptor"]
    interfaces = [
        i for i in interfaces if i["bInterfaceSubClass"] == "2 Video Streaming"
    ]
    if interfaces:
        report = {}
        reports.append(report)
        report["idVendor"] = descriptor["idVendor"]
        report["idProduct"] = descriptor["idProduct"]
        report["iProduct"] = descriptor["iProduct"]
        report["bcdUSB"] = descriptor["bcdUSB"]
        report["formats"] = []
        report["endpoints"] = []
        print("#{idVendor} - {idProduct}".format(**descriptor))
        for interface in interfaces:
            print("Alternate setting: {bAlternateSetting}".format(**interface))
            
            


for report in reports:
    basename = "devicereports/{}_{}_USB{}".format(
        report["idVendor"].split()[0],
        report["idProduct"].split()[0],
        report["bcdUSB"],
    )

print("## REPORT ")
print(report)
