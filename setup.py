#!/usr/bin/env python

import multiprocessing
import os
import platform
import re
import sys

from setuptools import setup

extra = {"ext_modules": []}
try:
    from Cython.Build import cythonize

    p = os.path.join("src", "wheezy", "html")
    extra["ext_modules"] += cythonize(
        [os.path.join(p, "*.py"), os.path.join(p, "ext", "*.py")],
        exclude=[
            os.path.join(p, "__init__.py"),
            os.path.join(p, "ext", "__init__.py"),
        ],
        # https://github.com/cython/cython/issues/3262
        nthreads=0 if multiprocessing.get_start_method() == "spawn" else 2,
        compiler_directives={"language_level": 3},
        quiet=True,
    )
except ImportError:
    pass

can_build_ext = (
    getattr(platform, "python_implementation", lambda: None)() != "PyPy"
    and "java" not in sys.platform
)

if can_build_ext:  # noqa: C901
    from distutils.command.build_ext import build_ext  # noqa
    from distutils.core import Extension  # noqa

    sources = [os.path.join("src", "wheezy", "html", "boost.c")]
    extra["ext_modules"] += [Extension("wheezy.html.boost", sources)]

    class BuildExtOptional(build_ext):
        def run(self):
            from distutils.errors import DistutilsPlatformError

            try:
                build_ext.run(self)
            except DistutilsPlatformError:
                self.warn()

        def build_extension(self, ext):
            from distutils.errors import CCompilerError, DistutilsExecError

            try:
                build_ext.build_extension(self, ext)
            except (CCompilerError, DistutilsExecError):
                self.warn()

        def warn(self):
            print(" WARNING ".center(44, "*"))
            print("An optional extension could not be compiled.")

    extra["cmdclass"] = {"build_ext": BuildExtOptional}

README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()
VERSION = (
    re.search(
        r'__version__ = "(.+)"',
        open("src/wheezy/html/__init__.py").read(),
    )
    .group(1)
    .strip()
)

setup(
    name="wheezy.html",
    version=VERSION,
    python_requires=">=3.8",
    description="A lightweight html rendering library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/akornatskyy/wheezy.html",
    author="Andriy Kornatskyy",
    author_email="andriy.kornatskyy@live.com",
    license="MIT",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Widget Sets",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    keywords="html widget markup mako jinja2 tenjin wheezy.template "
    "preprocessor",
    packages=["wheezy", "wheezy.html", "wheezy.html.ext"],
    package_dir={"": "src"},
    namespace_packages=["wheezy"],
    zip_safe=False,
    extras_require={
        "mako": ["mako>=0.7.0"],
        "tenjin": ["tenjin>=1.1.0"],
        "jinja2": ["jinja2>=2.6"],
        "wheezy.template": ["wheezy.template>=0.1.88"],
    },
    platforms="any",
    **extra
)
