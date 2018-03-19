#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from yaml import load, dump, YAMLError
from getpass import getpass
from base64 import b64encode as b64
from os import system
with open("config.yaml", 'r') as f:
    try:
        config = load(f)
        name = input("Your name: ")
        fb_log = b64(
            input("Your Facebook sign in (email or phone number): ").encode())
        fb_pw = b64(getpass("Your Facebook password: ").encode())
        gmail = b64(input("Your DCU email: ").encode())
        dcu_uname = b64(input("Your DCU username: ").encode())
        dcu_pw = b64(getpass("Your DCU password: ").encode())
        driver = b64(input("Firefox or Chrome?: ").encode())
        config['config']['name'] = name
        config['config']['facebook_login'] = fb_log
        config['config']['facebook_pw'] = fb_pw
        config['config']['gmail'] = gmail
        config['config']['dcu_uname'] = dcu_uname
        config['config']['dcu_pw'] = dcu_pw
        config['config']['driver'] = driver

        with open("config.yaml", 'w') as f:
            dump(config, f)
    except YAMLError as e:
        print(e)

system("chmod +x install_driver.sh && ./install_driver.sh")

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
