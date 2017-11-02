import os
from setuptools import setup, find_packages

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
