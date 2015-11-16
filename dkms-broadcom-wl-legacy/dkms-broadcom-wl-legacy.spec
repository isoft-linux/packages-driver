%define debug_package %{nil}

%define mod_name broadcom-wl-legacy 

Name: dkms-%{mod_name}
Version: 6.30.223.248
Release: 2
Summary: Dkms driver source for Broadcom 802.11 Linux STA wireless driver, legacy version
License: GPL
URL: https://www.broadcom.com/support/?gid=1 
#32bit source.
#Source0: https://www.broadcom.com/docs/linux_sta/hybrid-v35-nodebug-pcoem-6_30_223_248.tar.gz
Source0: https://www.broadcom.com/docs/linux_sta/hybrid-v35_64-nodebug-pcoem-6_30_223_248.tar.gz

Source2: %{mod_name}-dkms.conf

Source10: %{mod_name}-blacklist.conf

Patch0: linux-recent.patch
Patch1: license.patch
Patch2: gcc.patch
Patch3: fix-linux4.2.patch

Requires: kernel kernel-headers dkms gcc make
Conflicts: broadcom-wl
%description
%{summary}

%prep
%setup -q -c 
sed -i -e "/BRCM_WLAN_IFNAME/s:eth:wlan:" src/wl/sys/wl_linux.c
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

%install
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}

#install dkms.conf
install -m0644 %{SOURCE2} %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
sed -e "s/@MOD_VER@/%{version}/g" -i %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf

#install sources
cp -RL src lib Makefile %{buildroot}/usr/src/%{mod_name}-%{version}/

#install blacklist
mkdir -p  %{buildroot}/etc/modprobe.d
install -m 0644 %{SOURCE10} %{buildroot}/etc/modprobe.d/%{mod_name}-blacklist.conf


%post
(
dkms add -m %{mod_name} -v %{version}
dkms build -m %{mod_name} -v %{version}
dkms install -m %{mod_name} -v %{version} --force
/sbin/depmod -a
) || :

%preun
(
dkms uninstall -m %{mod_name} -v %{version}
dkms remove -m %{mod_name} -v %{version} --all
/sbin/depmod -a
) || :

%files
/usr/src/%{mod_name}-%{version}
/etc/modprobe.d/%{mod_name}-blacklist.conf

%changelog
* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 6.30.223.271-2
- Initial build



