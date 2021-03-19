#!/usr/bin/env python
"""installer for resumator"""
from distutils.core import setup

setup(name='resumator',
      version='0.0',
      description='Generator for resumes',
      author='Juniper Overbeck',
      author_email='nodeadtree@gmail.com',
      packages=['resumator'],
      scripts=['scripts/resumator']
      )
