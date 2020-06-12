
Examples
========

Before we proceed let's setup a `virtualenv`_ environment, activate it and
install::

    $ pip install wheezy.html


.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv

Signin Widget
-------------

Suppose we need to add user credential input to an HTML form. In case of error it would
be good to display it next to each input. Domain model looks like this::

    class Credential(object):

        def __init__(self):
            self.username = ''
            self.password = ''

Here is what we can get in html template::

    >>> from wheezy.html import widget
    >>> credential = Credential()
    >>> errors = {}
    >>> credential = widget(credential, errors)
    >>> credential.username.label('Username:')
    <label for="username">Username:</label>
    >>> credential.username.textbox(autocomplete='off')
    <input autocomplete="off" type="text" id="username"
      value="" name="username" />
    >>> credential.username.error()

Look how this changes in case of errors::

    >>> errors = {'username': ['Required field cannot be left blank.']}
    >>> credential = widget(credential, errors)
    >>> credential.username.label('Username:')
    <label class="error" for="username">Username:</label>
    >>> credential.username.textbox(autocomplete='off')
    <input name="username" value="" autocomplete="off"
       class="error" type="text" id="username" />
    >>> credential.username.error()
    <span class="error">Required field cannot be left blank.</span>

General error message::

    >>> errors = {'__ERROR__': ['The username or password provided is incorrect.']}
    >>> credential = widget(credential, errors)
    >>> credential.error()
    <span class="error-message">The username or password
      provided is incorrect.</span>
