
""" ``builder`` module.
"""

from wheezy.html.markup import Tag
from wheezy.html.widgets import default
from wheezy.html.widgets import hidden


CSS_CLASS_ERROR = 'error'


class Widget(object):
    """
    """

    __slots__ = ['tag', 'name', 'value', 'errors']

    def __init__(self, tag, name, value, errors):
        self.tag = default[tag]
        self.name = name
        self.value = value
        self.errors = errors

    def __call__(self, value=None, **attrs):
        """
            >>> w = Widget('label', 'zip_code', '79053', None)
        """
        if value is None:
            value = self.value
        tag = self.tag(self.name, value, attrs)
        if attrs and hasattr(tag, 'attrs'):
            tag.attrs.update(attrs)
        if self.errors:
            tag.append_attr('class_', CSS_CLASS_ERROR)
        return tag


class WidgetBuilder(object):
    """
        ``errors`` - a list of errors.

        >>> class User(object): pass
        >>> model = User()

        textbox

        >>> model.age = 33
        >>> errors = []
        >>> h = WidgetBuilder('age', 33, errors)
        >>> h.textbox(class_='b')
        <input class="b" type="text" id="age" value="33" name="age" />
        >>> h.error()
        ''
        >>> errors.append('required')
        >>> h = WidgetBuilder('age', 0, errors)
        >>> h.textbox(class_='b')
        <input class="error b" type="text" id="age" value="0" name="age" />
        >>> h.error()
        <span class="error">required</span>
    """

    __slots__ = ['name', 'value', 'errors']

    def __init__(self, name, value, errors):
        self.name = name
        self.value = value
        self.errors = errors

    def __repr__(self):
        """
            >>> class A(object):pass
            >>> model = A()
            >>> model.x = 100
            >>> errors = []
            >>> h = WidgetBuilder('x', 100, errors)
            >>> h
            100
        """
        return str(self.value)

    def __getattr__(self, tag_name):
        return Widget(tag_name, self.name, self.value,
                self.errors)

    def error(self):
        if self.errors:
            return Tag('span', self.errors[0], {
                'class_': CSS_CLASS_ERROR
            })
        else:
            return ''
