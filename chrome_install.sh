#!/bin/bash

set -e

get_arch() {
    ARCH=$(uname -m)
    if [ $ARCH == 'x86_64' ]; then
        return 64
    else
        return 32
    fi
}

linux_setup() {
    get_arch
    local ARCH="$?"
    if [ $ARCH -eq 64 ];then
        DRIVER="http://chromedriver.storage.googleapis.com/2.4/chromedriver_linux$ARCH.zip"
    else 
        DRIVER="http://chromedriver.storage.googleapis.com/2.10/chromedriver_linux$ARCH.zip"
    fi
    echo $DRIVER
}


mac_setup() {
    get_arch
    local ARCH="$?"
    if [ $ARCH -eq 64 ];then
        DRIVER="http://chromedriver.storage.googleapis.com/2.37/chromedriver_mac$ARCH.zip"
    else 
        DRIVER="http://chromedriver.storage.googleapis.com/2.10/chromedriver_mac$ARCH.zip"
    fi
    echo $DRIVER
}

function driver_installation() {
    wget --no-check-certificate -N $1
    sudo unzip chromedriver*
    chmod 755 chromedriver*
    sudo mv chromedriver /usr/local/bin/
    export PATH=$PATH:/usr/local/bin/chromedriver
    rm *.zip
}

main() {
    # uname -o does not exist on MacOSX. 
    uname -o >/dev/null 2>&1
    OUT="$?"

    if [ $OUT -eq 0 ]; then
        local INSTALL=$(linux_setup)
    else
        local INSTALL=$(mac_setup)
    fi
    echo $INSTALL
    driver_installation $INSTALL
}

main || exit 1
exit 0
