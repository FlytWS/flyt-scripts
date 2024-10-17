#!/bin/bash

if [ ! -f /etc/flyt/data/serial ]; then

  lshwserial="lshw -class system | grep 'serial'"
  serial="${lshwserial//serial:}"
   
  # Set Serial In Serial File
  echo -n $serial | tee /etc/flyt/serial
  
fi
