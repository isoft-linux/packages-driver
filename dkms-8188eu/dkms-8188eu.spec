%define debug_package %{nil}

%define mod_name 8188eu

Name: dkms-%{mod_name}
Version: 4.3.0.8.13968 
Release: 2 
Summary: Dkms driver sources for Realtek RTL8188EUS (RTL8188EUS, RTL8188ETV) WLAN
License: GPL
URL: http://www.realtek.com.tw
Source0: https://dl.dropboxusercontent.com/u/27457926/8188eu-v4.3.0.8_13968.tar.xz

Source1: %{mod_name}-dkms.conf
Source2: %{mod_name}-blacklist.conf

Patch0: date_time_macro.patch
Patch1: linux-4.0.patch
Patch2: linux-4.2.patch
Patch3: no_debug.patch

Requires: kernel kernel-headers dkms gcc make

%description
%{summary}

%prep
%setup -q -n 8188eu-v4.3.0.8_13968 
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1


find . -type f|xargs chmod 644 ||:

%build

%install
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}/
mkdir -p %{buildroot}/etc/modprobe.d/
install -m 0644 %{SOURCE1} %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
sed -e "s/@MOD_VER@/%{version}/g" -i %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
install -m 0644 %{SOURCE2} %{buildroot}/etc/modprobe.d/%{mod_name}-blacklist.conf

#install sources
sed -i 's/^CONFIG_POWER_SAVING \= y/CONFIG_POWER_SAVING = n/' Makefile
cp -r core hal include os_dep platform %{buildroot}/usr/src/%{mod_name}-%{version}/
cp -r Kconfig Makefile %{buildroot}/usr/src/%{mod_name}-%{version}/

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
/etc/modprobe.d/%{mod_name}-blacklist.conf

%changelog
* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 4.3.0.8.13968-2
- Initial build


