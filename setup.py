#!/usr/bin/env python
# vim: set fileencoding=utf8 :

from setuptools import setup
 
setup(
    name='Athena-DL',
    version='0.1',
    py_modules=['athena'],
    install_requires=[
        'Click',
        'retry',
    ],
    entry_points='''
        [console_scripts]
        athena-dl=athena_dl:cli
    '''
)
