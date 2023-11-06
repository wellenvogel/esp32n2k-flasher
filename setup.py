#!/usr/bin/env python
"""esphomeflasher setup script."""
import os
VERSION="2.1"

from setuptools import setup, find_packages


PROJECT_NAME = 'esp32n2kflasher'
PROJECT_PACKAGE_NAME = 'esp32n2kflasher'
PROJECT_LICENSE = 'MIT'
PROJECT_AUTHOR = 'wellenvogel'
PROJECT_COPYRIGHT = '2021, wellenvogel'
PROJECT_URL = 'https://github.com/wellenvogel/esp32n2k-flasher'
PROJECT_EMAIL = 'andreas@wellenvogel.net'

PROJECT_GITHUB_USERNAME = 'wellenvogel'
PROJECT_GITHUB_REPOSITORY = 'esp32n2k-flasher'

PYPI_URL = 'https://pypi.python.org/pypi/{}'.format(PROJECT_PACKAGE_NAME)
GITHUB_PATH = '{}/{}'.format(PROJECT_GITHUB_USERNAME, PROJECT_GITHUB_REPOSITORY)
GITHUB_URL = 'https://github.com/{}'.format(GITHUB_PATH)

DOWNLOAD_URL = '{}/archive/{}.zip'.format(GITHUB_URL, VERSION)

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as requirements_txt:
    REQUIRES = requirements_txt.read().splitlines()

with open(os.path.join(here, 'README.md')) as readme:
    LONG_DESCRIPTION = readme.read()


setup(
    name=PROJECT_PACKAGE_NAME,
    version=VERSION,
    license=PROJECT_LICENSE,
    url=GITHUB_URL,
    download_url=DOWNLOAD_URL,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    description="ESP32 firmware flasher for ESP32NMEA2000",
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    test_suite='tests',
    python_requires='>=3.6.9,<4.0',
    install_requires=REQUIRES,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords=['boat', 'nmea2000'],
    entry_points={
        'console_scripts': [
            'esp32n2kflashtool = flashtool.__main__:main'
        ]
    },
    packages=find_packages(include="esp32n2k-flasher.*")
)
