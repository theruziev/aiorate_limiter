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
            'faker==18.3.1',
            'flake8-bandit==4.1.1',
            'pep8-naming==0.13.3',
            'flake8==6.0.0',
            'coverage==7.2.4',
            'pytest==7.2.2',
            'pytest-asyncio==0.20.3',
            'black==23.1.0',
            'asynctest==0.13.0',
            'mypy==1.1.1',
        ]
    }
)
