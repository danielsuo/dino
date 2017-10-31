#!/usr/bin/env python

import os
from setuptools import setup, find_packages

# TODO: Bad, but some dependencies weren't installing correctly
os.system('pip install -r requirements.txt')

setup(
    name='dino',
    version='0.0.1',
    description='Dino',
    author='Daniel Suo',
    author_email='dsuo@cs.princeton.edu',
    url='https://github.com/danielsuo/dino',
    install_requires=[
        'click'
    ],
    packages=['dino'],
    entry_points='''
        [console_scripts]
        dino=dino.cli:cli
    ''')
