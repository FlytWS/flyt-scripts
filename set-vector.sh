#!/bin/bash

device_id=$1
hardware_sn=$2
access_key=$3

echo -n "$device_id" > /etc/wingbits/device

echo "DEVICE_ID=\"$device_id\"" > /etc/default/vector
echo "HARDWARE_SN=\"$hardware_sn\"" >> /etc/default/vector
echo "ACCESS_KEY=\"$access_key\"" >> /etc/default/vector

echo -n "$device_id" > /etc/flyt/wingbits

systemctl restart vector

cat /etc/flyt/wingbits
