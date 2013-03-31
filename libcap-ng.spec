%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: An alternate posix capabilities library
Name: libcap-ng
Version: 0.6.4
Release: 3%{?dist}.1
License: LGPLv2+
Group: System Environment/Libraries
URL: http://people.redhat.com/sgrubb/libcap-ng
Source0: http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
Patch1: libcap-ng-0.6.5-device.patch
Patch2: libcap-ng-0.6.5-segv.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: kernel-headers >= 2.6.11 
BuildRequires: libattr-devel

%description
Libcap-ng is a library that makes using posix capabilities easier

%package devel
Summary: Header files for libcap-ng library
License: LGPLv2+
Group: Development/Libraries
Requires: kernel-headers >= 2.6.11
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The libcap-ng-devel package contains the files needed for developing
applications that need to use the libcap-ng library.

%package python
Summary: Python bindings for libcap-ng library
License: LGPLv2+
Group: Development/Libraries
BuildRequires: python-devel swig
Requires: %{name} = %{version}-%{release}

%description python
The libcap-ng-python package contains the bindings so that libcap-ng
and can be used by python applications.

%package utils
Summary: Utilities for analysing and setting file capabilities
License: GPLv2+
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description utils
The libcap-ng-utils package contains applications to analyse the
posix capabilities of all the program running on a system. It also
lets you set the file system based capabilities.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
%configure --libdir=/%{_lib}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="${RPM_BUILD_ROOT}" install

# Move the symlink
rm -f $RPM_BUILD_ROOT/%{_lib}/%{name}.so
mkdir -p $RPM_BUILD_ROOT%{_libdir}
VLIBNAME=$(ls $RPM_BUILD_ROOT/%{_lib}/%{name}.so.*.*.*)
LIBNAME=$(basename $VLIBNAME)
ln -s ../../%{_lib}/$LIBNAME $RPM_BUILD_ROOT%{_libdir}/%{name}.so

# Move the pkgconfig file
mv $RPM_BUILD_ROOT/%{_lib}/pkgconfig $RPM_BUILD_ROOT%{_libdir}

# Remove a couple things so they don't get picked up
rm -f $RPM_BUILD_ROOT/%{_lib}/libcap-ng.la
rm -f $RPM_BUILD_ROOT/%{_lib}/libcap-ng.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/_capng.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/_capng.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING.LIB
%attr(0755,root,root) /%{_lib}/libcap-ng.so.*

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_includedir}/cap-ng.h
%attr(0755,root,root) %{_libdir}/libcap-ng.so
%attr(0644,root,root) %{_datadir}/aclocal/cap-ng.m4
%{_libdir}/pkgconfig/libcap-ng.pc

%files python
%defattr(-,root,root,-)
%attr(755,root,root) /%{_libdir}/python?.?/site-packages/_capng.so
%{python_sitearch}/capng.py*

%files utils
%defattr(-,root,root,-)
%doc COPYING
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man8/*

%changelog
* Fri Nov 05 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-3.el6.1
resolves: #650131 - filecap segfaults

* Thu Jun 17 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-3
resolves: #595673 - Crash in kernel by running 'filecap /dev/watchdog'

* Mon May 24 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-2
resolves: #593635 - Capabilities can't be set on just a thread
- Fix requires for the utils subpackage

* Wed Apr 28 2010 Steve Grubb <sgrubb@redhat.com> 0.6.2-5
resolves: #580708 - filecap shows full capabilities if file has any

* Tue Feb 16 2010 Steve Grubb <sgrubb@redhat.com> 0.6.2-4
- Use global macro and require pkgconfig for devel subpackage

* Fri Oct 09 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-3
- Apply patch to retain setpcap only if clearing bounding set

* Sat Oct 03 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-2
- Apply patch correcting pscap and netcap acct detection

* Mon Sep 28 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-1
- New upstream release

* Sun Jul 26 2009 Steve Grubb <sgrubb@redhat.com> 0.6.1-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Steve Grubb <sgrubb@redhat.com> 0.6-1
- New upstream release

* Sun Jun 21 2009 Steve Grubb <sgrubb@redhat.com> 0.5.1-1
- New upstream release

* Fri Jun 19 2009 Steve Grubb <sgrubb@redhat.com> 0.5-1
- New upstream release

* Fri Jun 12 2009 Steve Grubb <sgrubb@redhat.com> 0.4.2-1
- New upstream release

* Fri Jun 12 2009 Steve Grubb <sgrubb@redhat.com> 0.4.1-1
- Initial build.

