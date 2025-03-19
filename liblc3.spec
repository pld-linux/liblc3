#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	python3		# CPython 3.x module
#
Summary:	Low Complexity Communication Codec (LC3)
Summary(pl.UTF-8):	Kodek LC3 (Low Complexity Communication Codec)
Name:		liblc3
Version:	1.1.3
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/google/liblc3/releases
Source0:	https://github.com/google/liblc3/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c9252af36fbece63de402488675a9274
URL:		https://github.com/google/liblc3
BuildRequires:	meson >= 0.48.0
BuildRequires:	ninja >= 1.5
%{?with_python3:BuildRequires:	python3-modules >= 1:3.10}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
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

%package -n python3-liblc3
Summary:	Python wrapper for LC3 Codec library
Summary(pl.UTF-8):	Pythonowy interfejs do biblioteki kodeka LC3
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-modules >= 1:3.10
BuildArch:	noarch

%description -n python3-liblc3
Python wrapper for LC3 Codec library.

%description -n python3-liblc3 -l pl.UTF-8
Pythonowy interfejs do biblioteki kodeka LC3.

%prep
%setup -q

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	%{?with_python3:-Dpython=true} \
	-Dtools=true

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

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

%if %{with python3}
%files -n python3-liblc3
%defattr(644,root,root,755)
%{py3_sitescriptdir}/lc3.py
%{py3_sitescriptdir}/__pycache__/lc3.cpython-*.py[co]
%endif
