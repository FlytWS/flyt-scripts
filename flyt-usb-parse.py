#!/usr/bin/env python

import json
import subprocess
import sys


def split_nodes(lines):
    assert not lines[0].startswith("  ")
    nodes = []
    current_node = lines.pop(0)
    current_subnodes = []
    for line in lines + ["END"]:
        if line.startswith("  "):
            current_subnodes.append(line[2:])
        else:
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
input_file = subprocess.check_output("lsusb").decode()
for device in input_file.split("\n\n"):
    device = device.strip()
    tree = parse(device)
    devices.append(tree)



#json.dump(devices, sys.stdout)

with open("/etc/flyt/data/flyt-usb-parse.json", "w") as jsonFile:
    json.dump(devices, jsonFile)