
""" ``factory`` module.
"""

from wheezy.html.builder import WidgetBuilder
from wheezy.html.comp import str_type
from wheezy.html.markup import Fragment
from wheezy.html.markup import Tag
from wheezy.html.utils import html_escape


CSS_CLASS_ERROR_MESSAGE = 'error-message'
CSS_CLASS_WARNING_MESSAGE = 'warning-message'
CSS_CLASS_INFO_MESSAGE = 'info-message'


class TagFactory(object):
    """ Factory of xhtml tags.

        ``tag`` is a shortcut for ``TagFactory`` class instance.

        >>> assert isinstance(tag, TagFactory)
    """

    def __call__(self, *tags):
        """ Call function let combine several tags into fragment.

            >>> tag((tag.b('1'), tag.i('2')))
            <b>1</b><i>2</i>
        """
        return Fragment(*tags)

    def __getattr__(self, name):
        """ Attribute name is promoted to tag.

            >>> tag.span('text', class_='b')
            <span class="b">text</span>
        """
        return Tag(name)


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
        <input type="hidden" name="id" value="12345" />

        >>> user.name.textbox(maxlength='30')  #doctest: +NORMALIZE_WHITESPACE
        <input maxlength="30" type="text" id="name"
            value="John" name="name" />

        >>> user.name.textarea(rows='10')  #doctest: +NORMALIZE_WHITESPACE
        <textarea rows="10" cols="40" id="name"
            name="name">John</textarea>

        >>> user.accept.checkbox()  #doctest: +NORMALIZE_WHITESPACE
        <input type="hidden" name="accept" /><input type="checkbox"
            id="accept" value="1" name="accept" />

        >>> user = widget(model, errors)  # widget builders are cached
        >>> user.model.accept = True
        >>> user.accept.checkbox()  #doctest: +NORMALIZE_WHITESPACE
        <input type="hidden" name="accept" /><input checked="checked"
            type="checkbox" id="accept" value="1" name="accept" />

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
        <input class="error x" type="text" id="name" value="John"
            name="name" />
        >>> user.name.textarea()  #doctest: +NORMALIZE_WHITESPACE
        <textarea class="error" rows="9" cols="40" id="name"
            name="name">John</textarea>
        >>> user.accept.checkbox()  #doctest: +NORMALIZE_WHITESPACE
        <input type="hidden" name="accept" /><input checked="checked"
            name="accept" type="checkbox" id="accept" value="1"
            class="error" />
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
        try:
            return self.builders[name]
        except KeyError:
            value = getattr(self.model, name)
            builder = WidgetBuilder(name, value, self.errors.get(name, None))
            self.builders[name] = builder
            return builder

    def error(self, text=None):
        if text is None:
            errors = self.errors.get('__ERROR__', None)
            if errors:
                text = errors[-1]
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


tag = TagFactory()
widget = WidgetFactory
