#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	5.27.5
%define		qtver		5.15.2
%define		kpname		libkscreen

Summary:	KDE screen management software
Name:		kp5-%{kpname}
Version:	5.27.5
Release:	2
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	74bde56139ac985dcbdc2367a70b9bca
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules
BuildRequires:	kf5-kwayland-devel
BuildRequires:	kf5-plasma-wayland-protocols-devel >= 1.10.0
BuildRequires:	ninja
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
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	../
%ninja_build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kscreen-doctor
%attr(755,root,root) %{_prefix}/libexec/kf5/kscreen_backend_launcher
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
%{_pkgconfigdir}/kscreen2.pc
%{_libdir}/qt5/mkspecs/modules/qt_KScreen.pri
