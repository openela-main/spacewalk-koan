%if 0%{?fedora} || 0%{?suse_version} > 1320 || 0%{?rhel} >= 8
%global build_py3   1
%global default_py3 1
%endif

%if ( 0%{?fedora} && 0%{?fedora} < 28 ) || ( 0%{?rhel} && 0%{?rhel} < 8 )
%global build_py2   1
%endif

%define pythonX %{?default_py3: python3}%{!?default_py3: python2}

Summary: Support package for spacewalk koan interaction
Name: spacewalk-koan
Version: 2.8.6
Release: 7%{?dist}
License: GPLv2
Source0: https://github.com/spacewalkproject/spacewalk/archive/%{name}-%{version}.tar.gz
Patch0: spacewalk-koan-2.8.6-1-to-spacewalk-koan-2.8.6-2-el8.patch
Patch1: spacewalk-koan-2.8.6-2-el8-to-spacewalk-koan-2.8.6-3-el8.patch
Patch2: spacewalk-koan-2.8.6-3-el8-to-spacewalk-koan-2.8.6-4-el8.patch
Patch3: spacewalk-koan-2.8.6-4-el8-to-spacewalk-koan-2.8.6-5-el8.patch
Patch4: spacewalk-koan-2.8.6-5-el8-to-spacewalk-koan-2.8.6-6-el8.patch
Patch5: spacewalk-koan-2.8.6-6-el8-to-spacewalk-koan-2.8.6-7-el8.patch
URL:            https://github.com/spacewalkproject/spacewalk
BuildArch:      noarch
Requires:       %{pythonX}-%{name} = %{version}-%{release}
Requires:       koan
# dd, du
Requires:       coreutils
Requires:       cpio
Requires:       e2fsprogs
# gzip, zcat
Requires:       gzip
Requires:       tar
# mount, umount
Requires:       util-linux
Requires:       xz
Conflicts: rhn-kickstart
Conflicts: rhn-kickstart-common
Conflicts: rhn-kickstart-virtualization

Requires: rhn-check

%description
Support package for spacewalk koan interaction.

%if 0%{?build_py2}
%package -n python2-%{name}
Summary: Support package for spacewalk koan interaction
%{?python_provide:%python_provide python2-%{name}}
BuildRequires:  python
Requires:       python
%if 0%{?suse_version}
# provide directories for filelist check in OBS
BuildRequires: rhn-client-tools
%endif
%description -n python2-%{name}
Python 2 specific files for %{name}.
%endif

%if 0%{?build_py3}
%package -n python3-%{name}
Summary: Support package for spacewalk koan interaction
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3
BuildRequires:  python3-rpm-macros
%{?__python3:Requires: %{__python3}}
%description -n python3-%{name}
Python 3 specific files for %{name}.
%endif

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
make -f Makefile.spacewalk-koan all

%install
%if 0%{?build_py2}
make -f Makefile.spacewalk-koan install PREFIX=$RPM_BUILD_ROOT ROOT=%{python_sitelib} \
    MANDIR=%{_mandir}
%endif

%if 0%{?build_py3}
make -f Makefile.spacewalk-koan install PREFIX=$RPM_BUILD_ROOT ROOT=%{python3_sitelib} \
    MANDIR=%{_mandir}
%endif

%if 0%{?suse_version}
%py_compile -O %{buildroot}/%{python_sitelib}
%if 0%{?build_py3}
%py3_compile -O %{buildroot}/%{python3_sitelib}
%endif
%endif


%clean

%files
%config(noreplace)  %{_sysconfdir}/sysconfig/rhn/clientCaps.d/kickstart
%{_sbindir}/*

%if 0%{?build_py2}
%files -n python2-%{name}
%{python_sitelib}/spacewalkkoan/
%{python_sitelib}/rhn/actions/
%if 0%{?suse_version}
%dir %{python_sitelib}/rhn
%endif
%endif

%if 0%{?build_py3}
%files -n python3-%{name}
%{python3_sitelib}/spacewalkkoan/
%{python3_sitelib}/rhn/actions/
%if 0%{?suse_version}
%dir %{python3_sitelib}/rhn
%endif
%endif

%changelog
* Mon May 27 2019 Michael Mraka <michael.mraka@redhat.com> 2.8.6-7
- Require the Python interpreter directly instead of using the package name

* Tue May 21 2019 Michael Mraka <michael.mraka@redhat.com> 2.8.6-6
- Resolves: #1703706 - require commands we use in merge-rd.sh

* Tue Mar 20 2018 Tomas Kasparek <tkasparek@redhat.com> 2.8.6-5
- don't build python2 subpackages on systems with default python3
  (tkasparek@redhat.com)

* Wed Mar 14 2018 Tomas Kasparek <tkasparek@redhat.com> 2.8.6-4
- build python3-spacewalk-koan (tkasparek@redhat.com)

* Wed Mar 14 2018 Tomas Kasparek <tkasparek@redhat.com> 2.8.6-3
- don't require koan20 (tkasparek@redhat.com)

* Thu Mar 08 2018 Tomas Kasparek <tkasparek@redhat.com> 2.8.6-2
- rebuild for rhel8

* Fri Feb 09 2018 Michael Mraka <michael.mraka@redhat.com> 2.8.6-1
- remove install/clean section initial cleanup
- removed Group from specfile
- removed BuildRoot from specfiles

* Mon Oct 23 2017 Michael Mraka <michael.mraka@redhat.com> 2.8.5-1
- spacewalk-koan: add missing directories to filelist on SUSE and build py3 on
  Tumbleweed

* Wed Oct 18 2017 Jan Dobes 2.8.4-1
- spacewalk-koan - removing usage of string module not available in Python 3

* Mon Oct 16 2017 Jan Dobes 2.8.3-1
- upstream koan is not compatible with cobbler20, require our build for now

* Tue Oct 10 2017 Michael Mraka <michael.mraka@redhat.com> 2.8.2-1
- install files into python_sitelib/python3_sitelib
- split spacewalk-koan into python2/python3 specific packages

* Wed Sep 06 2017 Michael Mraka <michael.mraka@redhat.com> 2.8.1-1
- purged changelog entries for Spacewalk 2.0 and older
- use standard brp-python-bytecompile
- Bumping package versions for 2.8.

* Tue Jul 18 2017 Michael Mraka <michael.mraka@redhat.com> 2.7.2-1
- move version and release before sources

* Mon Jul 17 2017 Jan Dobes 2.7.1-1
- Updated links to github in spec files
- Migrating Fedorahosted to GitHub
- Bumping package versions for 2.7.

* Mon Sep 26 2016 Jan Dobes 2.6.1-1
- embed_kickstart was renamed to embed_autoinst in koan upstream
- Bumping package versions for 2.6.

* Wed May 25 2016 Tomas Kasparek <tkasparek@redhat.com> 2.5.2-1
- updating copyright years

* Tue Apr 26 2016 Gennadii Altukhov <galt@redhat.com> 2.5.1-1
- Adapt spacewalk-koan for Python 2/3 compatibility
- Bumping package versions for 2.5.

* Wed Sep 16 2015 Jan Dobes 2.4.2-1
- 1253464 - switch to KVM if possible

* Fri May 29 2015 Jan Dobes 2.4.1-1
- fixing duplicate BuildArch
- Bumping package versions for 2.4.

* Thu Mar 19 2015 Grant Gainey 2.3.2-1
- Updating copyright info for 2015

* Fri Jan 30 2015 Stephen Herr <sherr@redhat.com> 2.3.1-1
- 1187482 - make file preservation work again with new upstream koan
- spacewalk-koan: improved merge-rd
- Bumping package versions for 2.3.

* Fri Jul 11 2014 Milan Zazrivec <mzazrivec@redhat.com> 2.2.4-1
- fix copyright years

* Fri Jun 13 2014 Stephen Herr <sherr@redhat.com> 2.2.3-1
- 1109276 - make cobbler20 guest kickstart work with new koan

* Wed Mar 26 2014 Stephen Herr <sherr@redhat.com> 2.2.2-1
- 1063409 - guest provisioned on RHEL 7 host have no graphical console
- Merge pull request #9 from dyordano/1071657

* Fri Mar 14 2014 Michael Mraka <michael.mraka@redhat.com> 2.2.1-1
- remove unneded imports

* Fri Dec 20 2013 Milan Zazrivec <mzazrivec@redhat.com> 2.1.4-1
- 967503 - use new Koan attribute

* Mon Oct 14 2013 Michael Mraka <michael.mraka@redhat.com> 2.1.3-1
- cleaning up old svn Ids

* Mon Sep 30 2013 Michael Mraka <michael.mraka@redhat.com> 2.1.2-1
- removed trailing whitespaces

* Thu Jul 25 2013 Stephen Herr <sherr@redhat.com> 2.1.1-1
- 988428 - Mark spacewalk-koan as correctly requiring the xz package
- Bumping package versions for 2.1.

