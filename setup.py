# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), 'r') as f:
    long_description = f.read()

version = "0.1.0"

setup(
    name="datadog-deployer",
    packages=["datadog_deployer"],
    entry_points={
        "console_scripts": ['datadog-deployer = datadog_deployer:main']
    },
    version=version,
    description="Deployment of datadog monitors.",
    long_description=long_description,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['ruamel.yaml', 'click', 'datadog'],
    author="Mark van Holsteijn",
    author_email="mvanholsteijn@xebia.com",
    url="https://github.com/binxio/datadog-deployer",
)
