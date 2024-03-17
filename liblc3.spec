#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Low Complexity Communication Codec (LC3)
Summary(pl.UTF-8):	Kodek LC3 (Low Complexity Communication Codec)
Name:		liblc3
Version:	1.0.4
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/google/liblc3/releases
Source0:	https://github.com/google/liblc3/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	41ba0aba4d86713e5c7a102330bc2307
URL:		https://github.com/google/liblc3
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The LC3 is an efficient low latency audio codec.

%description -l pl.UTF-8
LC3 to wydajny kodek dźwięku o małych opóźnieniach.

%package devel
Summary:	Header files for LC3 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LC3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for LC3 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LC3.

%package static
Summary:	Static LC3 library
Summary(pl.UTF-8):	Statyczna biblioteka LC3
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LC3 library.

%description static -l pl.UTF-8
Statyczna biblioteka LC3.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	-Dtools=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/dlc3
%attr(755,root,root) %{_bindir}/elc3
%attr(755,root,root) %{_libdir}/liblc3.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblc3.so
%{_includedir}/lc3.h
%{_includedir}/lc3_cpp.h
%{_includedir}/lc3_private.h
%{_pkgconfigdir}/lc3.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liblc3.a
%endif
