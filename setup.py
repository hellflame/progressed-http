# coding=utf8
from __future__ import absolute_import, division, print_function

from setuptools import setup
from ProgressedHttp import __author__, __author_email__, __version__, __url__

setup(
    name='progressed-http',
    version=__version__,
    keywords=('http req/resp handle', 'progress bar', 'simple'),
    description="Personal http req/resp handler with origin progress bar support",
    long_description="More Detail, visit `{url} <{url}>`_".format(url=__url__),
    license='MIT',
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    packages=['ProgressedHttp'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Environment :: Console",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
