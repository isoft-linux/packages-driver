%global        _nvidia_serie       nvidia
%global        _nvidia_libdir      %{_libdir}/%{_nvidia_serie}
%global        _nvidia_xorgdir     %{_nvidia_libdir}/xorg

%global	       debug_package %{nil}
%global	       __strip /bin/true

Name:            xorg-x11-drv-nvidia
Epoch:           1
Version:         352.63
Release:         5
Summary:         NVIDIA's proprietary display driver for NVIDIA graphic cards

Group:           User Interface/X Hardware Support
License:         Redistributable, no modification permitted
URL:             http://www.nvidia.com/
Source1:         ftp://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-no-compat32.run
Source2:         99-nvidia.conf
Source3:         nvidia-xorg.conf
Source5:         00-avoid-glamor.conf
Source6:         blacklist-nouveau.conf
Source7:         alternate-install-present
Source8:         00-ignoreabi.conf
Source9:         nvidia-settings.desktop
Source10:        nvidia.conf
Source11:        nvidia-dkms.conf
Source12:        pre_build.sh
Source13:        post_install.sh
#Patch0: 	 nvidia-settings.patch
Patch1: 	 nvidia-settings2.patch

ExclusiveArch: x86_64

BuildRequires:   desktop-file-utils
Buildrequires:   systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires(post):   ldconfig
Requires(postun): ldconfig
#Requires(post):   grubby
Requires:        which

Requires:        %{name}-libs%{_isa} = %{?epoch}:%{version}-%{release}

Obsoletes:       %{_nvidia_serie}-kmod < %{?epoch}:%{version}
Provides:        %{_nvidia_serie}-kmod-common = %{?epoch}:%{version}
Conflicts:       xorg-x11-drv-nvidia-beta
Conflicts:       xorg-x11-drv-nvidia-legacy
Conflicts:       xorg-x11-drv-nvidia-71xx
Conflicts:       xorg-x11-drv-nvidia-96xx
Conflicts:       xorg-x11-drv-nvidia-173xx
Conflicts:       xorg-x11-drv-nvidia-304xx
Conflicts:       xorg-x11-drv-nvidia-340xx
Conflicts:       xorg-x11-drv-nvidia-340xx
Conflicts:       xorg-x11-drv-fglrx
Conflicts:       xorg-x11-drv-catalyst

%global         __provides_exclude ^(lib.*GL.*\\.so.*|libOpenCL\\.so.*)$
%global         __requires_exclude ^(lib.*GL.*\\.so.*|libOpenCL\\.so.*)$

%description
This package provides the most recent NVIDIA display driver which allows for
hardware accelerated rendering with current NVIDIA chipsets series.
GF8x, GF9x, and GT2xx GPUs NOT supported by this release.

For the full product support list, please consult the release notes
http://download.nvidia.com/XFree86/Linux-x86/%{version}/README/index.html

Please use the following documentation:
http://rpmfusion.org/Howto/nVidia


%package devel
Summary:         Development files for %{name}
Group:           Development/Libraries
Requires:        %{name}-libs%{_isa} = %{?epoch}:%{version}-%{release}
Requires:        %{name}-cuda%{_isa} = %{?epoch}:%{version}-%{release}

#Don't put an epoch here
Provides:        cuda-drivers-devel = %{version}
Provides:        cuda-drivers-devel%{_isa} = %{version}

%description devel
This package provides the development files of the %{name} package,
such as OpenGL headers.

%package cuda
Summary:         CUDA libraries for %{name}
Group:           Development/Libraries
# Requires:        %{_nvidia_serie}-kmod >= %{?epoch}:%{version}
Provides:        nvidia-modprobe = %{version}-%{release}
Provides:        nvidia-persistenced = %{version}-%{release}

Conflicts:       xorg-x11-drv-nvidia-340xx-cuda

#Don't put an epoch here
Provides:        cuda-drivers = %{version}
Provides:        cuda-drivers%{_isa} = %{version}

%description cuda
This package provides the CUDA driver libraries.

%package -n dkms-%{name}
Summary:         %{name} dkms module
Group:           System Environment/Kernel
Requires: 	 kernel-devel
Requires: xorg-x11-drv-nvidia >= %{epoch}:%{version}-%{release}

%description -n dkms-%{name}
%{name} dkms module

%package libs
Summary:         Libraries for %{name}
Group:           User Interface/X Hardware Support
Requires:        %{name} = %{?epoch}:%{version}-%{release}
Requires:        libvdpau%{_isa} >= 0.5

%description libs
This package provides the shared libraries for %{name}.


%prep
%setup -q -c -T
#Only extract the needed arch
sh %{SOURCE1} \
  --extract-only --target nvidiapkg-%{_target_cpu}
ln -s nvidiapkg-%{_target_cpu} nvidiapkg
patch -p1 < %{PATCH1}


%build
# Nothing to build
echo "Nothing to build"


%install
rm -rf $RPM_BUILD_ROOT

cd nvidiapkg

# The new 256.x version supplies all the files in a relatively flat structure
# .. so explicitly deal out the files to the correct places
# .. nvidia-installer looks too closely at the current machine, so it's hard
# .. to generate rpm's unless a NVIDIA card is in the machine.

rm -f nvidia-installer*

install -m 0755 -d $RPM_BUILD_ROOT%{_bindir}

# ld.so.conf.d file
install -m 0755 -d       $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/
echo "%{_nvidia_libdir}" > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia-%{_lib}.conf

#Blacklist nouveau (since F-11)
install    -m 0755 -d         $RPM_BUILD_ROOT/etc/modprobe.d/
install -p -m 0644 %{SOURCE6} $RPM_BUILD_ROOT/etc/modprobe.d/

# Simple wildcard install of libs
install -m 0755 -d $RPM_BUILD_ROOT%{_nvidia_libdir}
install -p -m 0755 lib*.so.%{version}          $RPM_BUILD_ROOT%{_nvidia_libdir}/
%ifarch x86_64 i686
install -m 0755 -d $RPM_BUILD_ROOT%{_nvidia_libdir}/tls/
install -p -m 0755 tls/lib*.so.%{version}      $RPM_BUILD_ROOT%{_nvidia_libdir}/tls/
%endif

%ifarch x86_64 i686
# OpenCL config
install    -m 0755         -d $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors/
install -p -m 0644 nvidia.icd $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors/
install -p -m 0755 libOpenCL.so.1.0.0          $RPM_BUILD_ROOT%{_nvidia_libdir}/
ln -s libOpenCL.so.1.0.0 $RPM_BUILD_ROOT%{_nvidia_libdir}/libOpenCL.so.1
ln -s libOpenCL.so.1.0.0 $RPM_BUILD_ROOT%{_nvidia_libdir}/libOpenCL.so
%endif

#Vdpau
install -m 0755 -d $RPM_BUILD_ROOT%{_libdir}/vdpau/
install -p -m 0755 libvdpau*.so.%{version}     $RPM_BUILD_ROOT%{_libdir}/vdpau

#
mkdir -p $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/
mkdir -p $RPM_BUILD_ROOT%{_nvidia_xorgdir}

# .. but some in a different place
install -m 0755 -d $RPM_BUILD_ROOT%{_nvidia_xorgdir}
install -m 0755 -d $RPM_BUILD_ROOT%{_nvidia_xorgdir}
rm -f $RPM_BUILD_ROOT%{_nvidia_libdir}/lib{nvidia-wfb,glx,vdpau*}.so.%{version}

# Finish up the special case libs
install -p -m 0755 libglx.so.%{version}        $RPM_BUILD_ROOT%{_nvidia_xorgdir}
install -p -m 0755 nvidia_drv.so               $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/

# Install binaries
install -p -m 0755 nvidia-{bug-report.sh,debugdump,smi,cuda-mps-control,cuda-mps-server,xconfig,settings,persistenced,modprobe} \
  $RPM_BUILD_ROOT%{_bindir}

# Install headers
install -m 0755 -d $RPM_BUILD_ROOT%{_includedir}/nvidia/GL/
install -p -m 0644 {gl.h,glext.h,glx.h,glxext.h} $RPM_BUILD_ROOT%{_includedir}/nvidia/GL/

# Install man pages
install    -m 0755 -d   $RPM_BUILD_ROOT%{_mandir}/man1/
install -p -m 0644 *.gz $RPM_BUILD_ROOT%{_mandir}/man1/

# Make unversioned links to dynamic libs
for lib in $( find $RPM_BUILD_ROOT%{_libdir} -name lib\*.%{version} ) ; do
  ln -s ${lib##*/} ${lib%.%{version}}
  ln -s ${lib##*/} ${lib%.%{version}}.1
done


# Install nvidia icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -pm 0644 nvidia-settings.png $RPM_BUILD_ROOT%{_datadir}/pixmaps

# Remove duplicate install
rm $RPM_BUILD_ROOT%{_nvidia_libdir}/libnvidia-{cfg,tls}.so

#Install static driver dependant configuration files
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d
install -pm 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d
install -pm 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d
# Comment Xorg abi override
install -pm 0644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d
sed -i -e 's|@LIBDIR@|%{_libdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d/99-nvidia.conf
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d/99-nvidia.conf
install -pm 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/X11/

# Desktop entry for nvidia-settings
desktop-file-install --vendor "" \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
    --set-icon=nvidia-settings \
    --set-key=Exec --set-value=nvidia-settings \
    nvidia-settings.desktop

#Workaround for self made xorg.conf using a Files section.
ln -fs ../../%{_nvidia_serie}/xorg $RPM_BUILD_ROOT%{_libdir}/xorg/modules/%{_nvidia_serie}-%{version}

#Workaround for cuda availability - rfbz#2916
ln -fs %{_nvidia_libdir}/libcuda.so.1 $RPM_BUILD_ROOT%{_libdir}/libcuda.so.1
ln -fs %{_nvidia_libdir}/libcuda.so $RPM_BUILD_ROOT%{_libdir}/libcuda.so

#Alternate-install-present is checked by the nvidia .run
install -p -m 0644 %{SOURCE7}            $RPM_BUILD_ROOT%{_nvidia_libdir}

#install the NVIDIA supplied application profiles
mkdir -p $RPM_BUILD_ROOT%{_datadir}/nvidia
install -p -m 0644 nvidia-application-profiles-%{version}-{rc,key-documentation} $RPM_BUILD_ROOT%{_datadir}/nvidia

#Install the output class configuration file - xorg-server >= 1.16
mkdir -p $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d
install -pm 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/nvidia.conf

#Avoid prelink to mess with nvidia libs - rfbz#3258
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/prelink.conf.d
touch $RPM_BUILD_ROOT%{_sysconfdir}/prelink.conf.d/nvidia-%{_lib}.conf

#Install the initscript
tar jxf nvidia-persistenced-init.tar.bz2
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -pm 0644 nvidia-persistenced-init/systemd/nvidia-persistenced.service.template \
  $RPM_BUILD_ROOT%{_unitdir}/nvidia-persistenced.service
#Change the daemon running owner
sed -i -e "s/__USER__/root/" $RPM_BUILD_ROOT%{_unitdir}/nvidia-persistenced.service

#Create the default nvidia config directory
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/nvidia

#Ghost Xorg nvidia.conf file
touch $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d/nvidia.conf

#Install the nvidia kernel modules sources archive
mkdir -p $RPM_BUILD_ROOT%{_datadir}/nvidia-kmod-%{version}
mv kernel nvidia-%{version}
#tar Jcf $RPM_BUILD_ROOT%{_datadir}/nvidia-kmod-%{version}/nvidia-kmod-%{version}-%{_target_cpu}.tar.xz nvidia-%{version}
if [ ! -e $RPM_BUILD_ROOT/usr/src ];
then
	mkdir -p $RPM_BUILD_ROOT/usr/src
fi
cp nvidia-%{version} $RPM_BUILD_ROOT/usr/src/ -R
install -m0644 %{SOURCE11} $RPM_BUILD_ROOT/usr/src/nvidia-%{version}/dkms.conf
sed -e "s|PACKAGE_VERSION=@VERSION@|PACKAGE_VERSION=\"%{version}\"|" -i $RPM_BUILD_ROOT/usr/src/nvidia-%{version}/dkms.conf
install -m0644 %{SOURCE6} $RPM_BUILD_ROOT/usr/src/nvidia-%{version}/
install -m0755 %{SOURCE12} $RPM_BUILD_ROOT/usr/src/nvidia-%{version}/
install -m0755 %{SOURCE13} $RPM_BUILD_ROOT/usr/src/nvidia-%{version}/

#Add autostart file for nvidia-settings to load user config
install -D -p -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/nvidia-settings.desktop


%pre
if [ "$1" -eq "1" ]; then
  if [ -x %{_bindir}/nvidia-uninstall ]; then
    %{_bindir}/nvidia-uninstall -s && rm -f %{_bindir}/nvidia-uninstall &>/dev/null || :
  fi
fi

%pre libs
if [ -d %{_sysconfdir}/prelink.conf.d ]; then
echo "-b %{_nvidia_libdir}" > %{_sysconfdir}/prelink.conf.d/nvidia-%{_lib}.conf
fi

%post
if [ "$1" -eq "1" ]; then
  ISGRUB1=""
  #echo "GRUB_GFXPAYLOAD_LINUX=text" >> %{_sysconfdir}/default/grub
  #grub-mkconfig -o /boot/grub/grub.cfg
  if [ -x /sbin/grubby ] ; then
    KERNELS=`/sbin/grubby --default-kernel`
    DIST=`rpm -E %%{?dist}`
    ARCH=`uname -m`
    [ -z $KERNELS ] && KERNELS=`ls /boot/vmlinuz-*${DIST}.${ARCH}*`
    for kernel in ${KERNELS} ; do
      /sbin/grubby $ISGRUB1 \
        --update-kernel=${kernel} \
        --args="nouveau.modeset=0 rd.driver.blacklist=nouveau video=vesa:off $GFXPAYLOAD" \
         &>/dev/null
    done
  fi
fi || :

%postun
sed -e 's|GRUB_GFXPAYLOAD_LINUX=.*|GRUB_GFXPAYLOAD_LINUX=keep|' -i /etc/default/grub

%post libs -p /sbin/ldconfig

%post cuda
/sbin/ldconfig
%systemd_post nvidia-persistenced.service

%posttrans
 [ -f %{_sysconfdir}/X11/xorg.conf ] || \
   cp -p %{_sysconfdir}/X11/nvidia-xorg.conf %{_sysconfdir}/X11/xorg.conf || :
sed -e 's|GRUB_GFXPAYLOAD_LINUX=.*|GRUB_GFXPAYLOAD_LINUX=text|' -i /etc/default/grub

%preun
if [ "$1" -eq "0" ]; then
  ISGRUB1=""
  # 下面这项在没有安装时是打开的
  sed -i -e 's|GRUB_GFXPAYLOAD_LINUX=.*||g' /etc/default/grub
  if [ -x /sbin/grubby ] ; then
    DIST=`rpm -E %%{?dist}`
    ARCH=`uname -m`
    KERNELS=`ls /boot/vmlinuz-*${DIST}.${ARCH}*`
    for kernel in ${KERNELS} ; do
      /sbin/grubby $ISGRUB1 \
        --update-kernel=${kernel} \
        --remove-args="nouveau.modeset=0 rdblacklist=nouveau \
            rd.driver.blacklist=nouveau nomodeset video=vesa:off \
            gfxpayload=vga=normal vga=normal" &>/dev/null
    done
  fi

  #Backup and disable previously used xorg.conf
  [ -f %{_sysconfdir}/X11/xorg.conf ] && \
    mv  %{_sysconfdir}/X11/xorg.conf %{_sysconfdir}/X11/xorg.conf.%{name}_uninstalled &>/dev/null
fi ||:

%posttrans -n dkms-%{name}
(
dkms add -m nvidia -v %{version}
dkms build -m nvidia -v %{version}
dkms install -m nvidia -v %{version} --force
/sbin/depmod -a
/usr/sbin/dracut --omit-drivers nouveau -f /boot/initrd-$(uname -r).img $(uname -r)
) || :

%preun -n dkms-%{name}
(
dkms uninstall -m nvidia -v %{version}
dkms remove -m nvidia -v %{version} --all
/sbin/depmod -a
/usr/sbin/dracut -f /boot/initrd-$(uname -r).img $(uname -r)
) || :

%preun cuda
%systemd_preun nvidia-persistenced.service

%postun libs -p /sbin/ldconfig

%postun cuda
/sbin/ldconfig
%systemd_postun_with_restart nvidia-persistenced.service

%files
%defattr(-,root,root,-)
%doc nvidiapkg/LICENSE
%doc nvidiapkg/NVIDIA_Changelog
%doc nvidiapkg/README.txt
%doc nvidiapkg/nvidia-application-profiles-%{version}-rc
%doc nvidiapkg/html
%dir %{_sysconfdir}/nvidia
%ghost  %{_sysconfdir}/X11/xorg.conf.d/nvidia.conf
%config %{_sysconfdir}/X11/xorg.conf.d/99-nvidia.conf
%config %{_sysconfdir}/X11/xorg.conf.d/00-avoid-glamor.conf
# Comment Xorg abi override
%config %{_sysconfdir}/X11/xorg.conf.d/00-ignoreabi.conf
#%config(noreplace) %{_prefix}/lib/modprobe.d/blacklist-nouveau.conf
%config(noreplace) %{_sysconfdir}/X11/nvidia-xorg.conf
%config %{_sysconfdir}/xdg/autostart/nvidia-settings.desktop
%{_bindir}/nvidia-bug-report.sh
%{_bindir}/nvidia-settings
%{_bindir}/nvidia-xconfig
# Xorg libs that do not need to be multilib
%dir %{_nvidia_xorgdir}
%{_nvidia_xorgdir}/*.so*
%{_libdir}/xorg/modules/drivers/nvidia_drv.so
%{_libdir}/xorg/modules/%{_nvidia_serie}-%{version}
# It's time that nvidia-settings used gtk3
%exclude %{_nvidia_libdir}/libnvidia-gtk2.so*
%{_nvidia_libdir}/libnvidia-gtk3.so*
#/no_multilib
%{_datadir}/X11/xorg.conf.d/nvidia.conf
%dir %{_datadir}/nvidia
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-*
%{_datadir}/applications/*nvidia-settings.desktop
%{_datadir}/pixmaps/*.png
%{_mandir}/man1/nvidia-settings.*
%{_mandir}/man1/nvidia-xconfig.*

%files -n dkms-%{name}
%config(noreplace) /etc/modprobe.d/blacklist-nouveau.conf
/usr/src/nvidia-%{version}/*
#%dir %{_datadir}/nvidia-kmod-%{version}
#%{_datadir}/nvidia-kmod-%{version}/nvidia-kmod-%{version}-%{_target_cpu}.tar.xz

%files libs
%defattr(-,root,root,-)
%dir %{_nvidia_libdir}
%config %{_sysconfdir}/ld.so.conf.d/nvidia-%{_lib}.conf
%ghost %{_sysconfdir}/prelink.conf.d/nvidia-%{_lib}.conf
%{_nvidia_libdir}/alternate-install-present
%{_nvidia_libdir}/*.so.*
%exclude %{_nvidia_libdir}/libcuda.so*
%exclude %{_nvidia_libdir}/libnvidia-gtk*.so*
%exclude %{_nvidia_libdir}/libnvcuvid.so*
%exclude %{_nvidia_libdir}/libnvidia-encode.so*
%exclude %{_nvidia_libdir}/libOpenCL.so.*
%exclude %{_nvidia_libdir}/libnvidia-compiler.so*
%exclude %{_nvidia_libdir}/libnvidia-opencl.so*
%dir %{_nvidia_libdir}/tls
%{_nvidia_libdir}/tls/*.so.*
%exclude %{_libdir}/vdpau/libvdpau.*
%{_libdir}/vdpau/libvdpau_nvidia.so.*
%exclude %{_libdir}/vdpau/libvdpau_trace.so*

%files cuda
%defattr(-,root,root,-)
%{_unitdir}/nvidia-persistenced.service
%{_bindir}/nvidia-debugdump
%{_bindir}/nvidia-smi
%{_bindir}/nvidia-cuda-mps-control
%{_bindir}/nvidia-cuda-mps-server
%{_bindir}/nvidia-persistenced
#nvidia-modprobe is setuid root to allow users to load the module in 
%attr(4755, root, root) %{_bindir}/nvidia-modprobe
%{_libdir}/libcuda.so*
%{_nvidia_libdir}/libcuda.so*
%{_nvidia_libdir}/libnvcuvid.so*
%{_nvidia_libdir}/libnvidia-encode.so*
%{_nvidia_libdir}/libnvidia-ml.so*
%dir %{_sysconfdir}/OpenCL
%dir %{_sysconfdir}/OpenCL/vendors
%config %{_sysconfdir}/OpenCL/vendors/nvidia.icd
%{_nvidia_libdir}/libnvidia-compiler.so*
%{_nvidia_libdir}/libnvidia-opencl.so*
%{_mandir}/man1/nvidia-smi.*
%{_mandir}/man1/nvidia-cuda-mps-control.1.*
%{_mandir}/man1/nvidia-persistenced.1.*
%{_mandir}/man1/nvidia-modprobe.1.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/nvidia/
%exclude %{_nvidia_libdir}/libOpenCL.so
%{_nvidia_libdir}/tls/libnvidia-tls.so
%{_libdir}/vdpau/libvdpau_nvidia.so
%{_nvidia_libdir}/libnvidia-ifr.so
%{_nvidia_libdir}/libEGL.so
%{_nvidia_libdir}/libGLESv1_CM.so
%{_nvidia_libdir}/libGLESv2.so
%{_nvidia_libdir}/libnvidia-eglcore.so
%{_nvidia_libdir}/libnvidia-glsi.so
%{_nvidia_libdir}/libGL.so
%{_nvidia_libdir}/libnvidia-glcore.so
%{_nvidia_libdir}/libnvidia-fbc.so

%changelog
* Tue Nov 17 2015 sulit <sulitsrc@gmail.com> - 352.55-3
-  add pre_build.sh and post_install.sh

* Mon Nov 16 2015 sulit <sulitsrc@gmail.com> - 352.55-2
-  update dkms for nvidia

* Wed Nov 04 2015 sulit <sulitsrc@gmail.com> - 352.55-1
-  update version to 352.55

* Fri Oct 30 2015 sulit <sulitsrc@gmail.com> - 352.41-1
- new build for isoft 4.0
