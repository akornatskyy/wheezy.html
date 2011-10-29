
""" ``factory`` module.
"""

from wheezy.html.builder import WidgetBuilder
from wheezy.html.markup import Fragment
from wheezy.html.markup import Tag


class TagFactory(object):
    """ Factory of xhtml tags.

        ``tag`` is a shortcut for ``TagFactory`` class instance.

        >>> assert isinstance(tag, TagFactory)
    """

    def __call__(self, *tags):
        """ Call function let combine several tags into fragment.

            >>> tag(tag.b('1'), tag.i('2'))
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

        >>> user.name.textbox(maxlength=30)  #doctest: +NORMALIZE_WHITESPACE
        <input maxlength="30" type="text" id="name"
            value="John" name="name" />

        >>> user.name.textarea(rows=10)  #doctest: +NORMALIZE_WHITESPACE
        <textarea rows="10" cols="40" id="name"
            name="name">John</textarea>

        >>> user.accept.checkbox()  #doctest: +NORMALIZE_WHITESPACE
        <input type="checkbox" id="accept" value="1"
            name="accept" /><input type="hidden" name="accept" />

        >>> user.model.accept = True
        >>> user.accept.checkbox()  #doctest: +NORMALIZE_WHITESPACE
        <input checked="checked" type="checkbox" id="accept"
            value="1" name="accept" /><input type="hidden"
            name="accept" />

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
        ...         'id': ['error 1'],
        ...         'name': ['error 2'],
        ...         'accept': ['error 3'],
        ...         'favorite_color': ['error 4']
        ... }
        >>> user = widget(model, errors)

        Render error message

        >>> user.id.error()
        <span class="error">error 1</span>

        HTML tags got class ``error``.

        >>> user.id.hidden()
        <input class="error" type="hidden" name="id" value="12345" />
        >>> user.name.textbox(class_='x')  #doctest: +NORMALIZE_WHITESPACE
        <input class="error x" type="text" id="name" value="John"
            name="name" />
        >>> user.name.textarea()  #doctest: +NORMALIZE_WHITESPACE
        <textarea class="error" rows="9" cols="40" id="name"
            name="name">John</textarea>
        >>> user.accept.checkbox()  #doctest: +NORMALIZE_WHITESPACE
        <input checked="checked" name="accept" value="1"
            class="error" type="checkbox" id="accept" /><input
            type="hidden" name="accept" />
        >>> user.favorite_color.label('Color:')
        <label class="error" for="favorite-color">Color:</label>
    """

    def __init__(self, model, errors):
        self.model = model
        self.errors = errors

    def __getattr__(self, name):
        value = getattr(self.model, name)
        return WidgetBuilder(name, value, self.errors.get(name, None))


tag = TagFactory()
widget = WidgetFactory
