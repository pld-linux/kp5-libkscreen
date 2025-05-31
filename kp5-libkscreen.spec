#
# Conditional build:
%bcond_with	tests		# test suite

%define		qt_ver		5.15.2
%define		kf_ver		5.102.0
%define		kp_ver		5.27.12
%define		kpname		libkscreen

Summary:	KDE screen management software
Summary(pl.UTF-8):	Biblioteka do zarządzania ekranami KDE
Name:		kp5-%{kpname}
Version:	5.27.12
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kp_ver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	bab09cf389e09d0f33ff55ca0550442d
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5DBus-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Test-devel >= %{qt_ver}
BuildRequires:	Qt5WaylandClient-devel >= %{qt_ver}
BuildRequires:	Qt5X11Extras-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf5-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf5-kconfig-devel >= %{kf_ver}
BuildRequires:	kf5-kwayland-devel >= %{kf_ver}
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	plasma-wayland-protocols-devel >= 1.10.0
BuildRequires:	qt5-linguist >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
BuildRequires:	wayland-devel >= 1.15
BuildRequires:	xz
Requires:	Qt5Core >= %{qt_ver}
Requires:	Qt5DBus >= %{qt_ver}
Requires:	Qt5Gui >= %{qt_ver}
Requires:	Qt5WaylandClient >= %{qt_ver}
Requires:	Qt5X11Extras >= %{qt_ver}
Requires:	kf5-kconfig >= %{kf_ver}
Requires:	kf5-kwayland >= %{kf_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KDE screen management software.

%description -l pl.UTF-8
Biblioteka do zarządzania ekranami KDE.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qt_ver}
Requires:	Qt5DBus-devel >= %{qt_ver}
Requires:	Qt5Gui-devel >= %{qt_ver}
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang libkscreen5_qt --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f libkscreen5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/kscreen-doctor
%attr(755,root,root) %{_libexecdir}/kf5/kscreen_backend_launcher
%attr(755,root,root) %{_libdir}/libKF5Screen.so.*.*.*
%ghost %{_libdir}/libKF5Screen.so.8
%attr(755,root,root) %{_libdir}/libKF5ScreenDpms.so.*.*.*
%ghost %{_libdir}/libKF5ScreenDpms.so.8
%dir %{_libdir}/qt5/plugins/kf5/kscreen
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kscreen/KSC_Fake.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kscreen/KSC_QScreen.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kscreen/KSC_XRandR.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kscreen/KSC_XRandR11.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kscreen/KSC_KWayland.so
%{_datadir}/dbus-1/services/org.kde.kscreen.service
%{_datadir}/qlogging-categories5/libkscreen.categories
%{systemduserunitdir}/plasma-kscreen.service
%{zsh_compdir}/_kscreen-doctor

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF5Screen.so
%{_libdir}/libKF5ScreenDpms.so
%{_includedir}/KF5/KScreen
%{_includedir}/KF5/kscreen_version.h
%{_libdir}/cmake/KF5Screen
%{_libdir}/qt5/mkspecs/modules/qt_KScreen.pri
%{_pkgconfigdir}/kscreen2.pc
