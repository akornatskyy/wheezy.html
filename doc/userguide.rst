
User Guide
==========

Core feature of :ref:`wheezy.html`
is :py:class:`~wheezy.html.factory.WidgetFactory`. This class has shortcut
``widget``. You instantiate :py:class:`~wheezy.html.factory.WidgetFactory`
and pass the following arguments:

* ``model`` - object being wrapped.
* ``errors`` - dictionary contains all errors reported; ``key`` corresponds to
  attribute name, while ``value`` is a list of errors.

Let declare our domain model::

    class Credential(object):

        def __init__(self):
            self.username = ''
            self.password = ''

This way we get HTML widget::

    from wheezy.html import widget

    credential = Credential()
    errors = {}
    credential = widget(credential, errors)

Widget Name
~~~~~~~~~~~

Each attribute in widget corresponds to appropriate attribute in ``model``.
Attribute name becomes ``name`` in html element. Convention for html ``id``
is replace underscope with dash. So attribute ``confirm_password`` remains
unchanged in html name, however id will be ``confirm-password``.

Widget Rendering
~~~~~~~~~~~~~~~~

Once we know name of html widget, next pass control to appropriate
widget for rendering::

    credential.username.textbox(autocomplete='off')

Let explain this single line:

* ``credential`` - an instance of
  :py:class:`~wheezy.html.factory.WidgetFactory` that wraps ``model`` and
  ``errors``.
* ``username`` - attribute name of our domain object.
* ``textbox`` - widget we need to render.
* ``autocomplete`` - html specific attribute.

Once that code is executed we get the following::

    <input autocomplete="off" type="text" id="username"
      value="" name="username" />

Value Formatting
~~~~~~~~~~~~~~~~

You can format model value before it is passed to widget for rendering.

Let declare our domain model::

    from datetime import date

    class Registration(object):

        def __init__(self):
            self.date_of_birth = date.min

Here is how you can apply formatting::

    registration.date_of_birth.format('%Y/%m/%d')

or this way::

    registration.date_of_birth.format(
            format_provider=lambda value, ignore: value.strftime('%m-%d-%y'))

Widget formatting can follow by actual widget that needs to be rendered::

    registration.date_of_birth.format('%Y/%m/%d').textbox()

``format_provider`` - a callable of the following form::

    def my_format_provider(value, format_string):
        return value_formatted

There are default format providers for built-in types. You can replace and
extend it with your own by altering ``format_providers`` map::

    from wheezy.html.utils import format_providers

    format_providers['my_type'] = my_format_provider

Default implementation for date/time types formats it minimal value to empty
string.

Model Error
~~~~~~~~~~~

Since ``widget`` is initialized with model and errors, it capable to
decorate html widget with attributes specific to errors. Let see this
in the following example::

    errors = {'username': ['Required field cannot be left blank.']}

We get the errors from some sort of validation. The same ``textbox`` is now
decorated with class error::

    <input name="username" value="" autocomplete="off"
       class="error" type="text" id="username" />

So I can apply appropriate css style to draw a border around input, or what
ever else since in html I have distinguished situation between input with
error and with valid input.

Now let display error::

    credential.username.error()

Read above as render error message for username, here is what we get::

    <span class="error">Required field cannot be left blank.</span>

General Error
~~~~~~~~~~~~~

General error is not related to certain model attribute but to operation
related instead. If ``errors`` dictionary contains an element with __ERROR__
key than that one is used as general error::

    errors = {'__ERROR__': 'The username or password provided is incorrect.'}

You can display it this way::

    credential.error()

It renders the following html element only if __ERROR__ key exists::

    <span class="error-message">The username or password
      provided is incorrect.</span>

Notice class ``error-message``. Your application is able to distinguish field
errors from general errors.

Widgets
~~~~~~~

:ref:`wheezy.html` comes with a number of built-in widgets. They can be
generally divided into two categories with support of a single value
(``string``, ``int``, ``datetime``, etc) or multiple (``list`` or ``tuple``).

Single value widgets:

* :py:meth:`~wheezy.html.widgets.hidden` - html element input of type hidden.
* :py:meth:`~wheezy.html.widgets.emptybox` - html element input of type text,
  value is rendered only if evaluated to boolean True..
* :py:meth:`~wheezy.html.widgets.textbox` - html element input of type text,
  value is rendered only if it is not None or ''.
* :py:meth:`~wheezy.html.widgets.password` - html element input of type
  password, value is rendered only if it is not None or ''.
* :py:meth:`~wheezy.html.widgets.textarea` - html element textarea.
* :py:meth:`~wheezy.html.widgets.checkbox` - html element input of type
  checkbox.
* :py:meth:`~wheezy.html.widgets.label` - html element label.
* :py:meth:`~wheezy.html.widgets.dropdown` - html element select (there is
  also synonym ``select``). Attribute ``choices`` is a list of html options.
* :py:meth:`~wheezy.html.widgets.radio` - a group of html input elements
  of type radio. Attribute ``choices`` is a list of options.

Widgets that support multiple values:

* :py:meth:`~wheezy.html.widgets.multiple_hidden` - renders several html
  input elements of type hidden per item in the value list.
* :py:meth:`~wheezy.html.widgets.multiple_checkbox` - renders several
  html elements of type checkbox per item in the value list nested into
  html label element.
* :py:meth:`~wheezy.html.widgets.listbox` - html element select of type
  multiple (there is also synonym ``multiple_select``). Attribute
  ``choices`` is a list of html options.

Several widgets support ``choinces`` attribute, it is an iteratable of tuple
of two::

    account_types = (('u', 'User'), ('b', 'Business'))
    account.account_type.radio(choices=account_types)

It renders the following html::

    <label><input checked="checked" type="radio"
        name="account_type" value="1" />User</label>
    <label><input type="radio" name="account_type"
        value="2" />Business</label>

It is sometimes more convinient to operate with dictionary::

    >>> from operator import itemgetter
    >>> account_types = sorted({'u': 'User', 'b': 'Business'}.items(),
    ...         key=itemgetter(1))
    >>> account_types
    [('u', 'User'), ('b', 'Business')]


Custom Widgets
~~~~~~~~~~~~~~

It is easy to provide own widgets. A widget is any callable of the following
contract::

    from wheezy.html.markup import Tag

    def my_widget(name, value, attrs):
        tag_attrs = {
            'id' = id(name)
        }
        if attrs:
            tag_attrs.update(attrs)
        return Tag('name', value, attrs=tag_attrs)

Here is a description of each attribute:

* ``name`` - name of model attribute.
* ``value`` - value that is currently rendered.
* ``attrs`` - a dictionary of extra key-word arguments passed.

Your custom widget must return an instance of
:py:class:`~wheezy.html.markup.Tag` or
:py:class:`~wheezy.html.markup.Fragment`. In case of field error html element
is decorated with css class ``error``.

Registration
^^^^^^^^^^^^

Once ``my_widget`` is ready you can add it to a list of default widgets::

    from wheezy.html.widgets import default as default_widgets

    default_widgets['my_widget'] = my_widget

Now you should be able to use it::

    credential.username.my_widget()

Since ``default_widgets`` is python dictionary you can manipulate it a way you
like.

Integration
~~~~~~~~~~~

:ref:`wheezy.html` integrates with the following template systems:

* `Mako Templates for Python <http://www.makotemplates.org>`_
* `Tenjin Templates for Python <http://www.kuwata-lab.com/tenjin/>`_

Mako
^^^^

:ref:`wheezy.html` integration with ``Mako`` is provided via preprocessor
feature. Here is how to add
:py:meth:`~wheezy.html.ext.mako.widget_preprocessor` to your code::

    from wheezy.html.ext.mako import widget_preprocessor

    template_lookup = TemplateLookup(
            ...
            preprocessor=[widget_preprocessor])

The only thing :py:meth:`~wheezy.html.ext.mako.widget_preprocessor` does is
translation of widget code to adequate ``Mako`` code.

Let demonstrate with by example::

    ${model.remember_me.checkbox()}

is translated to the following ``Mako`` code (during template compilation
phase)::

    <input id="remember-me" name="remember_me" type="checkbox" value="1"\
    % if 'remember_me' in errors:
     class="error"\
    % endif
    % if model.remember_me:
     checked="checked"\
    % endif
     />

which effectively renders the HTML at runtime::

    <input id="remember-me" name="remember_me" type="checkbox" value="1" />

Since widgets also decorate appropriate HTML tags in case of error, ``errors``
dictionary must be available in ``Mako`` context::

    template = template_lookup.get_template(template_name)
    assert 'errors' in kwargs
    template.render(
                **kwargs
    )

See :py:mod:`wheezy.html.ext.mako` for more examples.

Tenjin
^^^^^^

:ref:`wheezy.html` integration with ``Tenjin`` is provided via preprocessor
feature. Here is how to add
:py:meth:`~wheezy.html.ext.tenjin.widget_preprocessor` to your code::

    from wheezy.html.ext.mako import widget_preprocessor

    engine = tenjin.Engine(
            ...
            pp=[widget_preprocessor])

The only thing :py:meth:`~wheezy.html.ext.mako.widget_preprocessor` does is
translation of widget code to adequate ``Tenjin`` code.

Let demonstrate with by example::

    ${model.remember_me.checkbox(class_='i')}

is translated to the following ``Tenjin`` code (during template compilation
phase)::

    <input id="remember-me" name="remember_me" type="checkbox" value="1"<?py #pass ?>
    <?py if 'remember_me' in errors: ?>
     class="error i"<?py #pass ?>
    <?py else: ?>
     class="i"<?py #pass ?>
    <?py #endif ?><?py if model.remember_me: ?>
     checked="checked"<?py #pass ?>
    <?py #endif ?>
     />

which effectively renders the HTML at runtime::

    <input id="remember-me" name="remember_me" type="checkbox"
        value="1" class="i" />

Since widgets also decorate appropriate HTML tags in case of error, ``errors``
dictionary must be available in ``Tenjin`` context::

    assert 'errors' in kwargs
    engine.render('page.html',
                **kwargs
    )

See :py:mod:`wheezy.html.ext.tenjin` for more examples.
