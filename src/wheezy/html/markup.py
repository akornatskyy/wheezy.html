
""" ``markup`` module.
    http://www.w3schools.com/tags/
"""

from wheezy.html.comp import iteritems
from wheezy.html.comp import str_type


class Tag(object):
    """ Represents object version of HTML tag.
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

    def __unicode__(self):  # pragma: nocover, python 3
        """
            >>> assert str_type(Tag('x')) == str_type('<x />')
        """
        return self.render(str_type)

    def __str__(self):
        """
            >>> assert str(Tag('x')) == '<x />'
        """
        return self.render(str)

    def __repr__(self):
        return self.render(str)

    def render(self, converter):
        """
            Normal tag with attributes

            >>> Tag('span')("abc", class_='error')
            <span class="error">abc</span>

            Alternatively you can use ``attr``:

            >>> Tag('span')("abc", attrs={'class': 'error'})
            <span class="error">abc</span>

            Self closing tag

            >>> Tag('input')(id='name', value='abc')
            <input id="name" value="abc" />
        """
        name = self.name
        attrs = self.attrs
        if attrs:
            t = '<' + name + ' ' + ' '.join(
                    [k.rstrip('_') + '="' + attrs[k] + '"'
                        for k in attrs])
        else:
            t = '<' + name
        inner = self.inner
        if inner is not None:
            return t + '>' + converter(inner) + '</' + name + '>'
        else:
            return t + ' />'
        # 0.442
        #parts = []
        #append = parts.append
        #append('<' + self.name)
        #attrs = self.attrs
        #if attrs:
        #    parts.extend([' ' + name.rstrip('_') + '="' + attrs[name] + '"'
        #        for name in attrs])
        #    #for name, value in iteritems(self.attrs):
        #    #    append(' ' + name.rstrip('_') +
        #    #            '="' + value + '"')
        #if self.inner is not None:
        #    append('>' + converter(self.inner) +
        #            '</' + self.name + '>')
        #else:
        #    append(' />')
        #return ''.join(parts)


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
