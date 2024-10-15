#!/bin/bash

model=`cat /etc/flyt/model`
serial=`cat /etc/flyt/serial`
accesskey=`cat /etc/flyt/accesskey`

url="https://tower.flyt.ws/registration.php?serial=$serial&model=$model&accesskey=$accesskey"
urlparsed="$( echo "$url" | sed 's/ /%20/g' )"
content=$(curl $urlparsed )
echo $content
