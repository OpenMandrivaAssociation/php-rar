%define modname rar
%define soname %{modname}.so
%define inifile A75_%{modname}.ini

Summary:	RAR extension for PHP
Name:		php-%{modname}
Version:	3.0.2
Release:	2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/rar/
Source0:	http://pecl.php.net/get/rar-%{version}.tgz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file

%description
PHP extension for reading Rar archives using bundled unRAR library.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%serverbuild
export CXXFLAGS="$CXXFLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make

%install

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}/var/log/httpd

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean

%files 
%doc package*.xml tests CREDITS example.php
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Mon Jul 30 2012 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-1mdv2012.0
+ Revision: 811431
- 3.0.1

* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 3.0.0-5
+ Revision: 795491
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 3.0.0-4
+ Revision: 761283
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.0-3
+ Revision: 696460
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.0-2
+ Revision: 695456
- rebuilt for php-5.3.7

* Sun Jun 12 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.0-1
+ Revision: 684320
- 3.0.0

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-6
+ Revision: 646677
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-5mdv2011.0
+ Revision: 629857
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-4mdv2011.0
+ Revision: 628177
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-3mdv2011.0
+ Revision: 600523
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-2mdv2011.0
+ Revision: 588861
- rebuild

* Thu Apr 22 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-1mdv2010.1
+ Revision: 537986
- 2.0.0

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-0.0.RC1.1mdv2010.1
+ Revision: 514780
- drop one obsolete patch
- fix versioning
- 2.0.0RC1

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.0b2-2mdv2010.1
+ Revision: 485442
- rebuilt for php-5.3.2RC1

* Sat Dec 19 2009 Oden Eriksson <oeriksson@mandriva.com> 2.0.0b2-1mdv2010.1
+ Revision: 480163
- fix build
- 2.0.0b2

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-11mdv2010.1
+ Revision: 468245
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-10mdv2010.0
+ Revision: 451351
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.0.0-9mdv2010.0
+ Revision: 397587
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-8mdv2010.0
+ Revision: 377021
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-7mdv2009.1
+ Revision: 346600
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-6mdv2009.1
+ Revision: 341791
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-5mdv2009.1
+ Revision: 323045
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4mdv2009.1
+ Revision: 310300
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3mdv2009.0
+ Revision: 238424
- rebuild

* Wed Feb 27 2008 Thierry Vignaud <tv@mandriva.org> 1.0.0-2mdv2008.1
+ Revision: 175775
- make summary clearer

* Wed Feb 27 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2008.1
+ Revision: 175712
- import php-rar


