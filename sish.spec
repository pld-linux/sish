#
# Conditional build:
%bcond_with	prebuilt		# use prebuilt binary

%define		revision	58fc3ee5f
Summary:	An open source serveo/ngrok alternative
Name:		sish
Version:	0.0.1
Release:	1
License:	MIT
Group:		Development/Building
Source0:	https://github.com/antoniomika/sish/archive/%{revision}/%{revision}.tar.gz
# Source0-md5:	878d1a9bee0864181965448869f1c184
URL:		https://github.com/antoniomika/sish
BuildRequires:	golang >= 1.11
BuildRequires:	rpmbuild(macros) >= 1.647
ExclusiveArch:	%{ix86} %{x8664} %{arm}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# go stuff
%define _enable_debug_packages 0
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v %{?debug:-x} %{?**};
%define import_path	github.com/antoniomika/sish

%description
An open source serveo/ngrok alternative. HTTP(S)/WS(S)/TCP Tunnels to
localhost using only SSH.

%prep
%setup -qc

# for doc
mv %{name}-*/*.md .

# don't you love go?
install -d src/$(dirname %{import_path})
mv %{name}-* src/%{import_path}

%build
export GOPATH=$(pwd)
cd src/%{import_path}

go get ./...
%gobuild ./...

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p bin/%{name} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/sish
