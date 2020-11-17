"""
setup.py - Config for package distribution

@author - jwd3

@copyright:  2017 Equifax. All rights reserved.

@license:    Apache License 2.0

@contact:    jason.decorte@equifax.com

Version History:

"""
from setuptools import setup, find_packages

setup(
    name='pymdrepo',
    version='1.1.0',
    packages=find_packages(),
    url='http://scm.devcentral.equifax.com/svn/GISBI/trunk/app/python/dist/pymdrepo-1.1.0.tar.gz',
    license='GNU General Public License (GPL)',
    author='jwd3',
    author_email='jason.decorte@equifax.com',
    description='EFX Metadata Repository (mdrepo) library package',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only'
    ],
    install_requires=['SQLAlchemy',
                      'pycrypto==2.6.1',
                      'alembic'
                      ],
    include_package_data=False,
    entry_points={},
    scripts=[]
)
