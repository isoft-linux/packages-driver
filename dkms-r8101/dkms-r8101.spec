%define debug_package %{nil}

%define mod_name r8101

Name: dkms-%{mod_name}
Version: 1.027.00 
Release: 3
Summary: Dkms driver source for Realtek 8101 network cards

License: GPL
URL: http://www.realtek.com.tw
Source0: http://12244.wpc.azureedge.net/8012244/drivers/rtdrivers/cn/nic/0002-%{mod_name}-%{version}.tar.bz2

Source1: %{mod_name}-dkms.conf

#conflict with r8169 provided by kernel.
Source2: %{mod_name}-blacklist.conf

Requires: kernel kernel-headers dkms gcc make

%description
%{summary}

%prep
%setup -q -n %{mod_name}-%{version}

%build

%install
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}

#install dkms.conf
install -m0644 %{SOURCE1} %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
sed -e "s/@MOD_NAME@/%{mod_name}/g" -e "s/@MOD_VER@/%{version}/g" -i %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf

#install sources
cp -r src %{buildroot}/usr/src/%{mod_name}-%{version}/
cp -r Makefile %{buildroot}/usr/src/%{mod_name}-%{version}/

#install blacklist
mkdir -p  %{buildroot}/etc/modprobe.d
install -m 0644 %{SOURCE2} %{buildroot}/etc/modprobe.d/%{mod_name}-blacklist.conf


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
/etc/modprobe.d/%{mod_name}-blacklist.conf

%changelog
* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 1.027.00-3
- Switch from post to postrans to run postscript

* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 8.040.00-2
- Initial build


