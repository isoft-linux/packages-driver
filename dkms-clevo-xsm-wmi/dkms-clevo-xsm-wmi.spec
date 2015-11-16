%define debug_package %{nil}

%define mod_name clevo-xsm-wmi 

Name: dkms-%{mod_name}
Version: 0.4 
Release: 2
Summary: Dkms driver source for Clevo backlight keyboard based on tuxedo-wmi
License: GPL
URL: https://bitbucket.org/lynthium/clevo-xsm-wmi
#https://bitbucket.org/lynthium/clevo-xsm-wmi
Source0: %{mod_name}.tar.gz
Source1: %{mod_name}-dkms.conf

#for utility
BuildRequires: qt5-qtbase-devel
#for _unitdir rpm macro.
BuildRequires: systemd

Requires: kernel kernel-headers dkms gcc make
Requires: systemd

Conflicts: dkms-tuxedo-wmi
%description
%{summary}

%prep
%setup -q -n %{mod_name}

%build
pushd utility
qmake-qt5
make
popd

%install
#install qt based utility and systemd service
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
install -m0755 utility/clevo-xsm-wmi %{buildroot}%{_bindir}/clevo-xsm-wmi
install -m0644 utility/systemd/clevo-xsm-wmi.service %{buildroot}%{_unitdir}

#install dkms
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}

#install dkms.conf
install -m0644 %{SOURCE1} %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
sed -e "s/@MOD_VER@/%{version}/g" -i %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf

#install sources
cp -r module/Makefile module/clevo-xsm-wmi.c %{buildroot}/usr/src/%{mod_name}-%{version}/

%post
%systemd_post clevo-xsm-wmi.service
(
dkms add -m %{mod_name} -v %{version}
dkms build -m %{mod_name} -v %{version}
dkms install -m %{mod_name} -v %{version} --force
/sbin/depmod -a
) || :

%preun
%systemd_preun clevo-xsm-wmi.service
(
dkms uninstall -m %{mod_name} -v %{version}
dkms remove -m %{mod_name} -v %{version} --all
/sbin/depmod -a
) || :

%postun
%systemd_postun_with_restart clevo-xsm-wmi.service

%files
%{_bindir}/clevo-xsm-wmi
%{_unitdir}/clevo-xsm-wmi.service
/usr/src/%{mod_name}-%{version}

%changelog
* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 0.4-2
- Initial build




