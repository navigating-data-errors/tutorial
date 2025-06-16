"""
For 'python setup.py develop' and 'python setup.py test'
"""
import os
from setuptools import setup, find_packages

ROOT = os.path.dirname(__file__)

with open(os.path.join(ROOT, "requirements.txt"), encoding="utf-8") as f:
    required = f.read().splitlines()

setup(
    name="nde",
    version="0.0.1.dev0",
    description="Navigating data errors tutorial",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    license='Apache License 2.0',
    python_requires='==3.11.*',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10'
    ]
)
