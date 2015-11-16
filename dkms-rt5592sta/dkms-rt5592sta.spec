%define debug_package %{nil}

%define mod_name rt5592sta

Name: dkms-%{mod_name}
Version: 2.6.0.0
Release: 2
Summary: Drivers for rt2860 chipset wireless cards

License: GPL
URL: http://www.ralinktech.com/
Source0: http://dlcdnet.asus.com/pub/ASUS/wireless/PCE-N53/Linux_PCE_N53_1008.zip

Source1: %{mod_name}-dkms.conf

Patch0: arch_build_preparation.patch
Patch1: rt5592sta_fix_64bit_3.8.patch
Patch2: extra.patch
Patch3: 4.9_preperation.patch
Patch4: rename-to-rt5592sta.patch

Requires: kernel kernel-headers dkms gcc make

%description
%{summary}

%prep
%setup -q -c
pushd Linux
tar jxf DPO_GPL_RT5592STA_LinuxSTA_v2.6.0.0_20120326.tar.bz2
popd

pushd Linux/DPO_GPL_RT5592STA_LinuxSTA_v2.6.0.0_20120326
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
popd


%build


%install
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}/
mkdir -p %{buildroot}/etc/modprobe.d/

#install dkms.conf
install -m0644 %{SOURCE1} %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
sed -e "s/@MOD_VER@/%{version}/g" -i %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf

pushd Linux/DPO_GPL_RT5592STA_LinuxSTA_v2.6.0.0_20120326
cp -r * %{buildroot}/usr/src/%{mod_name}-%{version}/

#remove precompiled elf.
rm -rf %{buildroot}/usr/src/%{mod_name}-%{version}/tools/bin2h

install -D -m 0644 RT2860STA.dat %{buildroot}/etc/Wireless/RT5592STA/RT5592STA.dat
popd 


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
/etc/Wireless/RT5592STA
/usr/src/%{mod_name}-%{version}

%changelog
* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 2.6.0.0-2
- Remove precompiled elf

* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 2.6.0.0-2
- Initial build
