
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

:ref:`wheezy.html` comes with a number of built-in widgets:

* :py:meth:`~wheezy.html.widgets.hidden` - html element input of type hidden.
* :py:meth:`~wheezy.html.widgets.textbox` - html element input of type text.
* :py:meth:`~wheezy.html.widgets.password` - html element input of type
  password.
* :py:meth:`~wheezy.html.widgets.textarea` - html element textarea html
  element.
* :py:meth:`~wheezy.html.widgets.checkbox` - two html elements: input type
  hidden and input type checkbox.
* :py:meth:`~wheezy.html.widgets.label` - html element label.
* :py:meth:`~wheezy.html.widgets.dropdown` - html element select. Attribute
  ``choices`` is a list of html options.

Custom Widgets
~~~~~~~~~~~~~~

It is easy to provide own widgets. A widget is any callable of the following
contract::

    from wheezy.html.markup import Tag
    
    def my_widget(name, value, attrs=None):
        tag = Tag()
        return tag
    
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

