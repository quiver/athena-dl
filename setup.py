#!/usr/bin/env python
# vim: set fileencoding=utf8 :

from setuptools import setup
 
setup(
    name='Athena-DL',
    version='0.5',
    description='command line interface to query SQL to Amazon Athena and save its results',
    author='George Yoshida',
    url='https://github.com/quiver/athena-dl',
    packages=['athena_dl'],
    include_package_data=True,
    install_requires=[
        'boto3',
        'Click',
        'retrying',
    ],
   classifiers=(
       'Development Status :: 3 - Alpha',
       'License :: OSI Approved :: MIT License',
       'Programming Language :: Python :: 2.7',
   ),
    entry_points='''
        [console_scripts]
        athena-dl=athena_dl.athena_dl:cli
    '''
)
