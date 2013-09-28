%define		basever	3.10

Summary:	WebKit-based GNOME web browser
Name:		epiphany
Version:	%{basever}.0
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/gnome/sources/epiphany/%{basever}/%{name}-%{version}.tar.xz
# Source0-md5:	009d9ed8ee25885c5539c124f4630072
URL:		http://www.gnome.org/projects/epiphany/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	enchant-devel
BuildRequires:	gcr-devel >= 3.10.0
BuildRequires:	gnome-desktop-devel >= 3.10.0
BuildRequires:	gnome-doc-utils
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	gsettings-desktop-schemas-devel >= 3.10.0
BuildRequires:	gtk+3-webkit-devel >= 2.2.0
BuildRequires:	intltool
BuildRequires:	iso-codes
BuildRequires:	libtool
BuildRequires:	libwnck-devel
BuildRequires:	libxslt-devel
BuildRequires:	pkg-config
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires:	dbus
Requires:	gsettings-desktop-schemas >= 3.10.0
Requires:	iso-codes
Requires:	xdg-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME web browser based on WebKit.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e '/GNOME_COMPILE_WARNINGS.*/d'	\
    -i -e '/GNOME_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/GNOME_COMMON_INIT/d'		\
    -i -e '/GNOME_CODE_COVERAGE/d'		\
    -i -e '/GNOME_DEBUG_CHECK/d' configure.ac

%{__sed} -i '/@GNOME_CODE_COVERAGE_RULES@/d' Makefile.am

echo 'NoDisplay=true' >> data/bme.desktop.in.in

%build
%{__gnome_doc_prepare}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--with-distributor-name=Freddix
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw,tk,ps}

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_gsettings_cache

%postun
%update_desktop_database_postun
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{basever}
%dir %{_libdir}/%{name}/%{basever}/web-extensions

%attr(755,root,root) %{_bindir}/ephy-profile-migrator
%attr(755,root,root) %{_bindir}/epiphany
%attr(755,root,root) %{_libdir}/epiphany/3.*/web-extensions/libephywebextension.so

%{_datadir}/%{name}

%{_datadir}/dbus-1/services/org.gnome.Epiphany.service
%{_datadir}/glib-2.0/schemas/org.gnome.Epiphany.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.epiphany.gschema.xml
%{_datadir}/gnome-shell/search-providers/epiphany-search-provider.ini

%{_desktopdir}/epiphany.desktop
%{_mandir}/man1/epiphany.1*

