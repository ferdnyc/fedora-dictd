Summary: DICT protocol (RFC 2229) command-line client
Name: dictd
Version: 1.9.7
Release: 1
License: GPL
Group: Applications/Internet
Source0: ftp://ftp.dict.org/pub/dict/%{name}-%{version}.tar.gz
URL: http://www.dict.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: flex
BuildRequires: bison

%description
Command-line client for the DICT protocol.  The Dictionary Server
Protocol (DICT) is a TCP transaction based query/response protocol that
allows a client to access dictionary definitions from a set of natural
language dictionary databases.

%prep
%setup -q

%build
%configure --with-cflags="$RPM_OPT_FLAGS"
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc ANNOUNCE COPYING ChangeLog README doc/rfc2229.txt doc/security.doc
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/libdictdplugin.a
%{_includedir}/*
%{_mandir}/man?/*

%changelog
* Wed Jun 02 2004 Karsten Hopp <karsten@redhat.de> 1.9.7-1 
- update

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 18 2002 Tim Powers <timp@redhat.com>
- build on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Mar 26 2000 Philip Copeland <bryce@redhat.com> 1.5.5-1
- initial rpm version
