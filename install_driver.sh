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
    DRIVER="https://github.com/mozilla/geckodriver/releases/download/v0.20.0/geckodriver-v0.20.0-linux$ARCH.tar.gz"
    echo $DRIVER
}


mac_setup() {
    DRIVER="https://github.com/mozilla/geckodriver/releases/download/v0.20.0/geckodriver-v0.20.0-macos.tar.gz"
    echo $DRIVER
}

function driver_installation() {
    wget --no-check-certificate $1
    tar -xvzf geckodriver*
    chmod 755 geckodriver*
    sudo mv geckodriver /usr/local/bin/
    export PATH=$PATH:/usr/local/bin/geckodriver
    rm *.tar*
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
