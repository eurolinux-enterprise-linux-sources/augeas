Name:           augeas
Version:        1.4.0
Release:        6%{?dist}.1
Summary:        A library for changing configuration files

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://augeas.net/
Source0:        http://download.augeas.net/%{name}-%{version}.tar.gz
Patch1:         0001-Syslog-restored-Augeas-1.1.0-tree-compatibility-for-.patch
Patch2:         0002-Revert-Use-Quote-module-in-dovecot.patch
Patch3:         0003-Revert-Jaas-add-several-improvements-to-cover-more-v.patch
Patch4:         0004-UpdateDB-autoload-etc-updatedb.conf-with-Simplevars.patch
Patch5:         0005-Revert-Dnsmasq-add-structure-to-address-and-server-o.patch
Patch6:         0006-Sshd-revert-Sshd-module-to-1.1.0-compatible-add-Sshd.patch
Patch7:         0007-Dhcpd-revert-Dhcpd-module-to-1.1.0-compatible-add-Dh.patch
Patch8:         0008-Slapd-revert-Slapd-module-to-1.1.0-compatible-add-Sl.patch
Patch9:         0009-Rhsm-new-lens-to-parse-subscription-manager-s-rhsm.c.patch
Patch10:        0010-Fix-sudoers-lens-recognize-match_group_by_gid.patch
Patch11:        0011-src-pathx.c-parse_name-correctly-handle-trailing-whi.patch
Patch12:        0012-tests-test-save.c-testSaveNoPermission-skip-when-roo.patch
Patch13:        0013-Chrony-allow-signed-numbers.patch
Patch14:        0014-Fix-430-support-Krb5-include-dir.patch
Patch15:        0015-Cgconfig-allow-fperm-dperm-in-admin-task.patch
Patch16:        0016-Grub-handle-top-level-boot-directive-494.patch
Patch17:        0017-Fstab-allow-leading-whitespace-in-lines-with-spec-54.patch
Patch18:        0018-Fix-sudoers-lens-always_query_group_plugin-588.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  readline-devel libselinux-devel libxml2-devel
BuildRequires:  autoconf, automake
Requires:       %{name}-libs = %{version}-%{release}

%description
A library for programmatically editing configuration files. Augeas parses
configuration files into a tree structure, which it exposes through its
public API. Changes made through the API are written back to the initially
read files.

The transformation works very hard to preserve comments and formatting
details. It is controlled by ``lens'' definitions that describe the file
format and the transformation into a tree.

This package attempts to be compatible with Augeas 1.1.0 as shipped in
EL7.0, where possible.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries

%description    libs
The libraries for %{name}.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

# Patches affect Makefile.am and configure.ac, so rerun autotools.
autoreconf
autoconf

%build
%configure --disable-static
make %{?_smp_mflags}

%check
# Disable test-preserve.sh SELinux testing. This fails when run under mock due
# to differing SELinux labelling.
export SKIP_TEST_PRESERVE_SELINUX=1

make %{?_smp_mflags} check || {
  echo '===== tests/test-suite.log ====='
  cat tests/test-suite.log
  exit 1
}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# The tests/ subdirectory contains lenses used only for testing, and
# so it shouldn't be packaged.
rm -r $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/dist/tests

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/augtool
%{_bindir}/augparse
%{_bindir}/fadot
%doc %{_mandir}/man1/*
%{_datadir}/vim/vimfiles/syntax/augeas.vim
%{_datadir}/vim/vimfiles/ftdetect/augeas.vim

%files libs
%defattr(-,root,root,-)
# %{_datadir}/augeas and %{_datadir}/augeas/lenses are owned
# by filesystem.
%{_datadir}/augeas/lenses/dist
%{_libdir}/*.so.*
%doc AUTHORS COPYING NEWS

%files devel
%defattr(-,root,root,-)
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/augeas.pc

%changelog
* Thu Nov 15 2018 Pino Toscano <ptoscano@redhat.com> - 1.4.0-6.el7_6.1
- Sudoers: handle "always_query_group_plugin" option (RHBZ#1650174)

* Thu Mar 29 2018 Pino Toscano <ptoscano@redhat.com> - 1.4.0-6
- Fstab: allow leading whitespaces (RHBZ#1544520)

* Wed Oct 04 2017 Pino Toscano <ptoscano@redhat.com> - 1.4.0-5
- Cgconfig: allow fperm & dperm in admin & task (RHBZ#1325741)
- Grub: handle top-level "boot" directive (RHBZ#1484261)

* Mon Sep 04 2017 Pino Toscano <ptoscano@redhat.com> - 1.4.0-4
- Fix CVE-2017-7555, improper handling of escaped strings (RHBZ#1481546)
- Skip testSaveNoPermission when running as root (RHBZ#1269817)
- Chrony: allow signed numbers (RHBZ#1302017)
- Krb5: support includedir (RHBZ#1406111)

* Tue Aug 29 2017 Luigi Toscano <ltoscano@redhat.com> - 1.4.0-3
  Fix sudoers lens: recognize "match_group_by_gid" (RHBZ#1483888)

* Thu Jul 30 2015 Dominic Cleal <dcleal@redhat.com> - 1.4.0-2
- Rhsm: add to parse subscription-manager config (RHBZ#1141121)

* Fri Jun 12 2015 Dominic Cleal <dcleal@redhat.com> - 1.4.0-1
- Rebase to Augeas 1.4.0
- Revert some changes for better compatibility with 1.1.0-17:
  * Dhcpd: keep 1.1.0 behaviour, add Dhcpd_140 for 1.4.0 features
  * Dnsmasq: revert splitting of address/server options
  * Dovecot: restore quotes within values
  * Jaas: revert semicolon and line break changes
  * Slapd: keep 1.1.0 behaviour, add Slapd_140 for 1.4.0 features
  * Sshd: keep 1.1.0 behaviour, add Sshd_140 for 1.4.0 features
  * Syslog: restore tree without protocol for UDP hosts
  * UpdateDB: keep Simplevars to load config by default

* Thu Nov 27 2014 Dominic Cleal <dcleal@redhat.com> - 1.1.0-17
- Device_map: parse all device.map files under /boot (RHBZ#1166582)

* Tue Sep 23 2014 Dominic Cleal <dcleal@redhat.com> - 1.1.0-16
- Iptables: parse /etc/sysconfig/iptables.save (RHBZ#1144651)
- Lvm: parse /etc/lvm/lvm.conf (RHBZ#1145495)
- Shadow: add lens (RHBZ#1145249)

* Thu Sep 18 2014 Dominic Cleal <dcleal@redhat.com> - 1.1.0-15
- Remove man/augtool.1 patches, always create .1 during build (RHBZ#1143954)

* Thu Sep 18 2014 Dominic Cleal <dcleal@redhat.com> - 1.1.0-14
- Kdump: parse new options, EOL comments (RHBZ#1139298)
- Rsyslog: parse property filters and templates (RHBZ#1138402)
- Systemd: parse semicolons inside entry values (RHBZ#1139498)
- Systemd: parse environment variables where value is quoted (RHBZ#1138508)

* Thu Sep 04 2014 Dominic Cleal <dcleal@redhat.com> - 1.1.0-13
- aug_save: return error when unlink fails (RHBZ#1091143)
- augtool: add aliases to autocomplete (RHBZ#1100076)
- augtool: remove unused dump-xml arg (RHBZ#1100106)
- Automounter: parse hostnames with hyphens (RHBZ#1075162)
- Cgconfig: parse other valid controllers (RHBZ#1112543)
- Chrony: add lens (RHBZ#1071947)
- docs: update man page with new commands (RHBZ#1100077)
- Exports: permit colons for IPv6 client addresses (RHBZ#1067030)
- Httpd: parse continued, quoted lines (RHBZ#1100551)
- Ldso: parse hwcap lines (RHBZ#1102629)
- NagiosCfg: parse nrpe.cfg with Nrpe (RHBZ#1102623)
- Rmt: add lens (RHBZ#1100549)
- Services: permit colons in service name (RHBZ#1121527)
- Shellvars: support arithmetic expansion (RHBZ#1100550)
- Syslog: parse TCP loghosts (RHBZ#1129386)
- Syslog: parse IPv6 loghost addresses (RHBZ#1129388)
- Systemd: parse /etc/sysconfig/*.systemd (RHBZ#1083022)
- Systemd: parse quoted environment vars (RHBZ#1100547)

* Tue Feb 25 2014 Dominic Cleal <dcleal@redhat.com> - 1.1.0-12
- Add patch for Dovecot, mailbox and quote support (RHBZ#1064387)
- Add patch for Keepalived, virtual server fixes (RHBZ#1064388)
- Add patch for Krb5, parse braces in values (RHBZ#1066419)

* Thu Feb 20 2014 Dominic Cleal <dcleal@redhat.com> - 1.1.0-11
- Add patch for Yum, split exclude lines (RHBZ#1067039)

* Tue Feb 18 2014 Dominic Cleal <dcleal@redhat.com> - 1.1.0-10
- Add patch for IPRoute2, hex and hyphen protocols (RHBZ#1063961)
- Add patch for IPRoute2, slashes in protocols (RHBZ#1063968)

* Mon Feb 10 2014 Dominic Cleal <dcleal@redhat.com> - 1.1.0-9
- Add patch for yum-cron.conf incl entry (RHBZ#1058409)
- Add patch for firewalld.conf incl entry (RHBZ#1058411)
- Add patch for Grub, foreground option (RHBZ#1059426)
- Add patch for Yum, spaces around equals (RHBZ#1062614)
- Add patch for Shellvars, case and same-line ;; (RHBZ#1056541)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.1.0-8
- Mass rebuild 2014-01-24

* Tue Jan 14 2014 Dominic Cleal <dcleal@redhat.com> - 1.1.0-7
- Fix CVE-2013-6412, incorrect permissions under strict umask (RHBZ#1036081)

* Thu Jan 02 2014 Dominic Cleal <dcleal@redhat.com> - 1.1.0-6
- Add patch for Sysconfig module, empty comment lines (RHBZ#1043665)
- Add check section to run test suite
- Add patch for testPermsErrorReported test, when root (RHBZ#1043666)
- Add patch for Shellvars, multivariable exports (RHBZ#1043815)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.0-5
- Mass rebuild 2013-12-27

* Tue Nov 19 2013 Dominic Cleal <dcleal@redhat.com> - 1.1.0-4
- Add patch for saving files with // in incl path (RHBZ#1031084)

* Tue Oct 22 2013 Dominic Cleal <dcleal@redhat.com> - 1.1.0-3
- Add patch for Grub module, setkey/lock support (RHBZ#1019485)

* Mon Aug 12 2013 Dominic Cleal <dcleal@redhat.com> - 1.1.0-2
- Fix source URL to download.augeas.net (RHBZ#996033)

* Wed Jun 19 2013 David Lutterkort <lutter@redhat.com> - 1.1.0-1
- Update to 1.1.0; remove all patches

* Tue Jun 18 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-4
- Fix /etc/sysconfig/network (RHBZ#904222).

* Wed Jun  5 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-3
- Don't package lenses in tests/ subdirectory.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 David Lutterkort <lutter@redhat.com> - 1.0.0-1
- New version; remove all patches

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 David Lutterkort <lutter@redhat.com> - 0.10.0-3
- Add patches for bugs 247 and 248 (JSON lens)

* Sat Dec  3 2011 Richard W.M. Jones <rjones@redhat.com> - 0.10.0-2
- Add patch to resolve missing libxml2 requirement in augeas.pc.

* Fri Dec  2 2011 David Lutterkort <lutter@redhat.com> - 0.10.0-1
- New version

* Mon Jul 25 2011 David Lutterkort <lutter@redhat.com> - 0.9.0-1
- New version; removed patch pathx-whitespace-ea010d8

* Tue May  3 2011 David Lutterkort <lutter@redhat.com> - 0.8.1-2
- Add patch pathx-whitespace-ea010d8.patch to fix BZ 700608

* Fri Apr 15 2011 David Lutterkort <lutter@redhat.com> - 0.8.1-1
- New version

* Wed Feb 23 2011 David Lutterkort <lutter@redhat.com> - 0.8.0-1
- New version

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Matthew Booth <mbooth@redhat.com> - 0.7.4-1
- Update to version 0.7.4

* Thu Nov 18 2010 Richard W.M. Jones <rjones@redhat.com> - 0.7.3-2
- Upstream patch proposed to fix GCC optimization bug (RHBZ#651992).

* Fri Aug  6 2010 David Lutterkort <lutter@redhat.com> - 0.7.3-1
- Remove upstream patches

* Tue Jun 29 2010 David Lutterkort <lutter@redhat.com> - 0.7.2-2
- Patches based on upstream fix for BZ 600141

* Tue Jun 22 2010 David Lutterkort <lutter@redhat.com> - 0.7.2-1
- Fix ownership of /usr/share/augeas. BZ 569393

* Wed Apr 21 2010 David Lutterkort <lutter@redhat.com> - 0.7.1-1
- New version

* Thu Jan 14 2010 David Lutterkort <lutter@redhat.com> - 0.7.0-1
- Remove patch vim-ftdetect-syntax.patch. It's upstream

* Tue Dec 15 2009 David Lutterkort <lutter@redhat.com> - 0.6.0-2
- Fix ftdetect file for vim

* Mon Nov 30 2009 David Lutterkort <lutter@redhat.com> - 0.6.0-1
- Install vim syntax files

* Mon Sep 14 2009 David Lutterkort <lutter@redhat.com> - 0.5.3-1
- Remove separate xorg.aug, included in upstream source

* Tue Aug 25 2009 Matthew Booth <mbooth@redhat.com> - 0.5.2-3
- Include new xorg lens from upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 David Lutterkort <lutter@redhat.com> - 0.5.2-1
- New version

* Fri Jun  5 2009 David Lutterkort <lutter@redhat.com> - 0.5.1-1
- Install fadot

* Fri Mar 27 2009 David Lutterkort <lutter@redhat.com> - 0.5.0-2
- fadot isn't being installed just yet

* Tue Mar 24 2009 David Lutterkort <lutter@redhat.com> - 0.5.0-1
- New program /usr/bin/fadot

* Mon Mar  9 2009 David Lutterkort <lutter@redhat.com> - 0.4.2-1
- New version

* Fri Feb 27 2009 David Lutterkort <lutter@redhat.com> - 0.4.1-1
- New version

* Fri Feb  6 2009 David Lutterkort <lutter@redhat.com> - 0.4.0-1
- New version

* Mon Jan 26 2009 David Lutterkort <lutter@redhat.com> - 0.3.6-1
- New version

* Tue Dec 23 2008 David Lutterkort <lutter@redhat.com> - 0.3.5-1
- New version

* Mon Feb 25 2008 David Lutterkort <dlutter@redhat.com> - 0.0.4-1
- Initial specfile
