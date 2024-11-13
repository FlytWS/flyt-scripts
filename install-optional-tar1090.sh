#!/bin/bash
# shellcheck shell=bash disable=SC2016


#wget -O tar1090-install.sh https://raw.githubusercontent.com/wiedehopf/tar1090/master/install.sh
#bash tar1090-install.sh /run/readsb


umask 022


set -e
trap 'echo "[ERROR] Error in line $LINENO when executing: $BASH_COMMAND"' ERR
renice 10 $$

srcdir=/run/readsb
nginx=yes
repo="https://github.com/wiedehopf/tar1090"
db_repo="https://github.com/wiedehopf/tar1090-db"
ipath=/usr/local/share/tar1090




function useSystemd () { command -v systemctl &>/dev/null; }

gpath="$TAR1090_UPDATE_DIR"
if [[ -z "$gpath" ]]; then gpath="$ipath"; fi

mkdir -p "$ipath"
mkdir -p "$gpath"

if useSystemd && ! id -u tar1090 &>/dev/null
then
    adduser --system --home "$ipath" --no-create-home --quiet tar1090 || adduser --system --home-dir "$ipath" --no-create-home tar1090
fi

# terminate with /
command_package="git git/jq jq/curl curl"
packages=()

while read -r -d '/' CMD PKG
do
    if ! command -v "$CMD" &>/dev/null
    then
        #echo "command $CMD not found, will try to install package $PKG"
        packages+=("$PKG")
    fi
done < <(echo "$command_package")

if [[ -n "${packages[*]}" ]]; then
    if ! command -v "apt-get" &>/dev/null; then
        echo "Please install the following packages and rerun the install:"
        echo "${packages[*]}"
        exit 1
    fi
    echo "Installing required packages: ${packages[*]}"
    if ! apt-get install -y --no-install-suggests --no-install-recommends "${packages[@]}"; then
        apt-get update || true
        apt-get install -y --no-install-suggests --no-install-recommends "${packages[@]}" || true
    fi
    hash -r || true
    while read -r -d '/' CMD PKG
    do
        if ! command -v "$CMD" &>/dev/null
        then
            echo "command $CMD not found, seems we failed to install package $PKG"
            echo "FATAL: Exiting!"
            exit 1
        fi
    done < <(echo "$command_package")
fi




dir=$(pwd)

if (( $( { du -s "$gpath/git-db" 2>/dev/null || echo 0; } | cut -f1) > 150000 )); then
    rm -rf "$gpath/git-db"
fi

function copyNoClobber() {
    if ! [[ -f "$2" ]]; then
        cp "$1" "$2"
    fi
}

function getGIT() {
    # getGIT $REPO $BRANCH $TARGET (directory)
    if [[ -z "$1" ]] || [[ -z "$2" ]] || [[ -z "$3" ]]; then echo "getGIT wrong usage, check your script or tell the author!" 1>&2; return 1; fi
    REPO="$1"; BRANCH="$2"; TARGET="$3"; pushd . >/dev/null
    if cd "$TARGET" &>/dev/null && git fetch --depth 1 origin "$BRANCH" 2>/dev/null && git reset --hard FETCH_HEAD; then popd >/dev/null && return 0; fi
    if ! cd /tmp || ! rm -rf "$TARGET"; then popd > /dev/null; return 1; fi
    if git clone --depth 1 --single-branch --branch "$BRANCH" "$REPO" "$TARGET"; then popd > /dev/null; return 0; fi
    rm -rf "$TARGET"; tmp=/tmp/getGIT-tmp-tar1090
    if wget -O "$tmp" "$REPO/archive/refs/heads/$BRANCH.zip" && unzip "$tmp" -d "$tmp.folder" >/dev/null; then
        if mv -fT "$tmp.folder/$(ls "$tmp.folder")" "$TARGET"; then rm -rf "$tmp" "$tmp.folder"; popd > /dev/null; return 0; fi
    fi
    rm -rf "$tmp" "$tmp.folder"; popd > /dev/null; return 1;
}
function revision() {
    git rev-parse --short HEAD 2>/dev/null || echo "$RANDOM-$RANDOM"
}

if ! { [[ "$1" == "test" ]] && cd "$gpath/git-db"; }; then
    DB_VERSION_NEW=$(curl --silent --show-error "https://raw.githubusercontent.com/wiedehopf/tar1090-db/master/version")
    if  [[ "$(cat "$gpath/git-db/version" 2>/dev/null)" != "$DB_VERSION_NEW" ]]; then
        getGIT "$db_repo" "master" "$gpath/git-db" || true
    fi
fi

if ! cd "$gpath/git-db"
then
    echo "Unable to download files, exiting! (Maybe try again?)"
    exit 1
fi

DB_VERSION=$(revision)

cd "$dir"


VERSION_NEW=$(curl --silent --show-error "https://raw.githubusercontent.com/wiedehopf/tar1090/master/version")
if  [[ "$(cat "$gpath/git/version" 2>/dev/null)" != "$VERSION_NEW" ]]; then
	if ! getGIT "$repo" "master" "$gpath/git"; then
		echo "Unable to download files, exiting! (Maybe try again?)"
		exit 1
	fi
fi
if ! cd "$gpath/git"; then
	echo "Unable to download files, exiting! (Maybe try again?)"
	exit 1
fi
TAR_VERSION="$(cat version)"




instances="$srcdir tar1090"
instances=$(echo -e "$instances" | grep -v -e '^#')


if ! diff tar1090.sh "$ipath"/tar1090.sh &>/dev/null; then
    changed=yes
    while read -r srcdir instance; do
        if [[ -z "$srcdir" || -z "$instance" ]]; then
            continue
        fi

        if [[ "$instance" != "tar1090" ]]; then
            service="tar1090-$instance"
        else
            service="tar1090"
        fi
        if useSystemd; then
            systemctl stop "$service" 2>/dev/null || true
        fi
    done < <(echo "$instances")
    rm -f "$ipath"/tar1090.sh
    cp tar1090.sh "$ipath"
fi


# copy over base files
cp install.sh uninstall.sh getupintheair.sh LICENSE README.md "$ipath"
cp default "$ipath/example_config_dont_edit"
cp html/config.js "$ipath/example_config.js"
rm -f "$ipath/default"

# create 95-tar1090-otherport.conf
{
    echo '# serve tar1090 directly on port 8504'
    echo '$SERVER["socket"] == ":8504" {'
    cat 88-tar1090.conf
    echo '}'
} > 95-tar1090-otherport.conf

services=()
names=""
otherport=""

while read -r srcdir instance
do
    if [[ -z "$srcdir" || -z "$instance" ]]; then
        continue
    fi
    TMP="$ipath/.instance_tmp"
    rm -rf "$TMP"
    mkdir -p "$TMP"
    chmod 755 "$TMP"

    if [[ "$instance" != "tar1090" ]]; then
        html_path="$ipath/html-$instance"
        service="tar1090-$instance"
    else
        html_path="$ipath/html"
        service="tar1090"
    fi
    services+=("$service")
    names+="$instance "

    # don't overwrite existing configuration
    useSystemd && copyNoClobber default /etc/default/"$service"

    sed -i.orig -e "s?SOURCE_DIR?$srcdir?g" -e "s?SERVICE?${service}?g" \
        -e "s?/INSTANCE??g" -e "s?HTMLPATH?$html_path?g" 95-tar1090-otherport.conf

    if [[ "$instance" == "webroot" ]]; then
        sed -i.orig -e "s?SOURCE_DIR?$srcdir?g" -e "s?SERVICE?${service}?g" \
            -e "s?/INSTANCE??g" -e "s?HTMLPATH?$html_path?g" 88-tar1090.conf
        sed -i.orig -e "s?SOURCE_DIR?$srcdir?g" -e "s?SERVICE?${service}?g" \
            -e "s?/INSTANCE/?/?g" -e "s?HTMLPATH?$html_path?g" nginx.conf
        sed -i -e "s?/INSTANCE?/?g" nginx.conf
    else
        sed -i.orig -e "s?SOURCE_DIR?$srcdir?g" -e "s?SERVICE?${service}?g" \
            -e "s?INSTANCE?$instance?g" -e "s?HTMLPATH?$html_path?g" 88-tar1090.conf
        sed -i.orig -e "s?SOURCE_DIR?$srcdir?g" -e "s?SERVICE?${service}?g" \
            -e "s?INSTANCE?$instance?g" -e "s?HTMLPATH?$html_path?g" nginx.conf
    fi



    sed -i.orig -e "s?SOURCE_DIR?$srcdir?g" -e "s?SERVICE?${service}?g" tar1090.service

    cp -r -T html "$TMP"
    cp -r -T "$gpath/git-db/db" "$TMP/db-$DB_VERSION"
    sed -i -e "s/let databaseFolder = .*;/let databaseFolder = \"db-$DB_VERSION\";/" "$TMP/index.html"
    echo "{ \"tar1090Version\": \"$TAR_VERSION\", \"databaseVersion\": \"$DB_VERSION\" }" > "$TMP/version.json"

    # keep some stuff around
    mv "$html_path/config.js" "$TMP/config.js" 2>/dev/null || true
    mv "$html_path/upintheair.json" "$TMP/upintheair.json" 2>/dev/null || true

    # in case we have offlinemaps installed, modify config.js
    MAX_OFFLINE=""
    for i in {0..15}; do
        if [[ -d /usr/local/share/osm_tiles_offline/$i ]]; then
            MAX_OFFLINE=$i
        fi
    done
    if [[ -n "$MAX_OFFLINE" ]]; then
        if ! grep "$TMP/config.js" -e '^offlineMapDetail.*' -qs &>/dev/null; then
            echo "offlineMapDetail=$MAX_OFFLINE;" >> "$TMP/config.js"
        else
            sed -i -e "s/^offlineMapDetail.*/offlineMapDetail=$MAX_OFFLINE;/" "$TMP/config.js"
        fi
    fi

    cp "$ipath/customIcon.png" "$TMP/images/tar1090-favicon.png" &>/dev/null || true

    # bust cache for all css and js files

    dir=$(pwd)
    cd "$TMP"

    sed -i -e "s/tar1090 on github/tar1090 on github (${TAR_VERSION})/" index.html

    "$gpath/git/cachebust.sh" "$gpath/git/cachebust.list" "$TMP"

    rm -rf "$html_path"
    mv "$TMP" "$html_path"

    cd "$dir"

    cp nginx.conf "$ipath/nginx-${service}.conf"


    if useSystemd; then
        if [[ $changed == yes ]] || ! diff tar1090.service /lib/systemd/system/"${service}".service &>/dev/null
        then
            cp tar1090.service /lib/systemd/system/"${service}".service
            if systemctl enable "${service}"
            then
                echo "Restarting ${service} ..."
                systemctl restart "$service" || ! pgrep systemd
            else
                echo "${service}.service is masked, could not start it!"
            fi
        fi
    fi

    # restore sed modified configuration files
    mv 88-tar1090.conf.orig 88-tar1090.conf
    mv 95-tar1090-otherport.conf.orig 95-tar1090-otherport.conf
    mv nginx.conf.orig nginx.conf
    mv tar1090.service.orig tar1090.service
done < <(echo "$instances")








systemctl restart nginx

for name in $names; do
	echo "All done! Tar1090 is available at http://$(ip route get 1.2.3.4 | grep -m1 -o -P 'src \K[0-9,.]*')/$name"
done