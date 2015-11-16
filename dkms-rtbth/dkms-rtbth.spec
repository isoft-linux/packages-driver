%define debug_package %{nil}

%define mod_name rtbth

Name: dkms-%{mod_name}
Version: 3.9.4.1 
Release: 3
Summary: Kernel module sources for Ralink RT3290 bluetooth

License: GPL
URL: http://www.mediatek.com
#https://github.com/f1u77y/rtbth-dkms-aur/archive/%{version}.tar.gz
Source0: rtbth-%{version}.tar.gz

Requires: kernel kernel-headers dkms gcc make

%description
%{summary}

%prep
%setup -q -n rtbth-%{version}

%build

%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}
mkdir -p %{buildroot}/etc/modprobe.d/

cp -r ./* %{buildroot}/usr/src/%{mod_name}-%{version}

#do not remake initrd
sed -i -e 's#REMAKE_INITRD="yes"##g' %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf

#unneeded files
rm -rf %{buildroot}/usr/src/%{mod_name}-%{version}/tools

install -m0755 tools/rtbt %{buildroot}/usr/bin/
install -m0644 tools/ralink-bt.conf %{buildroot}/etc/modprobe.d/rt3290-bluetooth.conf

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
%{_bindir}/rtbt
/usr/src/%{mod_name}-%{version}
/etc/modprobe.d/rt3290-bluetooth.conf

%changelog
* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 3.9.4.1-3
- Do not remake initrd in dkms.conf

* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 3.9.4.1-2
- Initial build



