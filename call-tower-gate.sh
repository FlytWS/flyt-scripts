#!/bin/bash

serial=`cat /etc/flyt/serial`
model=`cat /etc/flyt/model`
accesskey=`cat /etc/flyt/accesskey`
location=`cat /etc/flyt/data/flyt-location.json`
antennaid=`cat /etc/flyt/wingbits`


generate_post_data()
{
  cat <<EOF
{
  "serial": "$serial",
  "accesskey": "$accesskey",
  "model": "$model",
  "antennaid": "$antennaid",
  "location": $location
}
EOF
}

echo -n $(curl -H 'Content-Type: application/json' -X POST https://tower.flyt.ws/gate.php -d "$(generate_post_data)")
