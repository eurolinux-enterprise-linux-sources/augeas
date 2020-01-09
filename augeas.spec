Name:           augeas
Version:        1.0.0
Release:        7%{?dist}
Summary:        A library for changing configuration files

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://augeas.net/
Source0:        http://augeas.net/download/%{name}-%{version}.tar.gz
Patch1:         0001-Shellvars-reinstate-etc-sysconfig-network.patch
Patch2:         0002-tests-test-run.c-load_module-do-not-downcase-the-len.patch
Patch3:         0003-Fix-umask-handling-when-creating-new-files.patch
Patch4:         0004-Grub-support-the-setkey-directive.patch
Patch5:         0005-Added-support-for-ActiveMQ-Red-Hat-JBoss-A-MQ.patch
Patch6:         0006-Add-Splunk-lens.patch
Patch7:         0007-Sudoers-Allow-user-aliases-in-specs.patch
Patch8:         0008-tests-test-load.c-testPermsErrorReported-skip-permis.patch
Patch9:         0009-RHBZ-1033795-RHEL-6-compatible-multiple-exports-fix.patch
Patch10:        0010-Shellvars-handle-case-statements-with-same-line-toke.patch
Patch11:        0011-Sysconfig-permit-empty-comments-after-comment-lines.patch
Patch12:        0012-Grub-handle-foreground-option.patch
Patch13:        0013-Yum-permit-spaces-after-equals-sign-in-list-options.patch
Patch14:        0014-IniFile-Add-ready-to-use-lns_loose-and-lns_loose_mul.patch
Patch15:        0015-Fixes-27-Automounter-lens-does-not-handle-hostnames-.patch
Patch16:        0016-Rsyslog-parse-property-filters-and-file-actions-with.patch
Patch17:        0017-Ldso-handle-hwcap-lines.patch
Patch18:        0018-Sudoers-permit-underscores-in-group-names.patch
Patch19:        0019-man-augtool.pod-update-man-page-with-new-commands.patch
Patch20:        0020-src-augrun.c-remove-unused-filename-argument-from-du.patch
Patch21:        0021-src-augtool.c-add-command-aliases-to-autocomplete.patch
Patch22:        0022-Nrpe-accept-any-config-option-remove-predefined-list.patch
Patch23:        0023-man-augtool.pod-fix-description-of-move-alias.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  readline-devel libselinux-devel libxml2-devel
Requires:       %{name}-libs = %{version}-%{release}

%description
A library for programmatically editing configuration files. Augeas parses
configuration files into a tree structure, which it exposes through its
public API. Changes made through the API are written back to the initially
read files.

The transformation works very hard to preserve comments and formatting
details. It is controlled by ``lens'' definitions that describe the file
format and the transformation into a tree.

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
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%check
# Disable test-preserve.sh. This fails when run under mock due to differing
# SELinux labelling.
cat > tests/test-preserve.sh <<EOF
#!/bin/sh
true
EOF

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
* Fri Jun 13 2014 Dominic Cleal <dcleal@redhat.com> - 1.0.0-7
* docs: fix description of 'move' alias (RHBZ#1100186)

* Tue Jun 03 2014 Dominic Cleal <dcleal@redhat.com> - 1.0.0-6
- Fix CVE-2013-6412, incorrect permissions under strict umask (RHBZ#1036080)
- Grub: support 'setkey' and 'lock' directives (RHBZ#1001635)
- ActiveMQ: add ActiveMQ lens (RHBZ#1016899)
- Splunk: add Splunk lens (RHBZ#1016900)
- Sudoers: user aliases fail to parse (RHBZ#1016904)
- Tests: testPermsError during compilation (RHBZ#1024275)
- Shellvars: multi-variable export lines (RHBZ#1033795)
- Shellvars: case statements with same-line ;; tokens (RHBZ#1033799)
- Sysconfig: permit empty comments (RHBZ#1043636)
- Grub: support 'foreground' directive (RHBZ#1059383)
- Yum: permit space after equals sign (RHBZ#1062091)
- IniFile: add generic INI lenses (RHBZ#1073072)
- Automounter: permit hostnames with hyphens (RHBZ#1075112)
- Rsyslog: parse property filters and templates (RHBZ#1083016)
- Ldso: parse hwcap lines (RHBZ#1083021)
- Sudoers: permit underscores in group names (RHBZ#1093711)
- augtool: remove dump-xml filename arg (RHBZ#1100182)
- augtool: add commands to autocomplete (RHBZ#1100184)
- docs: update command and arg lists (RHBZ#1100186)
- Nrpe: parse unknown config options (RHBZ#1100237)

* Wed Jun  5 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-5
- Don't package lenses in tests/ subdirectory.
  related: rhbz#817753

* Fri May 17 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-4
- Rebase to Augeas 1.0.0
  resolves: rhbz#817753
- Add dependency on libxml2-devel.
- Remove all patches (all upstream and included in 1.0.0).
- Print tests/test-suite.log when the tests fail.
- Add fix for regression added in 1.0.0 (RHBZ#920609).
- Fix tests/test-run.

* Fri May 11 2012 Matthew Booth <mbooth@redhat.com> - 0.9.0-4
- Handle fstab options with empty values (RHBZ#820864)
- Run make check during rpm build

* Tue Apr 17 2012 Matthew Booth <mbooth@redhat.com> - 0.9.0-3
- Add mdadm_conf.lens (RHBZ#808662)

* Thu Mar  1 2012 David Lutterkort <lutter@redhat.com> - 0.9.0-2
- Fix BZ 781690 "Grub password --encrypted argument not parsed correctly"
- Fix BZ 628507 "It's better to support fadot --help or fadot -h"
- Fix BZ 759311 "augtool --autosave does not save changes"

* Mon Jul 25 2011 David Lutterkort <lutter@redhat.com> - 0.9.0-1
- Rebased to new version; removed all patches

* Thu Mar 24 2011 David Lutterkort <lutter@redhat.com> - 0.7.2-6
- Add patch with regenerated lexer/parser for BZ 690286

* Thu Mar 24 2011 David Lutterkort <lutter@redhat.com> - 0.7.2-5
- Do not leak fd's when used from multiple threads. BZ 690286

* Fri Jan  1 2011 Matthew Booth <mbooth@redhat.com> - 0.7.2-4
- Include the lens for grub's device.map. BZ 609448

* Tue Aug 10 2010 Matthew Booth <mbooth@redhat.com> - 0.7.2-3
- Fix crash when reloading externally modified file. BZ 613967

* Tue Jun 29 2010 David Lutterkort <lutter@redhat.com> - 0.7.2-2
- Patches based on upstream fix for BZ 600141

* Tue Jun 22 2010 David Lutterkort <lutter@redhat.com> - 0.7.2-1
- Fix ownership of /usr/share/augeas. BZ 569393

* Wed Apr 21 2010 David Lutterkort <lutter@redhat.com> - 0.7.1-1
- New version

* Thu Jan 14 2010 David Lutterkort <lutter@redhat.com> - 0.7.0-1
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
