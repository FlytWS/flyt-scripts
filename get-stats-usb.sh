#!/bin/bash

stat_usb=`usb-devices | cut -d: -f2`

cat > /etc/flyt/data/flyt-usb << EOL
$stat_usb
EOL
