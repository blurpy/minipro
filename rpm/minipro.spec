# .SPEC-file to package RPMs for openSUSE

# adapt commit id and commitdate to match the git version you want to build
%global commit bf6770858dccac76b92bc0b74af1e2fe1c9369a9
%global commitdate 20200402

# then download and build like this:
# rpmdev-spectool -g -R minipro.spec
# rpmbuild -ba minipro.spec

Summary: Program for controlling the MiniPRO TL866xx series of chip programmers
Name: minipro
Version: 0.1
%global shortcommit %(c=%{commit}; echo ${c:0:7})
Release: %{commitdate}.%{shortcommit}%{?dist}
License: GPLv3
URL: https://gitlab.com/DavidGriffith/minipro
Source: https://gitlab.com/DavidGriffith/%{name}/-/archive/%{commit}/%{name}-%{commit}.tar.gz
BuildRequires: libusb-1_0-devel

%description
Software for Minipro TL866XX series of programmers from autoelectric.cn
Used to program flash, EEPROM, etc.

%prep
%autosetup -n %{name}-%{commit}

%build
make #%{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}

install -D -p -m 0644 udev/60-minipro.rules %{buildroot}/%{_udevrulesdir}/60-minipro.rules
install -D -p -m 0644 udev/61-minipro-plugdev.rules %{buildroot}/%{_udevrulesdir}/61-minipro-plugdev.rules
install -D -p -m 0644 udev/61-minipro-uaccess.rules %{buildroot}/%{_udevrulesdir}/61-minipro-uaccess.rules
install -D -p -m 0644 bash_completion.d/minipro %{buildroot}/%{_sysconfdir}/bash_completion.d/minipro

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%{_bindir}/minipro
%{_bindir}/miniprohex
%{_mandir}/man1/%{name}.*
%{_udevrulesdir}/60-minipro.rules
%{_udevrulesdir}/61-minipro-plugdev.rules
%{_udevrulesdir}/61-minipro-uaccess.rules
%{_sysconfdir}/bash_completion.d/*
