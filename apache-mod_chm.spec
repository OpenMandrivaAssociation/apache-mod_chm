#Module-Specific definitions
%define mod_name mod_chm
%define mod_conf A33_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0.3.1
Release:	15
Group:		System/Servers
License:	GPL
URL:		http://sourceforge.net/projects/modchm/
Source0: 	http://prdownloads.sourceforge.net/modchm/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRequires:	perl
BuildRequires:	chmlib-devel
Epoch:		1

%description
mod_chm is an apache module that gives you possibility to explore
files in CHM format. mod_chm uses chmlib by Jed Wing to access CHM
files. This package also includes chmdump program that unpacks
content of CHM file.

%prep

%setup -q -n mod_chm

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_bindir}/apxs -c %{mod_name}.c -I. -lchm

gcc %{optflags} chmdump/chmdump.c -o chmdump/chmdump -lchm

%install

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -m0755 chmdump/chmdump %{buildroot}%{_bindir}/

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc AUTHORS COPYING ChangeLog README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_bindir}/chmdump
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-15mdv2012.0
+ Revision: 772606
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-14
+ Revision: 678292
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-13mdv2011.0
+ Revision: 587950
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-12mdv2010.1
+ Revision: 516078
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-11mdv2010.0
+ Revision: 406562
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-10mdv2009.1
+ Revision: 325676
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-9mdv2009.0
+ Revision: 234853
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-8mdv2009.0
+ Revision: 215557
- fix rebuild

* Sat Mar 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-7mdv2008.1
+ Revision: 182249
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:0.3.1-6mdv2008.1
+ Revision: 170713
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-5mdv2008.0
+ Revision: 82545
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-4mdv2007.1
+ Revision: 140657
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-3mdv2007.0
+ Revision: 79381
- Import apache-mod_chm

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-3mdv2007.0
- rebuild

* Wed Dec 14 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-2mdk
- rebuilt against apache-2.2.0

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.3.1-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.3.1-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.3.1-2mdk
- use the %1

* Wed Mar 02 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.3.1-1mdk
- initial Mandrakelinux package

