%define debug_package %{nil}

%define mod_name igb 

Name: dkms-%{mod_name}
Version: 5.3.3.2 
Release: 2 
Summary: Dkms driver sources for Intel igb Ethernet adapter
License: GPL
URL: http://sourceforge.net/projects/e1000
Source0: http://sourceforge.net/projects/e1000/files/igb%20stable/%{version}/igb-%{version}.tar.gz

Source1: %{mod_name}-dkms.conf

Requires: kernel kernel-headers dkms gcc make

%description
%{summary}

%prep
%setup -q -n %{mod_name}-%{version}

%build

%install
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}/

install -m 0644 %{SOURCE1} %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
sed -e "s/@MOD_VER@/%{version}/g" -i %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf

#install sources
cp -r src/*.c src/*.h %{buildroot}/usr/src/%{mod_name}-%{version}/
cp -r src/Makefile %{buildroot}/usr/src/%{mod_name}-%{version}/

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

%changelog
* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 5.3.3.2-2
- Initial build


