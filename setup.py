from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='heartbridge',
    version='1.0.0',
    description='Command line tool to transfer heart rate data from iOS Health to your computer. Works with a companion iOS shortcut.',
    author='Matthew Mascioni',
    author_email='mascionim@gmail.com',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/mm/heartbridge',
    packages=['heartbridge'],
    entry_points={
        'console_scripts': [
            'heartbridge=heartbridge.app:main',
        ],
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords='heartrate apple watch shortcuts',
    python_requires='>=3.6'
)