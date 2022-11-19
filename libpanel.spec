#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	IDE paneling library for GTK
Summary(pl.UTF-8):	Biblioteka do paneli IDE dla GTK
Name:		libpanel
Version:	1.0.2
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libpanel/1.0/%{name}-%{version}.tar.xz
# Source0-md5:	6e50b6fb007671ebc68da8b9b81e0054
URL:		https://gitlab.gnome.org/GNOME/libpanel
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.72
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk4-devel >= 4.6
BuildRequires:	libadwaita-devel >= 1.0
BuildRequires:	meson >= 0.60
BuildRequires:	ninja >= 1.5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.44
BuildRequires:	vala-libadwaita >= 1.0
BuildRequires:	xz
Requires:	glib2 >= 1:2.72
Requires:	gtk4 >= 4.6
Requires:	libadwaita >= 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libpanel helps you create IDE-like applications using GTK 4 and
libadwaita.

It has widgets for panels, docks, columns and grids of pages.
Primarily, it's design and implementation focus around GNOME Builder
and Drafting projects.

%description -l pl.UTF-8
Libpanel pomaga tworzyć aplikacje typu IDE przy użyciu bibliotek GTK 4
oraz libadwaita.

Zawiera widżety do paneli, doków, kolumn i siatek stron. Projekt i
implementacja skupia się wokół projektów GNOME Builder i Drafting.

%package devel
Summary:	Header files for libpanel library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libpanel
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.72
Requires:	gtk4-devel >= 4.6

%description devel
Header files for libpanel library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libpanel.

%package -n vala-libpanel
Summary:	Vala API for libpanel library
Summary(pl.UTF-):	API języka Vala do biblioteki libpanel
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.44
Requires:	vala-libadwaita >= 1.0
BuildArch:	noarch

%description -n vala-libpanel
Vala API for libpanel library.

%description -n vala-libpanel -l pl.UTF-8
API języka Vala do biblioteki libpanel.

%package apidocs
Summary:	API documentation for libpanel library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libpanel
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libpanel library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libpanel.

%prep
%setup -q

%build
%meson build \
	%{!?with_apidocs:-Ddocs=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
# FIXME: where to package gi-docgen generated docs?
install -d $RPM_BUILD_ROOT%{_gtkdocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/panel-1.0 $RPM_BUILD_ROOT%{_gtkdocdir}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md TODO.md
%attr(755,root,root) %{_libdir}/libpanel-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpanel-1.so.1
%{_libdir}/girepository-1.0/Panel-1.typelib
%{_iconsdir}/hicolor/scalable/actions/panel-*-symbolic.svg

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpanel-1.so
%{_includedir}/libpanel-1
%{_datadir}/gir-1.0/Panel-1.gir
%{_pkgconfigdir}/libpanel-1.pc

%files -n vala-libpanel
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libpanel-1.deps
%{_datadir}/vala/vapi/libpanel-1.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/panel-1.0
%endif
