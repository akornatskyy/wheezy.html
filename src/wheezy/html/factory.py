
""" ``factory`` module.
"""

from wheezy.html.builder import WidgetBuilder
from wheezy.html.markup import Tag
from wheezy.html.utils import html_escape


CSS_CLASS_ERROR_MESSAGE = 'error-message'
CSS_CLASS_WARNING_MESSAGE = 'warning-message'
CSS_CLASS_INFO_MESSAGE = 'info-message'


class WidgetFactory(object):
    """
        ``errors`` is a defaultdict(list)

        ``widget`` is a shortcut for WidgetFactory class.

        >>> assert widget is WidgetFactory

        Here is a simple user model.

        >>> class User(object): pass
        >>> model = User()
        >>> model.id = 12345
        >>> model.name = 'John'
        >>> model.accept = False
        >>> model.favorite_color = 'yellow'

        No errors

        >>> errors = {}
        >>> user = widget(model, errors)

        Access model attributes

        >>> user.id
        12345
        >>> user.name
        John

        HTML tags

        >>> user.id.hidden()
        <input name="id" type="hidden" value="12345" />

        >>> user.name.textbox(maxlength='30')  #doctest: +NORMALIZE_WHITESPACE
        <input id="name" maxlength="30" name="name" type="text"
            value="John" />

        >>> user.name.textarea(rows='10')  #doctest: +NORMALIZE_WHITESPACE
        <textarea cols="40" id="name" name="name"
            rows="10">John</textarea>

        >>> user.accept.checkbox()  #doctest: +NORMALIZE_WHITESPACE
        <input id="accept" name="accept" type="checkbox" value="1" />

        >>> user = widget(model, errors)  # widget builders are cached
        >>> user.model.accept = True
        >>> user.accept.checkbox()  #doctest: +NORMALIZE_WHITESPACE
        <input checked="checked" id="accept" name="accept" type="checkbox"
            value="1" />

        >>> user.favorite_color.label('Color:')
        <label for="favorite-color">Color:</label>

        >>> colors = (('red', 'Red'), ('yellow', 'Yellow'),
        ...           ('black', 'Black'))
        >>> user.favorite_color.dropdown(
        ...         choices=colors)  #doctest: +NORMALIZE_WHITESPACE
        <select id="favorite-color" name="favorite_color"><option
            value="red">Red</option><option selected="selected"
            value="yellow">Yellow</option><option
            value="black">Black</option></select>

        Errors

        >>> errors = {
        ...         'name': ['error 2'],
        ...         'accept': ['error 3'],
        ...         'favorite_color': ['error 4']
        ... }
        >>> user = widget(model, errors)

        Render error message

        >>> user.favorite_color.error()
        <span class="error">error 4</span>

        HTML tags got class ``error``.

        >>> user.name.textbox(class_='x')  #doctest: +NORMALIZE_WHITESPACE
        <input class="error x" id="name" name="name" type="text"
            value="John" />
        >>> user.name.textarea()  #doctest: +NORMALIZE_WHITESPACE
        <textarea class="error" cols="40" id="name" name="name"
            rows="9">John</textarea>
        >>> user.accept.checkbox()  #doctest: +NORMALIZE_WHITESPACE
        <input checked="checked" class="error" id="accept" name="accept"
            type="checkbox" value="1" />
        >>> user.favorite_color.label('Color:')
        <label class="error" for="favorite-color">Color:</label>

        General messages: info, warning, error

        >>> user.info(None)
        ''
        >>> user.info('Your changes have been saved.')
        <span class="info-message">Your changes have been saved.</span>

        >>> user.warning('')
        ''
        >>> user.warning('No matching records were found.')
        <span class="warning-message">No matching records were found.</span>

        >>> user.error('The username or password '
        ...     'provided is incorrect.')  #doctest: +NORMALIZE_WHITESPACE
        <span class="error-message">The username or password provided
        is incorrect.</span>

        Error message is taken from context

        >>> user.error()
        ''
        >>> errors['__ERROR__'] = ['The username or password '
        ...     'provided is incorrect.']
        >>> user.error()  #doctest: +NORMALIZE_WHITESPACE
        <span class="error-message">The username or password provided
        is incorrect.</span>

    """

    __slots__ = ['model', 'errors', 'builders']

    def __init__(self, model, errors):
        self.model = model
        self.errors = errors
        self.builders = {}

    def __getattr__(self, name):
        builders = self.builders
        if name in builders:
            return builders[name]
        else:
            value = getattr(self.model, name)
            errors = self.errors
            if name in errors:
                builder = WidgetBuilder(name, value, errors[name])
            else:
                builder = WidgetBuilder(name, value, None)
            builders[name] = builder
            return builder

    def error(self, text=None):
        if text is None:
            errors = self.errors
            if '__ERROR__' in errors:
                errors = self.errors['__ERROR__']
                text = errors[-1]
            else:
                return ''
        return self.info(text, class_=CSS_CLASS_ERROR_MESSAGE)

    def warning(self, text):
        return self.info(text, class_=CSS_CLASS_WARNING_MESSAGE)

    def info(self, text, class_=CSS_CLASS_INFO_MESSAGE):
        if text:
            return Tag('span', html_escape(text), {
                'class': class_
            })
        else:
            return ''


widget = WidgetFactory
