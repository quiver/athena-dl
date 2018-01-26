#!/usr/bin/env python
# vim: set fileencoding=utf8 :

from setuptools import setup
 
setup(
    name='Athena-DL',
    version='0.1',
    description='CLI to ',
    author='George Yoshida',
    url='https://github.com/quiver/athena-dl',
    py_modules=['athena'],
    install_requires=[
        'Click',
        'retry',
    ],
   classifiers=(
       'Development Status :: 3 - Alpha',
       'License :: OSI Approved :: MIT License'
       'Programming Language :: Python :: 2.7',
   ),
    entry_points='''
        [console_scripts]
        athena-dl=athena_dl:cli
    '''
)
