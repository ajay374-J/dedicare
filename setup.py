# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in dedicare/__init__.py
from dedicare import __version__ as version

setup(
	name='dedicare',
	version=version,
	description='Customize solution',
	author='Ajay',
	author_email='ajayjogdand374@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
