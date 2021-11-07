#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    'pyvisa',
    'pyvisa-py',
    'pyvisa-sim',
    'numpy',
    'pandas',
    # 'pint',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='LabToolkit',
    version='0.1.3',
    description="Python package for instrument control, data acquisition and automation.",
    long_description=readme,  # + '\n\n' + history,
    author="David A Lutton",
    author_email='david@dalun.space',
    url='https://github.com/DavidLutton/LabToolkit',
    packages=[
        'labtoolkit',
    ],
    package_dir={'labtoolkit':
                 'labtoolkit'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='labtoolkit',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    long_description_content_type='text/markdown',
)
