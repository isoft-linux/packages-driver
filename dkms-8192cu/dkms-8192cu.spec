%define debug_package %{nil}

%define mod_name 8192cu 

Name: dkms-%{mod_name}
Version: 4.0.2.9000 
Release: 4
Summary: Drivers for Realtek RTL8188CUS (8188C, 8192C) chipset wireless cards 
License: GPL
URL: http://www.realtek.com.tw
Source0: https://dl.dropboxusercontent.com/u/54784933/8192cu-v4.0.2_9000.tar.gz

Source1: %{mod_name}-dkms.conf
Source2: %{mod_name}-blacklist.conf

Patch0: fix_310_proc2.patch
Patch1: N150MA.patch
Patch2: NoDebug.patch
Patch3: ISY.patch
Patch4: D-link.patch
Patch5: HWNUM-300V2.patch
Patch6: RTL8192CU-kernel-4.0.patch

Requires: kernel kernel-headers dkms gcc make

%description
%{summary}

%prep
%setup -q -n 8192cu-v4.0.2_9000
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

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
cp -r core hal include os_dep %{buildroot}/usr/src/%{mod_name}-%{version}/
cp -r Kconfig Makefile %{buildroot}/usr/src/%{mod_name}-%{version}/

%posttrans
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
* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 4.0.2.9000-4
- Switch from post to postrans to run postscript

* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 4.0.2.9000-3
- Initial build

* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com>
- Initial build

