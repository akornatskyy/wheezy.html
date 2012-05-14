
Getting Started
===============

Install
-------

:ref:`wheezy.html` requires `python`_ version 2.4 to 2.7 or 3.2.
It is independent of operating system. You can install it from `pypi`_
site using `setuptools`_::

    $ easy_install wheezy.html

If you are using `virtualenv`_::

    $ virtualenv env
    $ env/bin/easy_install wheezy.html

If you would like take a benefit of template preprocessing for Mako
or Tenjin engines specify extra requirements::

    $ env/bin/easy_install wheezy.html[mako]
    $ env/bin/easy_install wheezy.html[tenjin]

Develop
-------

You can get the `source code`_ using `mercurial`_::

    $ hg clone http://bitbucket.org/akorn/wheezy.html
    $ cd wheezy.html

Prepare `virtualenv`_ environment in *env* directory ::

    $ make env

... and run all tests::

    $ make test

You can read how to compile from source code different versions of
`python`_ in the `article`_ published on `mind reference`_ blog.

You can run certain make targets with specific python version. Here
we are going to run `doctest`_ with python3.2::

    $ make env doctest-cover VERSION=3.2

Generate documentation with `sphinx`_::

	$ make doc

If you run into any issue or have comments, go ahead and add on
`bitbucket`_.

.. _`pypi`: http://pypi.python.org/pypi/wheezy.html
.. _`python`: http://www.python.org
.. _`setuptools`: http://pypi.python.org/pypi/setuptools
.. _`bitbucket`: http://bitbucket.org/akorn/wheezy.html/issues
.. _`source code`: http://bitbucket.org/akorn/wheezy.html/src
.. _`mercurial`: http://mercurial.selenic.com/
.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv
.. _`article`: http://mindref.blogspot.com/2011/09/compile-python-from-source.html
.. _`mind reference`: http://mindref.blogspot.com/
.. _`doctest`: http://docs.python.org/library/doctest.html
.. _`sphinx`: http://sphinx.pocoo.org/
