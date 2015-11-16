#!/bin/sh

#
# This shell script downloads and installs firmware for the Terratec
# DMX 6Fire USB. See fwinst.txt for more information.
#
# Windows driver version used: 1.11.0.19
#
# Author:    Torsten Schenk
# Copyright: (C) Torsten Schenk
#
# Thanks:
# - Richard Lucassen: he fixed minor bugs in this script and
#                     helped fixing 7z version problems
#
# This script is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#

export FW_PATH=/lib/firmware
export FW_6FIRE_PATH=$FW_PATH/6fire
cleanup() {
  rm -Rf /tmp/dmx
  rm -f /tmp/dmx.exe
  rm -f /tmp/dmx.tmp
  rm -f /tmp/dmx6firel2.ihx
  rm -f /tmp/dmx6fireap.ihx
  rm -f /tmp/dmx6firecf.bin
}

success() {
  echo -e "\033[1;32m$1\033[m"
  cleanup
  exit
}

step_begin() {
  echo -e -n "\033[1;33m$1...\033[m"
}

step_error() {
  echo -e "\033[1;33mfailed.\033[0m"
  echo -e "\033[1;31m$1\033[0m"
  cleanup
  exit
}

step_success() {
  echo -e "\033[1;33mdone.\033[m"
}

step_begin "Checking for firmware directory"
if ! [ -d $FW_PATH ]; then
  step_error "Firmware directory\n  $FW_PATH\ndoes not exist.\n\nEither you have no firmware installed or your system uses another directory.\nPlease set FW_PATH in this script file accordingly.\nTypical paths you could try are:\n  /lib/firmware\n  /usr/lib/hotplug/firmware\n\nIf you nevertheless want to install the firmware into this path,\nplease create it manually:\n  $ sudo mkdir -p $FW_PATH\nor, if you are root:\n  $ mkdir -p $FW_PATH"
fi
step_success

step_begin "Downloading windows driver"
if ! wget "http://ftp.terratec.de/Audio/DMX_6fire_USB/Updates/DMX_6fire_USB_Setup_1.23.0.02_XP_Vista_7.exe" -q -O /tmp/dmx.exe ; then
  step_error "Internet connection alive? Perhaps a new driver version is available.\nIf that is the case, please redownload this script."
fi
step_success

step_begin "Checking MD-5 checksum of windows driver"
if ! echo "86049155f9326a77329d87f7b027a8b9  /tmp/dmx.exe" | md5sum -c >/dev/null 2>&1 ; then
  step_error "Downloaded windows driver has wrong MD-5 checksum."
fi
step_success

step_begin "Unpacking windows driver"
if ! mkdir /tmp/dmx ; then
  step_error "Cannot create temporary directory /tmp/dmx."
fi

if ! 7z x -aot -o/tmp/dmx /tmp/dmx.exe >/dev/null 2>&1 ; then
  step_error "Is 7z installed?"
fi
step_success

step_begin "Extracting firmware files"
if ! cp '/tmp/dmx/$[153]/$[153]/$[154]_17' /tmp/dmx6fireap.ihx ; then
  step_error "Extraction of file 'dmx6fireap.ihx' failed."
fi

if ! cp '/tmp/dmx/$[153]/$[153]/$[154]_18' /tmp/dmx6firecf.bin >/dev/null 2>&1 ; then
  step_error "Extraction of file 'dmx6firecf.bin' failed."
fi

if ! cp '/tmp/dmx/$[153]/$[153]/$[154]_16' /tmp/dmx6firel2.ihx >/dev/null 2>&1 ; then
  step_error "Extraction of file 'dmx6firel2.ihx' failed."
fi
step_success

step_begin "Checking MD-5 checksums of firmware files"
if ! echo "fa80973cb8c02097712933bd1d1c23b2  /tmp/dmx6firel2.ihx" | md5sum -c >/dev/null 2>&1 ; then
  step_error "File 'dmx6firel2.ihx' has wrong MD-5 checksum."
fi

if ! echo "7497b6b80d43e68f13b6929934ab60f4  /tmp/dmx6fireap.ihx" | md5sum -c >/dev/null 2>&1; then
  step_error "File 'dmx6fireap.ihx' has wrong MD-5 checksum."
fi

if ! echo "a65eecc11adc87af7307f5266ad31d65  /tmp/dmx6firecf.bin" | md5sum -c >/dev/null 2>&1 ; then
  step_error "File 'dmx6firecf.bin' has wrong MD-5 checksum."
fi
step_success

step_begin "Installing firmware files"
if ! mkdir -p $FW_6FIRE_PATH >/dev/null 2>&1 ; then
  step_error "Creation of firmware path failed. Are you root?"
fi

if ! cp /tmp/dmx6firel2.ihx $FW_6FIRE_PATH >/dev/null 2>&1 ; then
  step_error "Installation of file 'dmx6firel2.ihx' failed. Are you root?"
fi

if ! cp /tmp/dmx6fireap.ihx $FW_6FIRE_PATH >/dev/null 2>&1 ; then
  step_error "Installation of file 'dmx6fireap.ihx' failed. Are you root?"
fi

if ! cp /tmp/dmx6firecf.bin $FW_6FIRE_PATH >/dev/null 2>&1 ; then
  step_error "Installation of file 'dmx6firecf.bin' failed. Are you root?"
fi
step_success

success "Installation completed."

