%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1
%global library cyborg
%global module cyborg
%global common_desc OpenStack Accelerator Life Cycle Management.
%global pyver 3
Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Accelerator Life Cycle Management
License:    ASL 2.0
URL:        https://docs.openstack.org/cyborg/
Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz
BuildArch:  noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git-core
BuildRequires:  openstack-macros
Requires: pciutils
%description
%{common_desc}
%package -n  python3-%{library}
Summary: OpenStack Accelerator Life Cycle Management
%{?python_provide:%python_provide python3-%{library}}
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

%description -n python3-%{library}
%{common_desc}
%package -n python3-%{library}-tests
Summary:    OpenStack Cyborg tests
%{?python_provide:%python_provide python3-%{library}-tests}
Requires:   python3-%{library} = %{version}-%{release}
%description -n python3-%{library}-tests
%{common_desc}
This package contains the Octavia library test files.
%if 0%{?with_doc}
%package doc
Summary:    OpenStack Octavia library documentation
BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme
%description doc
%{common_desc}
This package contains the documentation.
%endif
%prep
%autosetup -n %{library}-%{upstream_version} -S git
# Let's handle dependencies ourseleves
%py_req_cleanup
%build
%{pyver_build}
%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif
%install
%{pyver_install}
# Remove setuptools installed data_files
rm -rf %{buildroot}%{_datadir}/%{library}/LICENSE
rm -rf %{buildroot}%{_datadir}/%{library}/README.rst
%check
export OS_TEST_PATH='./cyborg/tests/unit'
export PATH=$PATH:%{buildroot}/usr/bin
export PYTHONPATH=$PWD
stestr-3 --test-path $OS_TEST_PATH run
%files -n python3-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests
%files -n python3-%{library}-tests
%license LICENSE
%{pyver_sitelib}/%{module}/tests
%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif
%changelog
* Thu Oct 20 2022 Sean Mooney <smooney@redhat.com> master-2
  inital commit



