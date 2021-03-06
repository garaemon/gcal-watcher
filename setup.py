#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of gcal-watcher.
# http://github.com/garaemon/gcal-watcher

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2018, garaemon <garaemon@gmail.com>

from setuptools import setup, find_packages
from gcal_watcher import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='gcal-watcher',
    version=__version__,
    description='an incredible python package',
    long_description='''
an incredible python package
''',
    keywords='',
    author='garaemon',
    author_email='garaemon@gmail.com',
    url='http://github.com/garaemon/gcal-watcher',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'apiclient',
        'google-api-python-client',
        'python-dateutil',
        'requests',
        'fire',
        'pytz',
        'inquirer'
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            'gcal-watcher=gcal_watcher.cli:main',
            'gcal-watcher-deploy=gcal_watcher.deploy:main',
        ],
    },
)
