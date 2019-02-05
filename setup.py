"""A setup module for portbalance."""

from setuptools import setup

setup(
    name='portbalance',
    version='0.1.0',
    author='William Gilpin',
    author_email='wgilpin@stanford.edu',
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    description='A lightweight python library for maintaining and monitoring a stock portfolio',
    keywords="finance portfolio rebalancing stock",
    python_requires='>=3',
    install_requires=[
        'numpy', 
        'matplotlib',
        'pandas',
        'pandas-datareader'
    ],
    # This line tells setup.py to add non-Python files from the root-level MANIFEST.in file
    include_package_data=True, 
    packages=["portbalance"],
    url='https://github.com/williamgilpin/portbalance'
)