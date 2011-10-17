
""" ``factory`` module.
"""

from wheezy.html.builder import WidgetBuilder
from wheezy.html.markup import Fragment
from wheezy.html.markup import Tag


class TagFactory(object):
    """
        >>> t = TagFactory()

        Build span tag

        >>> print(t.span("abc", class_='error'))
        <span class="error">abc</span>

        ``tag`` is shortcut for ``TagFactory`` class instance.

        >>> assert isinstance(tag, TagFactory)
    """

    def __init__(self):  # TODO: encoding
        pass

    def __call__(self, *tags):
        return Fragment(*tags)

    def __getattr__(self, name):
        return Tag(name)


class WidgetFactory(object):
    """
        >>> class User(object): pass
        >>> model = User()
        >>> model.name = 'abc'
        >>> w = WidgetFactory(model)
        >>> w.name
        abc
        >>> w.name.textbox()
        <input type="text" id="name" value="abc" name="name" />
    """

    def __init__(self, model):
        self.model = model

    def __getattr__(self, name):
        return WidgetBuilder(self.model, name)


tag = TagFactory()
widget = WidgetFactory
