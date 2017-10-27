#!/usr/bin/env python

import os
from setuptools import setup

# TODO: Bad, but some dependencies weren't installing correctly
os.system('pip install -r requirements.txt')

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='dino',
    version='0.0.1',
    description='Dino',
    author='Daniel Suo',
    author_email='dsuo@cs.princeton.edu',
    url='https://github.com/danielsuo/dino',
    packages=['dino'])
