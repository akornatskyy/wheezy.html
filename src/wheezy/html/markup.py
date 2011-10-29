
""" ``markup`` module.
    http://www.w3schools.com/tags/
"""

from wheezy.html.comp import iteritems


class Tag(object):
    """
    """
    __slots__ = ['name', 'inner', 'attrs']

    def __init__(self, name, inner=None, attrs=None):
        self.name = name
        self.inner = inner
        self.attrs = attrs or {}

    def __call__(self, inner=None, attrs=None, **kwargs):
        """
            ``attrs`` overwrite ``kwargs``.

            >>> t = Tag('x')
            >>> t(attrs={'a': '1', 'b': '2'}, b='3', d='4')
            <x a="1" b="2" d="4" />
        """
        self.inner = inner
        self.attrs = dict(self.attrs, **kwargs)
        if attrs:
            self.attrs.update(attrs)
        return self

    def append_attr(self, name, value):
        """
            If there is no attribute with ``name`` than it added.

            >>> t = Tag('x')
            >>> t.append_attr('class', 'a')
            >>> t
            <x class="a" />

            Existing attribute is extended with space and value.

            >>> t.append_attr('class', 'b')
            >>> t
            <x class="b a" />
        """
        attrs = self.attrs
        if name in attrs:
            attrs[name] = value + ' ' + attrs[name]
        else:
            attrs[name] = value

    def __repr__(self):
        """
            Normal tag with attributes

            >>> print(Tag('span')("abc", class_='error'))
            <span class="error">abc</span>

            Alternatively you can use ``attr``:

            >>> print(Tag('span')("abc", attrs={'class': 'error'}))
            <span class="error">abc</span>

            Self closing tag

            >>> print(Tag('input')(id='name', value='abc'))
            <input id="name" value="abc" />
        """
        parts = []
        append = parts.append
        append('<' + self.name)
        if self.attrs:
            for name, value in iteritems(self.attrs):
                append(' ' + name.rstrip('_') +
                        '="' + str(value) + '"')
        if self.inner is not None:
            append('>' + str(self.inner) + '</' + self.name + '>')
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

    def __getattr__(self, name):
        return getattr(self.tags[0], name)
