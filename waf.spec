%define debug_package %{nil}
%define _requires_exceptions perl(Exporter)|\\perl(XSLoader)|\\

Summary:	A framework for configuring, compiling and installing applications
Name:		waf
Version:	1.5.6
Release:	%mkrel 1
License:	BSD
Group:		Development/Other
Url:		http://code.google.com/p/waf/
Source0:	http://waf.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:	%{name}.macros
Patch0:		%{name}-1.5.5-installdir.patch
%py_requires -d
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Waf is a Python-based framework for configuring, compiling and installing
applications.It derives from the concepts of other build tools such as 
Scons, Autotools, CMake or Ant.

* Easy to use: Waf configuration files are written in the mainstream 
  scripting language Python
* Easy to install and to distribute: Waf fits entirely in a single 
  75KB redistributable file which does not require any installation to run
* Portable: Waf only depends on Python which is ported onto most 
  operating systems
* Reliable: Waf uses hash-based dependency calculation dependencies to 
  compute the targets to rebuild
* User-friendly: The output can be displayed in colors, filtered, 
  displayed with progress bars or output all the commands that get 
  executed
* Documented: The Waf book sums up the essential concepts
* Flexible: Because Waf has a carefully designed object oriented 
  architecture it is very easy to add new features
* Fast: Because of its carefully designed architecture, Waf is able 
  to distribute the jobs on multi-core hardware (-j), it is able to 
  reuse targets compiled already (ccache), and its runtime footprint 
  is pretty small compared to other build tools
* Broad support for languages and tools: Waf is already used for C, 
  C++, C#, D, java, ocaml, python project, and provides various 
  tools for processing docbook, man pages, intltool, msgfmt 

%prep
%setup -q
%patch0 -p1

%build
./waf-light configure --prefix=%{_prefix}

./waf-light --make-waf

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# say yes, please
echo y | ./waf-light install --destdir=%{buildroot}

# remove shebangs from all scripts in wafadmin
find %{buildroot}%{_datadir}/waf/wafadmin -name '*.py' \
     -exec %{__sed} -i '1{/^#!/d}' {} \;

# fix waf script shebang line
%{__sed} -i "1c#! /usr/bin/python" %{buildroot}%{_bindir}/waf

# fix EOL
%{__sed} -i 's|\r$||g' utils/amtool.py

# remove x-bits from everything going to doc
find demos utils -type f -exec %{__chmod} 0644 {} \;

# remove zero-length files
%{__rm} demos/gnome/src/hello.h
%{__rm} demos/simple_scenarios/local_tool/uh.coin

# bash completion
%{__install} -D -p -m 0644 utils/waf-completion.bash \
  %{buildroot}%{_sysconfdir}/bash_completion.d//waf-completion.bash

# install waf rpm macro helper
install -D %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.d/%{name}.macros

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README TODO ChangeLog demos doc/book utils
%{_sysconfdir}/bash_completion.d/%{name}*
%{_sysconfdir}/rpm/macros.d/%{name}.macros
%{_bindir}/%{name}
%{_datadir}/%{name}
