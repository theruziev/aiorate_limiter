import os
from distutils.core import setup

from setuptools import find_packages

from aiorate_limiter.version import __version__

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name="aiorate_limiter",
    version=__version__,
    packages=find_packages(),
    url='https://github.com/theruziev/rate_limiter',
    license='MIT',
    author='Bakhtiyor Ruziev',
    author_email='bakhtiyor.ruziev@yandex.ru',
    description='rate-limiter',
    long_description=README,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    extras_require={
        'aioredis:python_version<"3.7"': ['aioredis>=0.3.3'],
        'aioredis:python_version>="3.7"': ['aioredis>=1.0.0'],
        'dev': [
            'faker==9.8.0',
            'flake8-bandit==2.1.2',
            'pep8-naming==0.11.1',
            'flake8==4.0.1',
            'coverage==6.1.1',
            'pytest==6.2.5',
            'pytest-asyncio==0.16.0',
            'black==21.10b0',
            'asynctest==0.13.0',
            'mypy==0.910',
        ]
    }
)
