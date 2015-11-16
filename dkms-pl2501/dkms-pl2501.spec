%define debug_package %{nil}

%define mod_name pl2501 

Name: dkms-%{mod_name}
Version: 20121021 
Release: 2 
Summary: Dkms driver source for PL-2501 USB Easy Trasfer Cables

License: GPL
URL: https://patchwork.kernel.org/patch/1227361
Source0: pl2501.c
Source1: Makefile
Source2: %{mod_name}-dkms.conf

Requires: kernel kernel-headers dkms gcc make

%description
%{summary}

%prep
%build
%install
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}

#install dkms.conf
install -m0644 %{SOURCE2} %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
sed -e "s/@MOD_VER@/%{version}/g" -i %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf

#install sources
install -m0644 %{SOURCE0} %{SOURCE1} %{buildroot}/usr/src/%{mod_name}-%{version}/

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

%changelog
* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 20121021-2
- Initial build



