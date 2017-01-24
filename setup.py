#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='engineering_project',
    version='0.1.0',
    description="Engineering project to operate a test system to IEC 61000-4-6:2014 and IEC 61000-4-3:2006+A2:2010 and ISO/IEC 17025:2005",
    long_description=readme + '\n\n' + history,
    author="David A Lutton",
    author_email='david@dalun.space',
    url='https://github.com/DavidLutton/engineering_project',
    packages=[
        'engineering_project',
    ],
    package_dir={'engineering_project':
                 'engineering_project'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='engineering_project',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
