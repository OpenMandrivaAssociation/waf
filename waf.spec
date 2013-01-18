%define debug_package %{nil}

%define rel		2
%if %mdkversion < 201100
%define release	%mkrel %{rel}
%else
%define	release %{rel}
%endif

Summary:	A framework for configuring, compiling and installing applications
Name:		waf
Version:	1.6.11
Release:	%{release}
License:	BSD
Group:		Development/Other
Url:		http://code.google.com/p/waf/
Source0:	http://waf.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:	%{name}.macros
Patch2:		waf-1.6.2-libdir.patch
%py_requires -d
Requires:   python
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Waf is a Python-based framework for configuring, compiling and installing
applications. It derives from the concepts of other build tools such as 
Scons, Autotools, CMake, and Ant.

* Easy to use: Waf configuration files are written in the mainstream 
  scripting language Python.
* Easy to install and to distribute: Waf fits entirely in a single 
  75KB redistributable file which does not require any installation to run.
* Portable: Waf only depends on Python which is ported onto most 
  operating systems.
* Reliable: Waf uses hash-based dependency calculation dependencies to 
  compute the targets to rebuild.
* User-friendly: The output can be displayed in colors, filtered, 
  displayed with progress bars or output all the commands that get 
  executed.
* Documented: The Waf book sums up the essential concepts.
* Flexible: Because Waf has a carefully designed object oriented 
  architecture it is very easy to add new features.
* Fast: Because of its carefully designed architecture, Waf is able 
  to distribute the jobs on multi-core hardware (-j), it is able to 
  reuse targets compiled already (ccache), and its runtime footprint 
  is pretty small compared to other build tools.
* Broad support for languages and tools: Waf is already used for C, 
  C++, C#, D, java, ocaml, python project, and provides various 
  tools for processing docbook, man pages, intltool, msgfmt. 

%prep
%setup -q
%patch2 -p0

%build

./waf-light configure --prefix=%{_prefix}

extras=
for f in waflib/extras/*.py ; do
   f=$(basename "$f" .py);
   if [ "$f" != "__init__" ]; then
     extras="${extras:+$extras,}$f" ;
   fi
done

./waf-light --make-waf --strip --tools="$extras" --prefix=%{_prefix}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# use waf so it unpacks itself
mkdir _temp ; pushd _temp
cp -av ../waf .
%{__python} ./waf >/dev/null 2>&1
    pushd .waf-%{version}-*
	find . -name '*.py' -printf '%%P\0' | xargs -0 -I{} install -m 0644 -p -D {} %{buildroot}%{_datadir}/waf/{}
    popd
popd

install -m 0755 -p -D waf-light %{buildroot}%{_bindir}/waf

# remove shebangs from and fix EOL for all scripts in wafadmin
find %{buildroot}%{_datadir}/ -name '*.py' \
      -exec sed -i -e '1{/^#!/d}' -e 's|\r$||g' {} \;

# fix waf script shebang line
sed -i "1c#! /usr/bin/python" %{buildroot}%{_bindir}/waf

# remove x-bits from everything going to doc
find demos utils -type f -exec %{__chmod} 0644 {} \;

# remove hidden file
rm -f docs/sphinx/build/html/.buildinfo

# remove x-bits from everything going to doc
find demos utils -type f -exec %{__chmod} 0644 {} \;

# install waf rpm macro helper
install -D %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.d/%{name}.macros

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README TODO ChangeLog demos utils
%{_sysconfdir}/rpm/macros.d/%{name}.macros
%{_bindir}/%{name}
%{_datadir}/%{name}


%changelog
* Mon Jun 18 2012 Lev Givon <lev@mandriva.org> 1.6.11-1
+ Revision: 806134
- Update to 1.6.11.

* Fri Oct 07 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.6.8-1
+ Revision: 703436
- update to new version 1.6.8
- remove patches 0 and 1
- add patch 2
- rewrite spec file

* Fri Oct 29 2010 Michael Scherer <misc@mandriva.org> 1.5.19-2mdv2011.0
+ Revision: 590142
- rebuild for python 2.7

* Sun Oct 17 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.19-1mdv2011.0
+ Revision: 586308
- update to new version 1.5.19

* Sun Aug 22 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.18-1mdv2011.0
+ Revision: 571976
- update to new version 1.5.18
- rediff patch 1

* Mon Apr 05 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.15-1mdv2010.1
+ Revision: 531573
- update to new version 1.5.15
- rediff patch 0

* Sun Mar 07 2010 Lev Givon <lev@mandriva.org> 1.5.14-1mdv2010.1
+ Revision: 515481
- Update to 1.5.14.

* Thu Feb 18 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.12-1mdv2010.1
+ Revision: 507863
- update to new version 1.5.12

* Mon Feb 01 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.11-1mdv2010.1
+ Revision: 499241
-- update to new version 1.5.11
- rediff patch 0

* Wed Nov 18 2009 Frederik Himpe <fhimpe@mandriva.org> 1.5.10-1mdv2010.1
+ Revision: 467287
- update to new version 1.5.10

* Wed Sep 02 2009 Frederik Himpe <fhimpe@mandriva.org> 1.5.9-1mdv2010.0
+ Revision: 425473
- update to new version 1.5.9

* Sat Jul 11 2009 Funda Wang <fwang@mandriva.org> 1.5.8-2mdv2010.0
+ Revision: 394731
- fix pthread linkage

* Sun Jun 14 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.8-1mdv2010.0
+ Revision: 385925
- update to new version 1.5.8

* Sat May 30 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.6-1mdv2010.0
+ Revision: 381343
- update to new version 1.5.6

* Fri May 01 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.5-1mdv2010.0
+ Revision: 369238
- update to new version 1.5.5
- rediff patch 0

* Mon Feb 02 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.3-1mdv2009.1
+ Revision: 336307
- update to new version 1.5.3

* Fri Jan 30 2009 Funda Wang <fwang@mandriva.org> 1.5.2-4mdv2009.1
+ Revision: 335640
- specify LINKFLAGS also.

* Sat Jan 03 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.2-3mdv2009.1
+ Revision: 323950
- fix install macro

* Sat Jan 03 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.2-2mdv2009.1
+ Revision: 323544
- fix typo in waf.macros

* Sat Jan 03 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.2-1mdv2009.1
+ Revision: 323515
- add specs and source files
- provide waf.macros for rpm building
- Patch0: fix installation of waf
- Created package structure for waf.

