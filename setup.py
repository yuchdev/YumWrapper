# -*- coding: utf-8 -*-
import os
import sys
from setuptools import find_packages, setup

# Package-wide name
PACKAGE_NAME = "yum_wrapper"

# Append package dir to sys.path
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.abspath(os.path.join(PROJECT_DIR, "src", PACKAGE_NAME)))

# noinspection PyUnresolvedReferences,PyPackageRequirements
from version import VERSION

HERE = os.path.abspath(os.path.dirname(__file__))
MARKDOWN_PATH = os.path.join(HERE, 'README.md')
LONG_DESCRIPTION = ""
if os.path.exists(MARKDOWN_PATH):
    with open(MARKDOWN_PATH, encoding='utf-8') as f:
        LONG_DESCRIPTION = f.read()

# Add possible dependencies here
DEPENDENCIES = []

# Github download link
GITHUB_URL = "https://github.com/yuchdev/YumWrapper"

# Github download link
GITHUB_DOWNLOAD = "{github_url}/releases/download/release.{version}/yum_wrapper-{version}.tar.gz".format(
    github_url=GITHUB_URL,
    version=VERSION
)

# AWS download link
AWS_DOWNLOAD = "https://yum-wrapper.s3.us-east-1.amazonaws.com/packages/yum_wrapper-{}-py3-none-any.whl".format(
    VERSION
)

# PyPI project page
PYPI_URL = "https://pypi.org/project/yum-wrapper/"

# Issue tracker
ISSUE_TRACKER = "{github_url}/issues".format(github_url=GITHUB_URL)

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Yurii Cherkasov",
    author_email="strategarius@protonmail.com",
    description="Python wrapper for Yum package manager",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    download_url=GITHUB_DOWNLOAD,
    project_urls={
        "Bug Tracker": ISSUE_TRACKER,
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(os.path.join(HERE, 'src')),
    package_dir={"": "src"},
    package_data={PACKAGE_NAME: ['defaults/*']},
    python_requires=">=3.8",
    install_requires=DEPENDENCIES,
)
