# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(name='neo',
      version='0.1.0',
      description='New Events Officer',
      author='theycallmemac',
      url='https://github.com/theycallmemac/neo',
      license='GPL-3.0',
      scripts=['scripts/neo', 'scripts/main.py'],
      install_requires=[
          'click', 'selenium'
      ],
      classifiers=[
          'Environment :: Console',
          'Natural Language :: English',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.6'])
