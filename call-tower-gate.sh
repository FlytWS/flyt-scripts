#!/bin/bash

serial=`cat /etc/flyt/data/serial`
model=`cat /etc/flyt/model`
accesskey=`cat /etc/flyt/data/accesskey`
location=`cat /etc/flyt/data/location`
antennaid=`cat /etc/flyt/data/wingbits`
statsnetwork=`cat /var/www/html/flyt-data/stats_network.json`
statshost=`cat /var/www/html/flyt-data/stats_host.json`


generate_post_data()
{
  cat <<EOF
{
  "serial": "$serial",
  "accesskey": "$accesskey",
  "model": "$model",
  "antennaid": "$antennaid",
  "location": $location,
  "statsnetwork": $statsnetwork,
  "statshost": $statshost
}
EOF
}

echo -n $(curl -H 'Content-Type: application/json' -X POST https://tower.flyt.ws/gate.php -d "$(generate_post_data)")
