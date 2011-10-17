
""" ``markup`` module.
    http://www.w3schools.com/tags/
"""

from wheezy.html.comp import iteritems


class Tag(object):
    """
    """
    __slots__ = ['name', 'inner', 'attr']

    def __init__(self, name, inner=None, attr=None, **kwargs):
        self.name = name
        self(inner, attr, **kwargs)

    def __call__(self, inner=None, attr=None, **kwargs):
        self.inner = repr(inner)
        if attr:
            if kwargs:
                attr.update(kwargs)
            self.attr = attr
        else:
            self.attr = kwargs
        return self

    def __repr__(self):
        """
            Normal tag with attributes

            >>> print(Tag('span')("abc", class_='error'))
            <span class="error">abc</span>

            Self closing tag

            >>> t = Tag('input')
            >>> print(Tag('input')(id='name', value='abc'))
            <input id="name" value="abc" />
        """
        parts = []
        append = parts.append
        append('<' + self.name)
        if self.attr:
            for name, value in iteritems(self.attr):
                append(' ' + name.rstrip('_') +
                        '="' + value + '"')
        if self.inner:
            append('>' + self.inner + '</' + self.name + '>')
        else:
            append(' />')
        return ''.join(parts)


class Fragment(object):
    """
    """

    __slots__ = ['tags']

    def __init__(self, *tags):
        self.tags = tags

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return ''.join(map(repr, self.tags))
