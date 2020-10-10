# -*- coding: UTF-8 -*-
"""
Flask-Vue-SFC
-------------
Flask extension for rendering Vue.js SFCs
"""
try:
    from setuptools import setup
except:
    from distutils.core import setup

import codecs

version = '0.0.1'

setup(
    name='Flask-Vue-SFC',
    version=version,
    url='https://github.com/michaelbukachi/flask_vue_sfc',
    license='Apache',
    author='Michael Bukachi',
    author_email='michaelbukachi@gmail.com',
    description='Flask extension for rendering Vue.js SFCs',
    long_description=codecs.open('README.rst', 'r', 'utf-8').read(),
    packages=['flask_vue_sfc'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.11'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)