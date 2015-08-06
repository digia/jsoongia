#!/usr/bin/env python

from setuptools import setup
from jsoongia import VERSION


setup(
    name='jsoongia',
    version=VERSION,
    url='https://github.com/digia/jsoongia',
    author='Jonathon Moore',
    author_email='jon@digia.io',
    description='Framework agnostic JSON API serializer',
    keywords='JSON, JSON API, Serializeer',
    license=open('LICENSE').read(),
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - ALPHA',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: OS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
