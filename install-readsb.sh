#!/bin/bash

#curl -sL https://github.com/wiedehopf/adsb-scripts/raw/master/readsb-install.sh | bash
#sed -i -e 's|After=.*|After=vector.service|' /lib/systemd/system/readsb.service
#sed -i.bak 's/NET_OPTIONS="[^"]*/& '"--net-connector localhost,30006,json_out"'/' /etc/default/readsb
#systemctl daemon-reload
#systemctl restart readsb


repository="https://github.com/wiedehopf/readsb.git"

ipath=/usr/local/share/adsb-wiki/readsb-install
mkdir -p $ipath

function aptInstall() {
    if ! apt install -y --no-install-recommends --no-install-suggests "$@" &>/dev/null; then
        apt update
        if ! apt install -y --no-install-recommends --no-install-suggests "$@"; then
            apt clean -y || true
            apt --fix-broken install -y || true
            apt install --no-install-recommends --no-install-suggests -y $packages
        fi
    fi
}

if command -v apt &>/dev/null; then
    packages=(git gcc make libusb-1.0-0-dev librtlsdr-dev librtlsdr0 ncurses-dev ncurses-bin zlib1g-dev zlib1g)
    if ! grep -E 'wheezy|jessie' /etc/os-release -qs; then
        packages+=(libzstd-dev libzstd1)
    fi
    if ! command -v nginx &>/dev/null; then
        packages+=(lighttpd)
    fi
    aptInstall "${packages[@]}"
fi

udevadm control --reload-rules || true

function getGIT() {
    # getGIT $REPO $BRANCH $TARGET-DIR
    if [[ -z "$1" ]] || [[ -z "$2" ]] || [[ -z "$3" ]]; then
        echo "getGIT wrong usage, check your script or tell the author!" 1>&2
        return 1
    fi
    if ! cd "$3" &>/dev/null || ! git fetch --depth 2 origin "$2" || ! git reset --hard FETCH_HEAD; then
        if ! rm -rf "$3" || ! git clone --depth 2 --single-branch --branch "$2" "$1" "$3"; then
            return 1
        fi
    fi
    return 0
}
BRANCH="stale"
if ! getGIT "$repository" "$BRANCH" "$ipath/git"
then
    echo "Unable to git clone the repository"
    exit 1
fi

rm -rf "$ipath"/readsb*.deb
cd "$ipath/git"

make clean
THREADS=$(( $(grep -c ^processor /proc/cpuinfo) - 1 ))
THREADS=$(( THREADS > 0 ? THREADS : 1 ))
CFLAGS="-O2 -march=native"

# disable unaligned access for arm 32bit ...
if uname -m | grep -qs -e arm -e aarch64 && gcc -mno-unaligned-access hello.c -o /dev/null &>/dev/null; then
    CFLAGS+=" -mno-unaligned-access"
fi

make "-j${THREADS}" AIRCRAFT_HASH_BITS=16 RTLSDR=yes OPTIMIZE="$CFLAGS" "$@"

cp -f debian/readsb.service /lib/systemd/system/readsb.service

rm -f /usr/bin/readsb /usr/bin/viewadsb
cp -f readsb /usr/bin/readsb
cp -f viewadsb /usr/bin/viewadsb

cp -n debian/readsb.default /etc/default/readsb

if ! id -u readsb &>/dev/null
then
    adduser --system --home $ipath --no-create-home --quiet readsb || adduser --system --home-dir $ipath --no-create-home readsb
    adduser readsb plugdev || true # USB access
    adduser readsb dialout || true # serial access
fi



#systemctl enable readsb
#systemctl restart readsb || true
