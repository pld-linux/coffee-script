%define		pkg	coffee-script
Summary:	The CoffeeScript Compiler
Name:		coffee-script
Version:	1.6.3
Release:	1
License:	MIT
Group:		Development/Libraries
URL:		http://coffeescript.org/
Source0:	https://github.com/jashkenas/coffee-script/archive/%{version}.tar.gz
# Source0-md5:	837fb08b97deb00c471101b9c3a5a107
Patch0:		coffee-script-Cakefile.patch
Patch1:		coffee-script-fix-importing-test.patch
BuildRequires:	rpmbuild(macros) >= 1.634
BuildRequires:	sed >= 4.0
Requires:	nodejs >= 0.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CoffeeScript is a little language that compiles into JavaScript.
Underneath all of those embarrassing braces and semicolons, JavaScript
has always had a gorgeous object model at its heart. CoffeeScript is
an attempt to expose the good parts of JavaScript in a simple way.

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' bin/*
chmod a+rx bin/*

./bin/cake build

#also build the unminifed version
MINIFY=false ./bin/cake build:browser

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
cp -a bin lib package.json $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}

install -d $RPM_BUILD_ROOT%{_bindir}
ln -s %{nodejs_libdir}/%{pkg}/bin/cake $RPM_BUILD_ROOT%{_bindir}/cake.coffeescript
ln -s %{nodejs_libdir}/%{pkg}/bin/coffee $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LICENSE CONTRIBUTING.md
%attr(755,root,root) %{_bindir}/cake.coffeescript
%attr(755,root,root) %{_bindir}/coffee
%dir %{nodejs_libdir}/%{pkg}
%{nodejs_libdir}/%{pkg}/lib
%{nodejs_libdir}/%{pkg}/package.json
%dir %{nodejs_libdir}/%{pkg}/bin
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/bin/*
