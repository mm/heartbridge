#!/user/bin/env python3

from setuptools import setup, find_packages

setup(
    name='Heartbridge',
    version='2.0',
    description='Command line tool to transfer heart rate data from iOS Health to your computer.',
    author='Matthew Mascioni',
    author_email='mascionim@gmail.com',
    packages=['heartbridge'],
    entry_points={
        'console_scripts': [
            'heartbridge=heartbridge.app:main',
        ],
    }   
)