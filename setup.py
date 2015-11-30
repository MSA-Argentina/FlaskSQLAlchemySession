#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='Flask-SQLAlchemySession',
    version='0.0.3',
    author='Felipe Lerena',
    author_email='felipelerena@gmail.com',
    packages=['FlaskSQLAlchemySession'],
    scripts=[],
    url='https://github.com/MSA-Argentina/FlaskSQLAlchemySession',
    license='LICENSE.txt',
    description='',
    long_description='',#open('README.txt').read(),
    install_requires=['Flask', 'Flask-SQLAlchemy'],
)
