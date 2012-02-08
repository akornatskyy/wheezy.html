
""" ``widgets`` module.
"""

from wheezy.html.comp import iteritems
from wheezy.html.markup import Fragment
from wheezy.html.markup import Tag
from wheezy.html.utils import html_escape


id = lambda name: name.replace('_', '-')


def hidden(name, value, attrs=None):
    """
        >>> hidden('pref', 'abc')
        <input type="hidden" name="pref" value="abc" />
    """
    return Tag('input', attrs={
            'name': name,
            'type': 'hidden',
            'value': value
    })


def textbox(name, value, attrs=None):
    """
        >>> textbox('zip_code', '79053')
        <input type="text" id="zip-code" value="79053" name="zip_code" />
    """
    return Tag('input', attrs={
            'id': id(name),
            'name': name,
            'type': 'text',
            'value': value
    })


def password(name, value, attrs=None):
    """
        >>> password('passwd', '')
        <input type="password" id="passwd" value="" name="passwd" />
    """
    return Tag('input', attrs={
            'id': id(name),
            'name': name,
            'type': 'password',
            'value': value
    })


def textarea(name, value, attrs=None):
    """
        >>> textarea('message_text', 'x')  #doctest: +NORMALIZE_WHITESPACE
        <textarea rows="9" cols="40" id="message-text"
            name="message_text">x</textarea>

        ``value`` is empty.

        >>> textarea('message_text', '')  #doctest: +NORMALIZE_WHITESPACE
        <textarea rows="9" cols="40" id="message-text"
            name="message_text"></textarea>
    """
    return Tag('textarea', value, attrs={
            'id': id(name),
            'name': name,
            'rows': '9',
            'cols': '40'
    })


def checkbox(name, checked, attrs=None):
    """
        >>> checkbox('accept', 'True')  #doctest: +NORMALIZE_WHITESPACE
        <input type="hidden" name="accept" /><input checked="checked"
            type="checkbox" id="accept" value="1" name="accept" />
        >>> checkbox('accept', 'False')  #doctest: +NORMALIZE_WHITESPACE
        <input type="hidden" name="accept" /><input type="checkbox"
            id="accept" value="1" name="accept" />

        >>> checkbox('accept', 'True',
        ...         attrs={'class_': 'b'})  #doctest: +NORMALIZE_WHITESPACE
        <input type="hidden" name="accept" /><input class="b"
            checked="checked" name="accept" type="checkbox"
            id="accept" value="1" />
     """
    tag_attrs = {
            'id': id(name),
            'name': name,
            'type': 'checkbox',
            'value': '1'
    }
    if checked == 'True':
        tag_attrs['checked'] = 'checked'
    if attrs:
        tag_attrs.update(attrs)
    return Fragment((
            Tag('input', attrs={'name': name, 'type': 'hidden'}),
            Tag('input', attrs=tag_attrs)
    ))


def label(name, value, attrs=None):
    """
        >>> label('zip_code', 'Zip Code')
        <label for="zip-code">Zip Code</label>
        >>> label('zip_code', 'Zip Code', attrs={'class_': 'inline'})
        <label class="inline" for="zip-code">Zip Code</label>
    """
    tag_attrs = {
            'for': id(name)
    }
    if attrs:
        tag_attrs.update(attrs)
    return Tag('label', inner=value, attrs=tag_attrs)


def dropdown(name, value, attrs):
    """
        >>> from operator import itemgetter
        >>> colors = sorted({'1': 'Yellow', '2': 'Red'}.items(),
        ...         key=itemgetter(1))
        >>> colors
        [('2', 'Red'), ('1', 'Yellow')]
        >>> dropdown('favorite_color', '1', attrs={
        ...     'choices': colors})  #doctest: +NORMALIZE_WHITESPACE
        <select id="favorite-color" name="favorite_color"><option
            value="2">Red</option><option selected="selected"
            value="1">Yellow</option></select>
    """
    choices = attrs.pop('choices')
    options = []
    for key, text in choices:
        if key == value:
            tag_attrs = {
                    'value': key,
                    'selected': 'selected'
            }
        else:
            tag_attrs = {
                    'value': key
            }
        options.append(Tag('option', inner=text, attrs=tag_attrs))
    options = Fragment(options)
    tag_attrs = {
            'id': id(name),
            'name': name
    }
    return Tag('select', inner=options, attrs=tag_attrs)


def radio(name, value, attrs=None):
    """
        >>> from operator import itemgetter
        >>> scm = sorted({'git': 'Git', 'hg': 'Mercurial'}.items(),
        ...         key=itemgetter(1))

        >>> scm
        [('git', 'Git'), ('hg', 'Mercurial')]

        >>> radio('scm', 'hg',
        ...         attrs={'choices': scm})  #doctest: +NORMALIZE_WHITESPACE
        <label><input type="radio" name="scm" value="git"
        />Git</label><label><input checked="checked" type="radio" name="scm"
        value="hg" />Mercurial</label>
    """
    choices = attrs.pop('choices')
    elements = []
    append = elements.append
    for key, text in choices:
        i = id(name) + '-' + key
        tag_attrs={
                'name': name,
                'type': 'radio',
                'value': key
        }
        if key == value:
            tag_attrs['checked'] = 'checked'
        append(Tag('label',
            Fragment((Tag('input', attrs=tag_attrs), text))))
    return Fragment(elements)

default = {
        'hidden': hidden,
        'textbox': textbox,
        'password': password,
        'textarea': textarea,
        'checkbox': checkbox,
        'label': label,
        'dropdown': dropdown,
        'select': dropdown,
        'radio': radio
}
