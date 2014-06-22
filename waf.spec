Summary:	A framework for configuring, compiling and installing applications
Name:		waf
Version:	1.7.16
Release:	3
License:	BSD
Group:		Development/Other
Url:		http://code.google.com/p/waf/
Source0:	http://waf.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:	%{name}.macros
Patch2:		waf-1.6.2-libdir.patch
BuildRequires:  pkgconfig(python)
Requires:       python
BuildArch:	noarch

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
# use waf so it unpacks itself
mkdir _temp ; pushd _temp
cp -av ../waf .
%{__python} ./waf
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

%files
%doc README TODO ChangeLog demos utils
%{_sysconfdir}/rpm/macros.d/%{name}.macros
%{_bindir}/%{name}
%{_datadir}/%{name}
