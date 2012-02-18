
""" ``builder`` module.
"""

from datetime import date
from datetime import datetime

from wheezy.html.comp import str_type
from wheezy.html.markup import Tag
from wheezy.html.widgets import default
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
        if self.errors:
            if 'class_' in attrs:
                attrs['class_'] = CSS_CLASS_ERROR + ' ' + attrs['class_']
            else:
                attrs['class'] = CSS_CLASS_ERROR
        return self.tag(self.name, value, attrs)


class WidgetBuilder(object):
    """
        ``errors`` - a list of errors.

        textbox

        >>> errors = []
        >>> h = WidgetBuilder('age', '33', errors)
        >>> h.textbox(class_='b')
        <input class="b" type="text" id="age" value="33" name="age" />
        >>> h.error()
        ''
        >>> errors.append('required')
        >>> h = WidgetBuilder('age', '0', errors)
        >>> h.textbox()
        <input class="error" type="text" id="age" value="0" name="age" />
        >>> h.textbox(class_='b')
        <input class="error b" type="text" id="age" value="0" name="age" />
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

            ``format_provider`` - a callable of the following form::

                def my_formatter(value, format_string):
                    return value_formatted

            >>> h = WidgetBuilder('date_of_birth', date(2012, 2, 6), None)
            >>> h.format('%m-%d-%y').formatted
            '02-06-12'
            >>> h = WidgetBuilder('date_of_birth', date(2012, 2, 6), None)
            >>> h.format(format_provider=lambda value, ignore:
            ...         value.strftime('%m-%d-%y')).formatted
            '02-06-12'
            >>> h = WidgetBuilder('pref', [1, 2, 7], None)
            >>> list(map(str, h.format().formatted))
            ['1', '2', '7']
            >>> h = WidgetBuilder('pref', [], None)
            >>> h.format().formatted
            ()
        """
        value = self.value
        # TODO: probably there is better check since attribute check for
        # __iter__ is not valid in python 3.2, str support it.
        if isinstance(value, (list, tuple)):
            try:
                if format_provider is None:
                    formatter_name = type(value[0]).__name__
                    format_provider = format_providers[formatter_name]
                self.formatted = tuple(format_provider(item, format_string)
                        for item in value)
            except IndexError:
                self.formatted = tuple([])
        else:
            if format_provider is None:
                formatter_name = type(value).__name__
                format_provider = format_providers[formatter_name]
            self.formatted = format_provider(self.value, format_string)
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
        if self.errors:
            return Tag('span', self.errors[-1], {
                'class': CSS_CLASS_ERROR
            })
        else:
            return ''


str_format_provider = lambda value, format_string: str_type(value)


def date_format_provider(value, format_string=None):
    """ Default format provider for ``datetime.date``.

        >>> date_format_provider(date.min)
        ''
        >>> date_format_provider(date(2012, 2, 6))
        '2012/02/06'
    """
    if date.min == value:
        return ''
    return value.strftime(str(format_string or '%Y/%m/%d'))


def datetime_format_provider(value, format_string=None):
    """ Default format provider for ``datetime.datetime``.

        >>> datetime_format_provider(datetime.min)
        ''
        >>> datetime_format_provider(datetime(2012, 2, 6, 15, 17))
        '2012/02/06 15:17'
    """
    if datetime.min == value:
        return ''
    return value.strftime(str(format_string or '%Y/%m/%d %H:%M'))


format_providers = {
        'str': lambda value, format_string: html_escape(str_type(value)),
        'unicode': lambda value, format_string: html_escape(value),
        'int': str_format_provider,
        'Decimal': str_format_provider,
        'bool': str_format_provider,
        'float': str_format_provider,
        'date': date_format_provider,
        'time': lambda value, format_string: value.strftime(
            str(format_string or '%H:%M')),
        'datetime': datetime_format_provider
}
