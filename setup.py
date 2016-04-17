import os
from setuptools import setup
from test.support import CoverageAnalysisTestCommand


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_version(fname):
    return read(fname).strip()


setup(
    name='Pymm',
    version=read_version('VERSION'),
    author='aRkadeFR',
    author_email='contact@arkade.info',
    description='Pymm - Python Model Manager',
    license='CC',
    long_description=read('README.rst'),
    url='https://github.com/aRkadeFR',
    keywords='pymm model manager postgresql postgres database',
    packages=['pymm', ],
    scripts=['bin/pymm'],
    install_requires=[
        'psycopg2>=2.6.1',
        'six>=1.10.0',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Development Status :: 1 - Planning',
    ],
    cmdclass={
        'test': CoverageAnalysisTestCommand,
    },
    tests_require=[
        'coverage>=4.0.3',
    ],
    test_suite='tests',
)
