Summary: DICT protocol (RFC 2229) command-line client
Name: dictd
Version: 1.9.7
Release: 5
License: GPL
Group: Applications/Internet
Source0: ftp://ftp.dict.org/pub/dict/%{name}-%{version}.tar.gz
Source1: dictd.init
Patch0:  dictd-1.9.7-gcc34.patch
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
%patch0 -p1 -b .gcc34

%build
%configure --with-cflags="$RPM_OPT_FLAGS"
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/usr/bin,/etc/init.d,/etc/sysconfig}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
make install DESTDIR=$RPM_BUILD_ROOT
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/etc/init.d/dictd
install -m 644 dictd.conf $RPM_BUILD_ROOT/etc/dictd.conf
echo "DICTD_FLAGS=" > $RPM_BUILD_ROOT/etc/sysconfig/dictd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 = 1 ]; then
   /sbin/chkconfig --add dictd
fi

%preun
if [ $1 = 0 ]; then
   /sbin/chkconfig --del dictd
fi

%files
%defattr(-,root,root,0755)
%doc ANNOUNCE COPYING ChangeLog README doc/rfc2229.txt doc/security.doc
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/libdictdplugin.a
%{_includedir}/*
%{_mandir}/man?/*
/etc/init.d/*
%config(noreplace) /etc/sysconfig/dictd

%changelog
* Tue Jan 25 2005 Karsten Hopp <karsten@redhat.de> 1.9.7-5 
- don't install config file, leave it to the dictionary packages to
  populate it. (#135920)

* Mon Oct 04 2004 Karsten Hopp <karsten@redhat.de> 1.9.7-4 
- add initscript

* Sat Jun 19 2004 Karsten Hopp <karsten@redhat.de> 1.9.7-3 
- fix build with gcc34

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

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
