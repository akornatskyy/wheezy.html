
""" ``builder`` module.
"""

from wheezy.html.markup import Tag
from wheezy.html.widgets import default
from wheezy.html.utils import format_value
from wheezy.html.utils import html_escape


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
            >>> w = Widget('label', 'zip_code', 'Zip Code', None)
            >>> w()
            <label for="zip-code">Zip Code</label>
            >>> w = Widget('label', 'zip_code', None, None)
            >>> w('Zip Code')
            <label for="zip-code">Zip Code</label>
        """
        if value is None:
            value = self.value
        else:
            value = html_escape(value)
        if self.errors is not None:
            if 'class_' in attrs:
                attrs['class_'] = CSS_CLASS_ERROR + ' ' + attrs['class_']
            else:
                attrs['class'] = CSS_CLASS_ERROR
        return self.tag(self.name, value, attrs)


class WidgetBuilder(object):
    """
        ``errors`` - a list of errors.

        textbox

        >>> errors = None
        >>> h = WidgetBuilder('age', '33', errors)
        >>> h.textbox(class_='b')
        <input class="b" id="age" name="age" type="text" value="33" />
        >>> h.error()
        ''
        >>> errors = ['required']
        >>> h = WidgetBuilder('age', '0', errors)
        >>> h.textbox()
        <input class="error" id="age" name="age" type="text" value="0" />
        >>> h.textbox(class_='b')
        <input class="error b" id="age" name="age" type="text" value="0" />
        >>> h.error()
        <span class="error">required</span>
    """

    __slots__ = ['name', 'value', 'errors', 'formatted']

    def __init__(self, name, value, errors):
        self.name = name
        self.value = value
        self.errors = errors
        self.formatted = None

    def format(self, format_string=None, format_provider=None):
        """ Formats widget value.
        """
        value = self.value
        self.formatted = format_value(value, format_string, format_provider)
        return self

    def __repr__(self):
        """
            >>> h = WidgetBuilder('age', '0', None)
            >>> h
            0
        """
        return self.format().formatted

    def __getattr__(self, tag_name):
        if self.formatted is None:
            self.format()
        return Widget(tag_name, self.name, self.formatted,
                      self.errors)

    def error(self):
        if self.errors is None:
            return ''
        return Tag('span', self.errors[-1], {
            'class': CSS_CLASS_ERROR
        })
