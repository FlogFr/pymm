import os
from setuptools import setup

from pypandoc import convert

def read_md(f):
    return convert(f, 'rst')


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Pymm',
    version=read('VERSION'),
    author='aRkadeFR',
    author_email='contact@arkade.info',
    description='Pymm - Python Model Manager',
    license='CC',
    long_description=read_md('README.rst'),
    url='https://github.com/aRkadeFR',
    keywords='pymm model manager postgresql postgres database',
    packages=['pymm', ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Development Status :: 1 - Planning',
    ],
)