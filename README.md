# wheezy.html

[![Build Status](https://travis-ci.org/akornatskyy/wheezy.html.svg?branch=master)](https://travis-ci.org/akornatskyy/wheezy.html)
[![Documentation Status](https://readthedocs.org/projects/wheezyhtml/badge/?version=latest)](https://wheezyhtml.readthedocs.io/en/latest/?badge=latest)

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
- [documentation](http://readthedocs.org/builds/wheezyhtml)

## Install

[wheezy.html](https://pypi.org/project/wheezy.html) requires
[python](http://www.python.org) version 2.4 to 2.7 or 3.2+. It is
independent of operating system. You can install it from
[pypi](https://pypi.org/project/wheezy.html) site:

```sh
pip install wheezy.html
```

If you would like take a benefit of template preprocessing for Mako,
Jinja2, Tenjin or Wheezy.Template engines specify extra requirements:

```sh
pip install wheezy.html[jinja2]
pip install wheezy.html[wheezy.template]
```

If you run into any issue or have comments, go ahead and add on
[github](https://github.com/akornatskyy/wheezy.html/issues).