#!/usr/bin/env python

from setuptools import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session='hack')

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='dino',
    version='0.0.1',
    description='Dino',
    author='Daniel Suo',
    author_email='dsuo@cs.princeton.edu',
    url='https://github.com/danielsuo/dino',
    packages=['dino'],
    install_requires=reqs)
