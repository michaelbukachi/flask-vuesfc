# -*- coding: UTF-8 -*-
"""
Flask-VueSFC
-------------
Flask extension for rendering Vue.js SFCs
"""
try:
    from setuptools import setup
except:
    from distutils.core import setup

import codecs


version = '0.1.3'

setup(
    name='Flask-VueSFC',
    version=version,
    url='https://github.com/michaelbukachi/flask-vuesfc',
    license='MIT',
    author='Michael Bukachi',
    author_email='michaelbukachi@gmail.com',
    description='Flask extension for rendering Vue.js SFCs',
    long_description=codecs.open('README.rst', 'r', 'utf-8').read(),
    packages=['flask_vue_sfc'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.11',
        'py-mini-racer>=0.4.0',
        'tinycss2>=1.0.2',
        'esprima>=4.0.1',
        'css-html-js-minify',
        'libsass>=0.20.1'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)