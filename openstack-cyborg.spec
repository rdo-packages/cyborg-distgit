%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global service cyborg
%global common_desc OpenStack Accelerator Life Cycle Management.

Name:       openstack-%{service}
Version:    master
Release:    1%{?dist}
Summary:    OpenStack Accelerator Life Cycle Management
License:    ASL 2.0
URL:        https://docs.openstack.org/%{service}/

Source0:    https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git-core
BuildRequires:  openstack-macros

# Required for tests
BuildRequires: python3-oslotest
BuildRequires: python3-stestr
BuildRequires: python3-testtools
BuildRequires: python3-ddt
BuildRequires: python3-fixtures
BuildRequires: python3-testrepository
BuildRequires: python3-testresources
BuildRequires: python3-testscenarios

# Required for service
BuildRequires: python3-oslo-i18n
BuildRequires: python3-oslo-log
BuildRequires: python3-oslo-utils
BuildRequires: python3-oslo-config
BuildRequires: python3-oslo-context
BuildRequires: python3-oslo-db
BuildRequires: python3-oslo-policy
BuildRequires: python3-oslo-versionedobjects
BuildRequires: python3-oslo-messaging
BuildRequires: python3-oslo-upgradecheck
BuildRequires: python3-os-resource-classes
BuildRequires: python3-stevedore
BuildRequires: python3-glanceclient
BuildRequires: python3-wsme
BuildRequires: python3-eventlet
BuildRequires: python3-jsonpatch
BuildRequires: python3-keystonemiddleware
BuildRequires: python3-keystoneauth1
BuildRequires: python3-oslo-privsep
BuildRequires: python3-pecan
BuildRequires: python3-psutil
BuildRequires: python3-pbr
BuildRequires: python3-sqlalchemy
BuildRequires: python3-alembic
BuildRequires: python3-cursive
BuildRequires: python3-microversion-parse
BuildRequires: python3-openstacksdk

Requires:   python3-%{service} = %{version}-%{release}

Requires(pre): shadow-utils
%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif

%description
%{common_desc}


%package -n python3-%{service}
Summary:    Cyborg
%{?python_provide:%python_provide python3-%{service}}
Group:      Applications/System

Requires: python3-oslo-i18n >= 1.5.0
Requires: python3-oslo-log >= 5.0.0
Requires: python3-oslo-utils >= 4.5.0
Requires: python3-oslo-config >= 1.1.0
Requires: python3-oslo-context >= 2.9.0
Requires: python3-oslo-db >= 10.0.0
Requires: python3-oslo-policy >= 3.7.0
Requires: python3-oslo-versionedobjects >= 1.31.2
Requires: python3-oslo-messaging >= 10.3.0
Requires: python3-oslo-upgradecheck >= 1.3.0
Requires: python3-os-resource-classes >= 1.1.0
Requires: python3-stevedore >= 1.20.0
Requires: python3-glanceclient >= 1:2.8.0
Requires: python3-wsme >= 0.10.1
Requires: python3-eventlet >= 0.26.0
Requires: python3-jsonpatch >= 1.16
Requires: python3-keystonemiddleware >= 4.17.0
Requires: python3-keystoneauth1
Requires: python3-oslo-privsep >= 2.6.2
Requires: python3-pecan >= 1.0.0
Requires: python3-psutil >= 3.2.2
Requires: python3-pbr >= 0.11
Requires: python3-sqlalchemy >= 1.4.13
Requires: python3-alembic >= 1.5.0
Requires: python3-cursive >= 0.2.1
Requires: python3-microversion-parse >= 0.2.1
Requires: python3-openstacksdk >= 0.35.0
Requires: pciutils

%description -n python3-%{service}
%{common_desc}

%package -n python3-%{service}-tests
Summary:    Cyborg tests
%{?python_provide:%python_provide python3-%{service}-tests}
Group:      Applications/System

Requires:   python3-%{service} = %{version}-%{release}

Requires:   python3-mock
Requires:   python3-subunit
Requires:   python3-oslotest
Requires:   python3-testrepository
Requires:   python3-testtools
Requires:   python3-testresources
Requires:   python3-testscenarios
Requires:   python3-tempest

Requires:   python3-requests-mock

%description -n python3-%{service}-tests
%{common_desc}

This package contains cyborg test files.

%package -n openstack-cyborg-common
Summary:    Cyborg common files
Group:      Applications/System

Requires:   python3-%{service} = %{version}-%{release}

%description -n openstack-cyborg-common
%{common_desc}

%prep
rm -rf '%{service}-%{upstream_version}'
mkdir '%{service}-%{upstream_version}' && cd '%{service}-%{upstream_version}'
/usr/bin/gzip -dc %(ls /builddir/build/SOURCES/*cyborg*) | /usr/bin/tar --strip-components 1 -xof -
STATUS=$?
if [ $STATUS -ne 0 ]; then
  exit $STATUS
fi
# Let's handle dependencies ourseleves
rm -f requirements.txt
rm -rf *cyborg.egg-info

%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
cd '%{service}-%{upstream_version}'
%{py3_build}

%install
cd '%{service}-%{upstream_version}'
%{py3_install}
# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/nova
install -p -D -m 640 etc/%{service}/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini
install -p -D -m 640 etc/%{service}/policy.yaml %{buildroot}%{_sysconfdir}/%{service}/policy.yaml
rm -rf %{buildroot}/usr/etc/%{service}

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
getent passwd %{service} >/dev/null || \
    useradd -r -g %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin \
    -c "OpenStack Cyborg Daemons" %{service}
exit 0

%check

%files common
%license %{service}-%{upstream_version}/LICENSE
%{python3_sitelib}/%{service}
%{python3_sitelib}/openstack_%{service}*.egg-info
%exclude %{python3_sitelib}/%{service}/tests
%{_bindir}/cyborg-*
%dir %{_sysconfdir}/cyborg
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/policy.yaml

%files -n python3-%{service}
%license %{service}-%{upstream_version}/LICENSE
%{python3_sitelib}/%{service}
%{python3_sitelib}/openstack_%{service}*.egg-info
%exclude %{python3_sitelib}/%{service}/tests

%files -n python3-%{service}-tests
%license %{service}-%{upstream_version}/LICENSE
%{python3_sitelib}/%{service}/tests

%changelog
