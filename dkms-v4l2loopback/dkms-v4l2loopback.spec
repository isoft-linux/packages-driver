%define debug_package %{nil}

%define mod_name v4l2loopback 

Name: dkms-%{mod_name}
Version: 0.9.1
Release: 2 
Summary: Dkms driver source to create v4l2-loopback device

License: GPL
URL: https://github.com/umlaeute/v4l2loopback
#https://github.com/umlaeute/v4l2loopback/archive/v0.9.1.tar.gz
Source0: %{mod_name}-%{version}.tar.gz

BuildRequires: help2man 
Requires: kernel kernel-headers dkms gcc make

%description
%{summary}

%prep
%setup -q -n %{mod_name}-%{version}

%build
%install
make DESTDIR=%{buildroot} PREFIX="/usr" install-utils install-man


mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}
#install dkms.conf
install -m0644 dkms.conf %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf
#install driver sources
cp -r * %{buildroot}/usr/src/%{mod_name}-%{version}

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
%{_bindir}/v4l2loopback-ctl
%{_mandir}/man1/v4l2loopback-ctl.1*

/usr/src/%{mod_name}-%{version}

%changelog
* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 0.9.1-2
- Initial build

