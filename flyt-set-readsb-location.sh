#!/bin/bash

lat=$1
lon=$2

sh /etc/flyt/scripts/readsb-set-location.sh [$lat] [$lon]
