%define debug_package %{nil}

%define mod_name tuxedo-wmi 

Name: dkms-%{mod_name}
Version: 1.5.1
Release: 3 
Summary: Dkms driver source for Clevo P150EM/P170EM/P150SM/P157SM/P170SM/P177SM backlight keyboard

License: GPL
URL: http://www.linux-onlineshop.de/forum/index.php?page=Thread&threadID=26&s=82130b57e71bd5b6ea569abc1424025c6f8d412d 
Source0: tuxedo-wmi-1.5.1.src.tar.gz 
Source1: tuxedo-wmi-dkms.conf

Requires: kernel kernel-headers dkms gcc make

Conflicts: dkms-clevo-xsm-wmi

%description
%{summary}

%prep
%setup -q -n %{mod_name}-%{version}

%build

%install
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}

#install dkms.conf
install -m0644 %{SOURCE1} %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
sed -e "s/@MOD_VER@/%{version}/g" -i %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf

#install sources
cp -r src/Makefile src/tuxedo-wmi.c %{buildroot}/usr/src/%{mod_name}-%{version}/

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
* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 1.5.1-3
- Switch from post to postrans to run postscript

* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 1.5.1-2
- Initial build



