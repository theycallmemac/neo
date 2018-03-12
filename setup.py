# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from yaml import load, dump, YAMLError
from getpass import getpass

with open("config.yaml", 'r') as f:
    try:
        config = load(f)
        name = input("Your name: ")
        fb_log = input("Your Facebook sign in (email or phone number): ")
        fb_pw = getpass("Your Facebook password: ")
        gmail = input("Your DCU email: ")
        dcu_uname = input("Your DCU username: ")
        dcu_pw = getpass("Your DCU password: ")
        driver = input("Your browser (Firefox, Chrome supported only): ")
        config['config']['name'] = name
        config['config']['facebook_login'] = fb_log
        config['config']['facebook_pw'] = fb_pw
        config['config']['gmail'] = gmail
        config['config']['dcu_uname'] = dcu_uname
        config['config']['dcu_pw'] = dcu_pw
        config['config']['driver'] = driver.lower().strip()

        with open("config.yaml", 'w') as f:
            dump(config, f)
    except YAMLError as e:
        print(e)

setup(name='neo',
      version='0.1.0',
      description='New Events Officer',
      author='theycallmemac',
      url='https://github.com/theycallmemac/neo',
      license='GPL-3.0',
      scripts=['scripts/neo', 'scripts/main.py'],
      install_requires=[
          'click', 'selenium', 'pyyaml'
      ],
      classifiers=[
          'Environment :: Console',
          'Natural Language :: English',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.6'])
