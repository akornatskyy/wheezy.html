
""" ``markup`` module.
    http://www.w3schools.com/tags/
"""

from wheezy.html.comp import PY3
from wheezy.html.comp import str_type


class Tag(object):
    """ Represents object version of HTML tag.
    """
    __slots__ = ['name', 'inner', 'attrs']

    def __init__(self, name, inner, attrs):
        self.name = name
        self.inner = inner
        self.attrs = attrs

    def __repr__(self):
        return str(self.render())

    def render(self):
        """
            Normal tag with attributes

            >>> Tag('span', 'abc', {'class': 'error'})
            <span class="error">abc</span>

            Self closing tag

            >>> Tag('input', None, {'id': 'name', 'value': 'abc'})
            <input id="name" value="abc" />
        """
        name = self.name
        attrs = self.attrs
        t = '<' + name + ' ' + ' '.join(
            [k.rstrip('_') + '="' + attrs[k] + '"'
                for k in sorted(attrs.keys())])
        inner = self.inner
        if inner is None:
            return t + ' />'
        else:
            return t + '>' + str_type(inner) + '</' + name + '>'

    if PY3:  # pragma: nocover
        __str__ = render
    else:  # pragma: nocover
        __unicode__ = render


class Fragment(object):
    """ Represents object version of composite HTML tag.
    """

    __slots__ = ['tags']

    def __init__(self, tags):
        self.tags = tags

    def __unicode__(self):  # pragma: nocover, python 3
        """
            >>> assert str_type(Fragment((1, 2))) == str_type('12')
        """
        return ''.join(map(str_type, self.tags))

    def __str__(self):
        """
            >>> print(Fragment((1, 2)))
            12
        """
        return ''.join(map(str, self.tags))

    def __repr__(self):
        """
            >>> Fragment((1, 2))
            12
        """
        return ''.join(map(repr, self.tags))
