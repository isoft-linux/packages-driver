#!/bin/sh

kernelver=$(uname -r)

cp /usr/src/nvidia-blacklist /etc/modprobe.d/
dracut --omit-drivers "nouveau" -f /boot/initrd-${kernelver}.img $kernelver
