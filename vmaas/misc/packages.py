EXPECTED_BASH = [
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:1931",
        "package": "bash-4.2.46-28.el7.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2014:1306",
        "package": "bash-4.2.45-5.el7_0.4.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:1931",
        "package": "bash-4.2.46-28.el7.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2014:1306",
        "package": "bash-4.2.45-5.el7_0.4.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    }
]

EXPECTED_VIM = [
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2016:2972",
        "package": "vim-common-2:7.4.160-1.el7_3.1.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2016:2972",
        "package": "vim-common-2:7.4.160-1.el7_3.1.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    },
]

EXPECTED_HTTPD = [
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2016:1422",
        "package": "httpd-2.4.6-40.el7_2.4.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:0906",
        "package": "httpd-2.4.6-45.el7_3.4.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:2479",
        "package": "httpd-2.4.6-67.el7_4.2.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:2882",
        "package": "httpd-2.4.6-67.el7_4.5.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2016:1422",
        "package": "httpd-2.4.6-40.el7_2.4.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:0906",
        "package": "httpd-2.4.6-45.el7_3.4.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:2479",
        "package": "httpd-2.4.6-67.el7_4.2.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:2882",
        "package": "httpd-2.4.6-67.el7_4.5.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    }
]

EXPECTED_X86_64_TO_NOARCH = [
    {
        "basearch": "x86_64",
        "erratum": "vmaas_test_1",
        "package": "test-vmaas-0.3-3.noarch",
        "releasever": "7",
        "repository": "vmaas-test-1"
    }
]

EXPECTED_FROM_NOARCH = [
    {
        "basearch": "x86_64",
        "erratum": "vmaas_test_1",
        "package": "test-vmaas-0.3-3.noarch",
        "releasever": "7",
        "repository": "vmaas-test-1"
    }
]

EXPECTED_OTHER_REPO = [
    {
        "basearch": "x86_64",
        "erratum": "vmaas_test_2",
        "package": "test-vmaas-2-2.x86_64",
        "releasever": "7",
        "repository": "vmaas-test-2"
    }
]

PACKAGES_BASIC = [
    # package, expected updates
    ('bash-0:4.2.45-5.el7_0.2.x86_64', EXPECTED_BASH),
    ('httpd-2.4.6-31.el7_1.1.x86_64', EXPECTED_HTTPD),
    ('vim-common-2:7.4.160-1.el7.x86_64', EXPECTED_VIM),
    ('vim-enhanced-2:7.4.160-2.el7.x86_64', None),
    ('telepathy-logger-0.8.0-5.el7.x86_64', None)
]

PACKAGES_TO_NOARCH = [
    # package, expected updates
    # update to noarch package expected
    ('test-vmaas-0.1-1.x86_64', EXPECTED_X86_64_TO_NOARCH + EXPECTED_OTHER_REPO),
    ('test-vmaas-0.2-2.x86_64', EXPECTED_X86_64_TO_NOARCH + EXPECTED_OTHER_REPO),
    ('test-vmaas-0.3-3.x86_64', EXPECTED_OTHER_REPO)
]

PACKAGES_FROM_NOARCH = [
    # package, expected updates
    # update from noarch to arch package expected
    ('test-vmaas-0.1-1.noarch', EXPECTED_FROM_NOARCH + EXPECTED_OTHER_REPO),
    ('test-vmaas-0.3-3.noarch', EXPECTED_OTHER_REPO)
]

PACKAGES_OTHER_REPO = [
    # package, expected updates
    # update to package from different repository within same product
    ('test-vmaas-0.1-1.x86_64', EXPECTED_X86_64_TO_NOARCH + EXPECTED_OTHER_REPO),
    ('test-vmaas-0.2-2.x86_64', EXPECTED_X86_64_TO_NOARCH + EXPECTED_OTHER_REPO),
    ('test-vmaas-0.3-3.x86_64', EXPECTED_OTHER_REPO),
    ('test-vmaas-1-1.x86_64', EXPECTED_OTHER_REPO),
    ('test-vmaas-2-2.x86_64', None),
    ('test-vmaas-3-3.x86_64', None)
]