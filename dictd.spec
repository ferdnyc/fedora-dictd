%define libmaaVersion 1.1.0
Summary:   DICT protocol (RFC 2229) command-line client
Name:      dictd
Version:   1.11.0
Release:   4%{?dist}
License:   GPL+ and zlib and MIT
Group:     Applications/Internet
Source0:   http://downloads.sourceforge.net/dict/%{name}-%{version}.tar.gz
Source1:   dictd.init
Source2:   libmaa-%{libmaaVersion}.tar.gz
URL:       http://www.dict.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post):  chkconfig
Requires(preun): chkconfig
Requires(postun): initscripts
BuildRequires:   flex bison libtool libtool-libs libtool-ltdl-devel byacc
BuildRequires:   libdbi-devel, zlib-devel, gawk

%description
Command-line client for the DICT protocol.  The Dictionary Server
Protocol (DICT) is a TCP transaction based query/response protocol that
allows a client to access dictionary definitions from a set of natural
language dictionary databases.

%prep
%setup -q
tar xzf %{SOURCE2}
mv libmaa-%{libmaaVersion} libmaa

%build
%configure --with-cflags="$RPM_OPT_FLAGS" --enable-dictorg --disable-plugin \
            --with-local-libmaa
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/dictd
echo "DICTD_FLAGS=" > $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/dictd

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

%postun
if [ $1 -ge 1 ] ; then
   /sbin/service dictd condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc ANNOUNCE COPYING ChangeLog README doc/rfc2229.txt doc/security.doc
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man?/*
%{_sysconfdir}/rc.d/init.d/*
%config(noreplace) %{_sysconfdir}/sysconfig/dictd

%changelog
* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Karsten Hopp <karsten@redhat.com> 1.11.0-3
- add disttag

* Thu Jan 22 2009 Karsten Hopp <karsten@redhat.com> 1.11.0-2
- add postun script (#225694)
- fix file permissions (defattr)

* Wed Jan 14 2009 Karsten Hopp <karsten@redhat.com> 1.11.0-1
- update

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.10.11-3
- fix license tag

* Wed May 07 2008 Karsten Hopp <karsten@redhat.com> 1.10.11-2
- update to 1.10.11

* Tue Apr 01 2008 Karsten Hopp <karsten@redhat.com> 1.10.10-1
- fix typo (#281981)
- update

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.10.9-2
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Karsten Hopp <karsten@redhat.com> 1.10.9-1
- new upstream version

* Wed Aug 22 2007 Karsten Hopp <karsten@redhat.com> 1.9.15-11
- update license tag and rebuild

* Mon Aug 13 2007 Karsten Hopp <karsten@redhat.com> 1.9.15-10
- add LSB stuff (#246910)

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 1.9.15-9
- misc. merge review fixes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.9.15-8.1
- rebuild

* Mon May 22 2006 Karsten Hopp <karsten@redhat.de> 1.9.15-8
- buildrequires zlib-devel

* Thu May 18 2006 Karsten Hopp <karsten@redhat.de> 1.9.15-7
- Buildrequires: libdbi-devel

* Mon Feb 20 2006 Karsten Hopp <karsten@redhat.de> 1.9.15-6
- BuildRequires: byacc

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.9.15-5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.9.15-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 02 2006 Karsten Hopp <karsten@redhat.de> 1.9.15-5
- add BuildRequires libtool-ltdl-devel (#176505)

* Tue Dec 20 2005 Karsten Hopp <karsten@redhat.de> 1.9.15-4
- consult dict.org if no server is specified on the commandline
  (#176038)

* Mon Dec 12 2005 Karsten Hopp <karsten@redhat.de> 1.9.15-3
- rebuild with gcc-4.1

* Tue Jul 12 2005 Karsten Hopp <karsten@redhat.de> 1.9.15-2
- Buildrequires libtool (ltdl.h)

* Wed Jul 06 2005 Karsten Hopp <karsten@redhat.de> 1.9.15-1
- update to dictd-1.9.15
- drop gcc34 patch

* Mon May 02 2005 Karsten Hopp <karsten@redhat.de> 1.9.7-9
- use _bindir / _sysconfdir macros

* Sat Apr 02 2005 Florian La Roche <laroche@redhat.com>
- /etc/init.d -> /etc/rc.d/init.d


* Thu Mar 10 2005 Bill Nottingham <notting@redhat.com> 1.9.7-7
- prereq chkconfig

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.9.7-6
- build with gcc-4

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
