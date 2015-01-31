#!python
# -*- coding: utf-8 -*-
import sys, os, re
from os.path import dirname, abspath, join
from setuptools import setup, find_packages


HERE = abspath(dirname(__file__))
readme = open(join(HERE, 'README.md')).read()

package_file = open(join(HERE, 'munch', '__init__.py'), 'rU')
__version__ = re.sub(
    r".*\b__version__\s+=\s+'([^']+)'.*",
    r'\1',
    [ line.strip() for line in package_file if '__version__' in line ].pop(0)
)


setup(
    name             = "munch",
    version          = __version__,
    description      = "A dot-accessible dictionary (a la JavaScript objects)",
    long_description = readme,
    url              = "http://github.com/Infinidat/munch",

    author           = "Rotem Yaari",
    author_email     = "vmalloc@gmail.com",

    packages         = find_packages(exclude=["tests"]),
    keywords         = ['munch', 'dict', 'mapping', 'container', 'collection'],
    classifiers      = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: PyPy'
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    license          = 'MIT',
)
