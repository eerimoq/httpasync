#!/usr/bin/env python3

import re
import setuptools
from setuptools import find_packages


def find_version():
    return re.search(r"^__version__ = '(.*)'$",
                     open('httpasync/version.py', 'r').read(),
                     re.MULTILINE).group(1)


setuptools.setup(
    name='httpasync',
    version=find_version(),
    description='HTTP Async.',
    long_description=open('README.rst', 'r').read(),
    author='Erik Moqvist',
    author_email='erik.moqvist@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords=['http'],
    url='https://github.com/eerimoq/httpasync',
    packages=find_packages(exclude=['tests']),
    test_suite="tests")
