
User Guide
==========

Widget Name
~~~~~~~~~~~

Each attribute in widget corresponds to an appropriate attribute in ``model``.
Attribute name becomes ``name`` in the html element. By convention in html ``id``
underscore is replaced with dash. So attribute ``confirm_password`` remains
unchanged in html name, however id will be ``confirm-password``.

Widget Rendering
~~~~~~~~~~~~~~~~

Once we know the name of the html widget, next we pass control to the appropriate
widget for rendering::

    credential.username.textbox(autocomplete='off')

Let's explain this single line:

* ``credential`` - domain object.
* ``username`` - attribute name of our domain object.
* ``textbox`` - widget we need to render.
* ``autocomplete`` - html specific attribute.

Once that code is executed we get the following::

    <input autocomplete="off" type="text" id="username"
      value="" name="username" />

Value Formatting
~~~~~~~~~~~~~~~~

You can the format model value before it is passed to widget for rendering.

Let's declare our domain model::

    from datetime import date

    class Registration(object):

        def __init__(self):
            self.date_of_birth = date.min

Here is how you can apply formatting::

    registration.date_of_birth.format('%Y/%m/%d')

or this way::

    registration.date_of_birth.format(
            format_provider=lambda value, ignore: value.strftime('%m-%d-%y'))

Widget formatting can followed by the actual widget that needs to be rendered::

    registration.date_of_birth.format('%Y/%m/%d').textbox()

``format_provider`` - a callable of the following form::

    def my_format_provider(value, format_string):
        return value_formatted

There are default format providers for built-in types. You can replace and
extend them with your own, by altering ``format_providers`` map::

    from wheezy.html.utils import format_providers

    format_providers['my_type'] = my_format_provider

Default implementation for date/time types formats its minimal value to an empty
string.

Model Error
~~~~~~~~~~~

Since ``widget`` is initialized with model and errors, it is capable of
decorating html widgets with attributes specific to errors. Let's see this
in the following example::

    errors = {'username': ['Required field cannot be left blank.']}

We get the errors from some sort of validation. The same ``textbox`` is now
decorated with class error::

    <input name="username" value="" autocomplete="off"
       class="error" type="text" id="username" />

So I can apply appropriate css style to draw a border around input, or what
ever else, since in html I have distinguished between input with
error and valid input.

Now let display error::

    credential.username.error()

Read above as render error message for username, here is what we get::

    <span class="error">Required field cannot be left blank.</span>

General Error
~~~~~~~~~~~~~

General error is not related to certain model attribute but is operation
related instead. If ``errors`` dictionary contains an element with key __ERROR__
than that one is used as a general error::

    errors = {'__ERROR__': 'The username or password provided is incorrect.'}

You can display it this way::

    credential.error()

It renders the following html element only if the __ERROR__ key exists::

    <span class="error-message">The username or password
      provided is incorrect.</span>

Notice class ``error-message``. Your application is able to distinguish field
errors from general errors.

Integration
~~~~~~~~~~~

:ref:`wheezy.html` integrates with the following template systems:

* `Jinja2 Templates <http://jinja.pocoo.org>`_
* `Mako Templates <http://www.makotemplates.org>`_
* `Tenjin Templates <http://www.kuwata-lab.com/tenjin/>`_
* `Wheezy Templates <http://pypi.python.org/pypi/wheezy.template/>`_

Jinja2
^^^^^^

:ref:`wheezy.html` integration with ``Jinja2`` is provided via the extension
feature. Here is how to add
:py:meth:`~wheezy.html.ext.jinja2.WidgetExtension` to your code::

    from wheezy.html.ext.jinja2 import WidgetExtension

    env = Environment(
            ...
            extensions=[WidgetExtension])

The only thing :py:meth:`~wheezy.html.ext.jinja2.WidgetExtension` does is
translation of widget code to adequate ``Jinja2`` code.

Let's demonstrate this with an example::

    {{ model.remember_me.checkbox() }}

is translated to the following ``Jinja2`` code (during template compilation
phase)::

    <input id="remember-me" name="remember_me" type="checkbox"
    value="1"
    {% if 'remember_me' in errors: %}
     class="error"
    {% endif %}
    {% if  model.remember_me: %}
     checked="checked"
    {% endif %} />

which effectively renders the HTML at runtime::

    <input id="remember-me" name="remember_me" type="checkbox" value="1" />

Since widgets also decorate appropriate HTML tags in case of error, the ``errors``
dictionary must be available in the ``Jinja2`` context::

    template = env.get_template(template_name)
    assert 'errors' in kwargs
    template.render(
                **kwargs
    )

See :py:mod:`wheezy.html.ext.jinja2` for more examples.


Mako
^^^^

:ref:`wheezy.html` integration with ``Mako`` is provided via the preprocessor
feature. Here is how to add
:py:meth:`~wheezy.html.ext.mako.widget_preprocessor` to your code::

    from wheezy.html.ext.mako import widget_preprocessor

    template_lookup = TemplateLookup(
            ...
            preprocessor=[widget_preprocessor])

The only thing :py:meth:`~wheezy.html.ext.mako.widget_preprocessor` does is
translation of widget code to adequate ``Mako`` code.

Let's demonstrate this with an example::

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

Since widgets also decorate appropriate HTML tags in case of error, the ``errors``
dictionary must be available in the ``Mako`` context::

    template = template_lookup.get_template(template_name)
    assert 'errors' in kwargs
    template.render(
                **kwargs
    )

See :py:mod:`wheezy.html.ext.mako` for more examples.

Tenjin
^^^^^^

:ref:`wheezy.html` integration with ``Tenjin`` is provided via the preprocessor
feature. Here is how to add
:py:meth:`~wheezy.html.ext.tenjin.widget_preprocessor` to your code::

    from wheezy.html.ext.tenjin import widget_preprocessor

    engine = tenjin.Engine(
            ...
            pp=[widget_preprocessor])

The only thing :py:meth:`~wheezy.html.ext.mako.widget_preprocessor` does is
translation of widget code to adequate ``Tenjin`` code.

Let's demonstrate this with an example::

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

    <input id="remember-me" name="remember_me" type="checkbox" value="1" class="i" />

Since widgets also decorate appropriate HTML tags in case of error, the ``errors``
dictionary must be available in the ``Tenjin`` context::

    assert 'errors' in kwargs
    engine.render('page.html',
                **kwargs
    )

See :py:mod:`wheezy.html.ext.tenjin` for more examples.

Wheezy Template
^^^^^^^^^^^^^^^

:ref:`wheezy.html` integration with ``wheezy.template`` is provided via the preprocessor
feature. Here is how to add
:py:meth:`~wheezy.html.ext.template.WidgetExtension` to your code::

    from wheezy.html.ext.template import WidgetExtension
    from wheezy.html.utils import html_escape
    from wheezy.html.utils import format_value

    engine = Engine(
            ...
            extensions=[
                WidgetExtension
    ])
    engine.global_vars.update({
        'format_value': format_value,
        'h': html_escape
    })

The only thing
:py:meth:`~wheezy.html.ext.template.WidgetExtension` does is
translation of widget code to adequate ``wheezy.template`` code.

Let's demonstrate this with an example::

    @model.remember_me.checkbox(class_='i')

is translated to the following ``wheezy.template`` code (during template compilation
phase)::

    <input id="remember-me" name="remember_me" type="checkbox" value="1"
    @if 'remember_me' in errors:
     class="error i"
    @else:
     class="i"
    @if model.remember_me:
     checked="checked"
    @end
     />

which effectively renders the HTML at runtime::

    <input id="remember-me" name="remember_me" type="checkbox" value="1" class="i" />

Since widgets also decorate appropriate HTML tags in case of error, ``errors``
dictionary must be available in ``wheezy.template`` context::

    assert 'errors' in kwargs
    engine.render('page.html',
                **kwargs
    )

See :py:mod:`wheezy.html.ext.template` for more examples.
