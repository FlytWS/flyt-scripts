#!/bin/bash

wget -O tar1090-install.sh https://raw.githubusercontent.com/wiedehopf/tar1090/master/install.sh
bash tar1090-install.sh /run/readsb
systemctl restart nginx