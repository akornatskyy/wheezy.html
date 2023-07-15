# wheezy.html

[![Build Status](https://travis-ci.org/akornatskyy/wheezy.html.svg?branch=master)](https://travis-ci.org/akornatskyy/wheezy.html)
[![Coverage Status](https://coveralls.io/repos/github/akornatskyy/wheezy.html/badge.svg?branch=master)](https://coveralls.io/github/akornatskyy/wheezy.html?branch=master)
[![Documentation Status](https://readthedocs.org/projects/wheezyhtml/badge/?version=latest)](https://wheezyhtml.readthedocs.io/en/latest/?badge=latest)
[![pypi version](https://badge.fury.io/py/wheezy.html.svg)](https://badge.fury.io/py/wheezy.html)

[wheezy.html](https://pypi.org/project/wheezy.html) is a
[python](http://www.python.org) package written in pure Python code. It
is a lightweight html widget library. Integrates with the following
template systems:

- [Jinja2 Templates](http://jinja.pocoo.org)
- [Mako Templates](http://www.makotemplates.org)
- [Tenjin Templates](http://www.kuwata-lab.com/tenjin/)
- [Wheezy Templates](http://pypi.python.org/pypi/wheezy.template/)

It is optimized for performance, well tested and documented.

Resources:

- [source code](https://github.com/akornatskyy/src) and
  [issues](https://github.com/akornatskyy/wheezy.html/issues) tracker are
  available on [github](https://github.com/akornatskyy/wheezy.html)
- [documentation](https://wheezyhtml.readthedocs.io/en/latest/)

## Install

[wheezy.html](https://pypi.org/project/wheezy.html) requires
[python](http://www.python.org) version 3.8+. It is independent of operating
system. You can install it from [pypi](https://pypi.org/project/wheezy.html)
site:

```sh
pip install -U wheezy.html
```

If you would like take a benefit of template preprocessing for Mako,
Jinja2, Tenjin or Wheezy.Template engines specify extra requirements:

```sh
pip install wheezy.html[wheezy.template]
```

If you run into any issue or have comments, go ahead and add on
[github](https://github.com/akornatskyy/wheezy.html/issues).
