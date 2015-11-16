%define debug_package %{nil}

%define mod_name mt7630e 

Name: dkms-%{mod_name}
Version: 2.3.4 
Release: 2
Summary: Dkms driver source for Mediatek 7630e PCIe Wifi 

License: GPL
URL: http://www.mediatek.com/en/downloads/mt7630-pcie/

#https://github.com/benjarobin/MT7630E/archive/v2.3.4.tar.gz 
Source0: MT7630E-%{version}.tar.gz

Source1: %{mod_name}-dkms.conf

Requires: kernel kernel-headers dkms gcc make

%description
%{summary}

%prep
%setup -q -n MT7630E-%{version}

%build

%install
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}

#install dkms.conf
install -m0644 %{SOURCE1} %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
sed -e "s/@MOD_VER@/%{version}/g" -i %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf

cp -RL rt2x00/* %{buildroot}/usr/src/%{mod_name}-%{version}
rm -rf %{buildroot}/usr/src/%{mod_name}-%{version}/*.sh

mkdir -p %{buildroot}/lib/firmware
install -m0644 firmware/Wi-FI/MT7650E234.bin %{buildroot}/lib/firmware/

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
/lib/firmware/MT7650E234.bin

%changelog
* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 8.040.00-2
- Initial build


