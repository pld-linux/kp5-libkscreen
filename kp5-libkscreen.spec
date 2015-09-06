%define		kdeplasmaver	5.4.0
%define		qtver		5.3.2
%define		kpname		libkscreen

Summary:	KDE screen management software
Name:		kp5-%{kpname}
Version:	5.4.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	4e40165c6bef910a728bd17dbdc312df
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KDE screen management software.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
install -d build
cd build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kf5/kscreen_backend_launcher
%attr(755,root,root) %{_libdir}/libKF5Screen.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5Screen.so.6
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kscreen/KSC_Fake.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kscreen/KSC_QScreen.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kscreen/KSC_XRandR.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kscreen/KSC_XRandR11.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF5Screen.so
%{_includedir}/KF5/KScreen
%{_includedir}/KF5/kscreen_version.h
%{_libdir}/cmake/KF5Screen
%{_pkgconfigdir}/kscreen2.pc
%{_libdir}/qt5/mkspecs/modules/qt_KScreen.pri
