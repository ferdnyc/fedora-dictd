%global _hardened_build 1
# User management -- https://fedoraproject.org/wiki/PackageUserCreation
%bcond_without      fedora
# Need to register in https://fedoraproject.org/wiki/PackageUserRegistry
%global uid     52
# Do no change username -- hardcoded in dictd.c
%global username    dictd
%global homedir     %{_datadir}/dict/dictd
%global gecos       dictd dictionary server
%define libmaaVersion 1.3.2

Summary:   DICT protocol (RFC 2229) server and command-line client
Name:      dictd
Version:   1.12.1
Release:   7%{?dist}
License:   GPL+ and zlib and MIT
Group:     Applications/Internet
Source0:   http://downloads.sourceforge.net/dict/%{name}-%{version}.tar.gz
Source1:   dictd.service
Source2:   libmaa-%{libmaaVersion}.tar.gz
Patch0:    dictd-1.12.1-unused-return.patch
URL:       http://www.dict.org/

BuildRequires:  flex bison libtool libtool-ltdl-devel byacc
BuildRequires:  libdbi-devel, zlib-devel, gawk, systemd
Requires(pre):  shadow-utils

%description
Command-line client for the DICT protocol.  The Dictionary Server
Protocol (DICT) is a TCP transaction based query/response protocol that
allows a client to access dictionary definitions from a set of natural
language dictionary databases.

%package server
Summary: Server for the Dictionary Server Protocol (DICT)
Group: System Environment/Daemons
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%description server
A server for the DICT protocol. You need to install dictd-usable databases
before you can use this server. Those can be found p.e. at 
ftp://ftp.dict.org/pub/dict/pre/
More information can be found in the INSTALL file in this package.

%prep
%setup -q
tar xzf %{SOURCE2}
mv libmaa-%{libmaaVersion} libmaa
%patch0 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export LDFLAGS="%{?__global_ldflags}" CPPFLAGS="$RPM_OPT_FLAGS -fPIC"
pushd libmaa
# Required for aarch64 support:
%configure
make %{?_smp_mflags}
popd

export LDFLAGS="%{?__global_ldflags} -Llibmaa/.libs" CPPFLAGS="-Ilibmaa $RPM_OPT_FLAGS -fPIC"
%configure --enable-dictorg --disable-plugin
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{homedir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/dictd.service

cat <<EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/dictd
# Secure by default: --listen-to 127.0.0.1
# Remove this option if you want dictd to answer remote clients.
DICTD_FLAGS='--listen-to 127.0.0.1'
EOF
cat <<EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/dictd.conf
global {
    #syslog
    #syslog_facility daemon
}

# Add database definitions here...

# We stop the search here
database_exit

# Add hidden database definitions here...

EOF


%post server
%systemd_post dictd.service

%preun server
%systemd_preun dictd.service

%postun server
%systemd_postun_with_restart dictd.service 

%pre
getent group %{username} >/dev/null || groupadd -r %{username} -g %{uid}
getent passwd %{username} >/dev/null || \
    useradd -r -g %{username} -d %{homedir} -s /sbin/nologin -u %{uid} \
    -c '%{gecos}' %{username}
exit 0


%files
%doc ANNOUNCE COPYING ChangeLog README doc/rfc2229.txt doc/security.doc
%doc examples/dict1.conf
%{_bindir}/dict
%{_mandir}/man1/dict.1*


%files server
%doc ANNOUNCE COPYING INSTALL ChangeLog README doc/rfc2229.txt doc/security.doc
%doc examples/dictd*
%exclude %{_mandir}/man1/dict.1*
%exclude %{_bindir}/dict
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man?/*
%{_unitdir}/dictd.service
%{homedir}
%config(noreplace) %{_sysconfdir}/sysconfig/dictd
%config(noreplace) %{_sysconfdir}/dictd.conf

%changelog
* Wed Jun 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.12.1-7
- %%configure macro updates config.guess/sub for new arches (aarch64/ppc64le)
- Update systemd scriptlets to latest standard
- General cleanups

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Karsten Hopp <karsten@redhat.com> 1.12.1-5
- used hardened build flag to enable PIE (rhbz 955198)

* Mon Aug 05 2013 Karsten Hopp <karsten@redhat.com> 1.12.1-3
- add BR: systemd-units for the _unitdir macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 22 2013 Karsten Hopp <karsten@redhat.com> 1.12.1-1
- update to 1.12.1
- add support for aarch64 (#925252)

* Wed Apr 10 2013 Jon Ciesla <limburgher@gmail.com> - 1.12.0-6
- Migrate from fedora-usermgmt to guideline scriptlets.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 14 2012 Jon Ciesla <limburgher@gmail.com> - 1.12.0-3
- Migrate to systemd, BZ 772085.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 04 2011 Karsten Hopp <karsten@redhat.com> 1.12.0-1
- update to version 1.12.0
- split into server and client packages
- add most of Oron Peled's <oron@actcom.co.il> changes from 
  https://bugzilla.redhat.com/attachment.cgi?id=381332
  - The daemon now runs as 'dictd' user. This user is added/remove
    during install/uninstall.
  - Create and own a default configuration file
  - By default listen only on 127.0.0.1 (secure by default)
  - Default directory for dictionaries (datadir) is
    now /usr/share/dict/dictd and not /usr/share
  - Add the examples directory to the documentation

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

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

* Sun Mar 26 2000 Philip Copeland <bryce@redhat.com> 1.5.5-1
- initial rpm version
