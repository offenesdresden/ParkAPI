"""open API serving parking lot data for multiple cities
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

from pip.req import parse_requirements

here = path.abspath(path.dirname(__file__))

requirements = parse_requirements(path.join(here, "requirements.txt"), session=False)
install_requires = [str(ir.req) for ir in requirements]

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ParkAPI',
    version='0.0.1',

    description='open API serving parking lot data for multiple cities',
    long_description=long_description,

    url='https://github.com/offenesdresden/ParkAPI',

    author='kilian',
    author_email='me@kilian.io',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Framework :: Flask',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='webapp parkinglots scraping',

    packages=find_packages(exclude=['cache', 'server.log']),

    install_requires=install_requires,

    extras_require={
        'dev': ['pip'],
        'test': [],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        "console_scripts": [
            "parkapi-scraper=park_api.scraper:main",
            "parkapi-server=park_api.server:main",
            "parkapi-setupdb=park_api.setupdb:main",
        ],
    },
)
