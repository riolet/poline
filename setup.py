import sys
import subprocess
from setuptools import setup, Command

setup(
    name='poline',
    version='0.1',
    description='Python one-liners: Awk-like one-liners for python',
    long_description='pol lets you do awk-like one liners in python.',
    url='https://github.com/riolet/pol',
    author='Rohana Rezel',
    author_email='poline@riolet.com',
    maintainer='Rohana Rezel',
    maintainer_email='poline@riolet.com',
    packages = ['poline'],
    entry_points={
        'console_scripts': ['pol = poline.poline:main'],
    },
    classifiers=[
        'Topic :: System :: Operating System'
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: MIT',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)