#!/usr/bin/env python

import os
import platform
import sys

extra = {}
can_build_ext = getattr(platform, 'python_implementation', lambda: None
                   )() != 'PyPy' and 'java' not in sys.platform
sources = [os.path.join('src', 'wheezy', 'html', 'boost.c')]

try:
    from setuptools import setup, Extension, Feature
    from setuptools.command.build_ext import build_ext
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command.build_ext import build_ext
    if can_build_ext:
        extra['ext_modules'] = [Extension('wheezy.html.boost', sources)]
else:
    if can_build_ext:
        extra['features'] = {
            'boost': Feature(
                'code optimizations',
                standard=True,
                ext_modules=[Extension('wheezy.html.boost', sources)])
        }


if can_build_ext:

    class build_ext_optional(build_ext):

        def run(self):
            from distutils.errors import DistutilsPlatformError
            try:
                build_ext.run(self)
            except DistutilsPlatformError:
                self.warn()

        def build_extension(self, ext):
            from distutils.errors import CCompilerError
            from distutils.errors import DistutilsExecError
            try:
                build_ext.build_extension(self, ext)
            except (CCompilerError, DistutilsExecError):
                self.warn()

        def warn(self):
            print(' WARNING '.center(44, '*'))
            print('An optional extension could not be compiled.')

    extra['cmdclass'] = {'build_ext': build_ext_optional}


README = open(os.path.join(os.path.dirname(__file__), 'README')).read()

setup(
    name='wheezy.html',
    version='0.1',
    description='A lightweight html rendering library',
    long_description=README,
    url='https://bitbucket.org/akorn/wheezy.html',

    author='Andriy Kornatskyy',
    author_email='andriy.kornatskyy at live.com',

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
    keywords='html widget markup mako jinja2 tenjin wheezy.template '
             'preprocessor',
    packages=['wheezy', 'wheezy.html', 'wheezy.html.ext'],
    package_dir={'': 'src'},
    namespace_packages=['wheezy'],

    zip_safe=False,
    install_requires=[
    ],
    extras_require={
        'dev': [
            'coverage',
            'nose',
            'pytest',
            'pytest-pep8',
            'pytest-cov',
        ],
        'mako': [
            'mako>=0.7.0'
        ],
        'tenjin': [
            'tenjin>=1.1.0'
        ],
        'jinja2': [
            'jinja2>=2.6'
        ],
        'wheezy.template': [
            'wheezy.template>=0.1.88'
        ]
    },

    platforms='any',
    **extra
)
