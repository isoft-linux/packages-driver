#!/bin/sh

kernelver=$(uname -r)
rm -rf /etc/modprobe.d/nvidia-blacklist
dracut -f /boot/initrd-${kernelver}.img $kernelver
