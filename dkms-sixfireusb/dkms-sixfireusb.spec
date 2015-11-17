%define debug_package %{nil}

%define mod_name sixfireusb 

Name: dkms-%{mod_name}
Version: 0.6.1 
Release: 4
Summary: Dkms driver source for Terratec DMX6FireUSB soundcard, include firmware. 

License: GPL
URL: http://sourceforge.net/projects/sixfireusb
Source0: http://sourceforge.net/projects/sixfireusb/files/sixfireusb-0.6.1.tar.bz2
Source1: http://sourceforge.net/projects/sixfireusb/files/tools/fwinst.sh
#Put all firmware in linux-firmware package.
##firmware extracted by fwinst.sh
#Source5: dmx6fireap.ihx
#Source6: dmx6firel2.ihx
#Source7: dmx6firecf.bin

Source10: %{mod_name}-dkms.conf

Patch0: kernel-3.16.patch
Patch1: grsecurity.patch
Patch2: fwinst.patch

Requires: kernel kernel-headers dkms gcc make

%description
%{summary}

%prep
%setup -q -n %{mod_name}-%{version}
cp %{SOURCE1} .
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

%install
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}

#install all sources
cp -r * %{buildroot}/usr/src/%{mod_name}-%{version}/
rm -rf %{buildroot}/usr/src/%{mod_name}-%{version}/*.sh

#install dkms.conf
install -m0644 %{SOURCE10} %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
sed -e "s/@MOD_VER@/%{version}/g" -i %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf

#install firmwares
#mkdir -p %{buildroot}/lib/firmware
#install -m0644 %{SOURCE5} %{SOURCE6} %{SOURCE7} %{buildroot}/lib/firmware
 
%posttrans
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

%changelog
* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 0.6.1-4
- Move all firmwares to linux-firmware package

* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 0.6.1-3
- Switch from post to postrans to run postscript

* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 0.6.1-2
- Initial build



