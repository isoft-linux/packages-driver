%define debug_package %{nil}

%define mod_name rt3290

Name: dkms-%{mod_name}
Version: 2.6.0.0
Release: 2
Summary: Drivers for rt3290 chipset wireless cards

License: GPL
URL: http://www.ralinktech.com/
Source0: https://launchpad.net/~barracuda72/+archive/ralink/+files/rt3290-dkms_2.6.0.0rev1-0ubuntu1~ppa1.tar.gz
Patch0: rt3290sta_fix_64bit_3.8.patch
Patch1: kernel_version_fix.patch
Patch2: 3.14fix.patch
Patch3: sta_fix.patch

Requires: kernel kernel-headers dkms gcc make

%description
%{summary}

%prep
%setup -q -n rt3290-%{version}rev1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build


%install
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}/
mkdir -p %{buildroot}/etc/Wireless/RT2860STA/
mkdir -p %{buildroot}/etc/modprobe.d/

cp -Rv chips common include os rate_ctrl sta tools %{buildroot}/usr/src/%{mod_name}-%{version}/

install -m 0644 Makefile %{buildroot}/usr/src/%{mod_name}-%{version}/
install -m 0644 debian/dkms.conf %{buildroot}/usr/src/%{mod_name}-%{version}/
install -m 0755 RT2860STA.dat %{buildroot}/etc/Wireless/RT2860STA/
install -m 0644 blacklist-ralink.conf %{buildroot}/etc/modprobe.d/%{mod_name}-blacklist.conf

%post
(
dkms add -m %{mod_name} -v %{version} 
dkms build -m %{mod_name} -v %{version} 
dkms install -m %{mod_name} -v %{version} --force
/sbin/depmod -a
) ||: 

%preun
(
dkms uninstall -m %{mod_name} -v %{version} 
dkms remove -m %{mod_name} -v %{version} --all
/sbin/depmod -a
) ||:

%files
/usr/src/%{mod_name}-%{version}
/etc/Wireless/RT2860STA
/etc/modprobe.d/%{mod_name}-blacklist.conf

%changelog
* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 2.6.0.0-2
- Initial build
