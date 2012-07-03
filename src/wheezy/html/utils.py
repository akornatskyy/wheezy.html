
""" ``utils`` module.
"""

from datetime import date
from datetime import datetime

from wheezy.html.comp import str_type


try:
    from wheezy.html.boost import escape_html
    html_escape = escape_html
except ImportError:
    def escape_html(s):
        """ Escapes a string so it is valid within HTML.

            >>> html_escape('abc')
            'abc'
            >>> escape_html('&<>"\\'')
            "&amp;&lt;&gt;&quot;\'"
        """
        return s.replace('&', '&amp;').replace('<', '&lt;').replace(
            '>', '&gt;').replace('"', '&quot;')
    html_escape = escape_html


html_id = lambda name: name.replace('_', '-')


def format_value(value, format_spec=None, format_provider=None):
    """ Formats widget value.

        ``format_provider`` - a callable of the following form::

            def my_formatter(value, format_spec):
                return value_formatted

        >>> str(format_value(date(2012, 2, 6), '%m-%d-%y'))
        '02-06-12'
        >>> format_value(date(2012, 2, 6),
        ...         format_provider=lambda value, ignore:
        ...         value.strftime('%m-%d-%y'))
        '02-06-12'
        >>> list(map(str, format_value([1, 2, 7])))
        ['1', '2', '7']
        >>> format_value([])
        ()

        If format provider is unknown apply str_type.

        >>> str(format_value({}))
        '{}'
    """
    # TODO: probably there is better check since attribute check for
    # __iter__ is not valid in python 3.2, str support it.
    if isinstance(value, (list, tuple)):
        try:
            if format_provider is None:
                formatter_name = type(value[0]).__name__
                format_provider = format_providers[formatter_name]
            return tuple(format_provider(item, format_spec)
                         for item in value)
        except IndexError:
            return tuple([])
    else:
        if format_provider is None:
            formatter_name = type(value).__name__
            if formatter_name in format_providers:
                format_provider = format_providers[formatter_name]
            else:
                return str_type(value)
        return format_provider(value, format_spec)


str_format_provider = lambda value, format_spec: str_type(value)


def date_format_provider(value, format_spec=None):
    """ Default format provider for ``datetime.date``.

        >>> date_format_provider(date.min)
        ''
        >>> date_format_provider(date(2012, 2, 6))
        '2012/02/06'
    """
    if date.min == value:
        return ''
    # Python 2.4, 2.5
    # TypeError: strftime() argument 1 must be str, not unicode
    return value.strftime(str(format_spec or '%Y/%m/%d'))


def datetime_format_provider(value, format_spec=None):
    """ Default format provider for ``datetime.datetime``.

        >>> datetime_format_provider(datetime.min)
        ''
        >>> datetime_format_provider(datetime(2012, 2, 6, 15, 17))
        '2012/02/06 15:17'
    """
    if datetime.min == value:
        return ''
    # Python 2.4, 2.5
    # TypeError: strftime() argument 1 must be str, not unicode
    return value.strftime(str(format_spec or '%Y/%m/%d %H:%M'))


format_providers = {
    'str': lambda value, format_spec: html_escape(str_type(value)),
    'unicode': lambda value, format_spec: html_escape(value),
    'int': str_format_provider,
    'Decimal': str_format_provider,
    'bool': str_format_provider,
    'float': str_format_provider,
    'date': date_format_provider,
    'time': lambda value, format_spec: value.strftime(
        str(format_spec or '%H:%M')),
    'datetime': datetime_format_provider,
    'NoneType': lambda value, format_spec: ''
}
