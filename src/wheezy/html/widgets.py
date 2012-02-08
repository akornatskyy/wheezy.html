
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
        >>> textbox('zip_code', '79053',
        ...         attrs={'class': 'error'})  #doctest: +NORMALIZE_WHITESPACE
        <input class="error" type="text" id="zip-code" value="79053"
            name="zip_code" />
    """
    tag_attrs = {
            'id': id(name),
            'name': name,
            'type': 'text',
            'value': value
    }
    if attrs:
        tag_attrs.update(attrs)
    return Tag('input', attrs=tag_attrs)


def password(name, value, attrs=None):
    """
        >>> password('passwd', '',
        ...         attrs={'class': 'error'})  #doctest: +NORMALIZE_WHITESPACE
        <input class="error" type="password" id="passwd" value=""
            name="passwd" />
    """
    tag_attrs = {
            'id': id(name),
            'name': name,
            'type': 'password',
            'value': value
    }
    if attrs:
        tag_attrs.update(attrs)
    return Tag('input', attrs=tag_attrs)


def textarea(name, value, attrs):
    """
        >>> textarea('message_text', 'x', {})  #doctest: +NORMALIZE_WHITESPACE
        <textarea rows="9" cols="40" id="message-text"
            name="message_text">x</textarea>

        ``value`` is empty.

        >>> textarea('message_text', '', attrs={
        ...    'class': 'error', 'rows': '10'
        ... })  #doctest: +NORMALIZE_WHITESPACE
        <textarea rows="10" name="message_text" class="error" cols="40"
            id="message-text"></textarea>
    """
    tag_attrs = {
            'id': id(name),
            'name': name,
            'rows': '9',
            'cols': '40'
    }
    if attrs:
        tag_attrs.update(attrs)
    return Tag('textarea', value, tag_attrs)


def checkbox(name, checked, attrs):
    """
        >>> checkbox('accept', 'True', {})  #doctest: +NORMALIZE_WHITESPACE
        <input type="hidden" name="accept" /><input checked="checked"
            type="checkbox" id="accept" value="1" name="accept" />
        >>> checkbox('accept', 'False', {})  #doctest: +NORMALIZE_WHITESPACE
        <input type="hidden" name="accept" /><input type="checkbox"
            id="accept" value="1" name="accept" />

        >>> checkbox('accept', 'True',
        ...         attrs={'class': 'b'})  #doctest: +NORMALIZE_WHITESPACE
        <input type="hidden" name="accept" /><input checked="checked"
            name="accept" type="checkbox" id="accept" value="1" class="b" />
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


def label(name, value, attrs):
    """
        >>> label('zip_code', 'Zip Code', {})
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
        ...     'choices': colors,
        ...     'class': 'error'
        ... })  #doctest: +NORMALIZE_WHITESPACE
        <select class="error" id="favorite-color"
            name="favorite_color"><option value="2">Red</option><option
            selected="selected" value="1">Yellow</option></select>
    """
    choices = attrs.pop('choices')
    options = Fragment([])
    append = options.tags.append
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
        append(Tag('option', inner=text, attrs=tag_attrs))
    tag_attrs = {
            'id': id(name),
            'name': name
    }
    if attrs:
        tag_attrs.update(attrs)
    return Tag('select', inner=options, attrs=tag_attrs)


def radio(name, value, attrs):
    """
        >>> from operator import itemgetter
        >>> scm = sorted({'git': 'Git', 'hg': 'Mercurial'}.items(),
        ...         key=itemgetter(1))

        >>> scm
        [('git', 'Git'), ('hg', 'Mercurial')]

        >>> radio('scm', 'hg', attrs={
        ...     'choices': scm, 'class': 'error'
        ... })  #doctest: +NORMALIZE_WHITESPACE
        <label class="error"><input type="radio" name="scm" value="git"
            class="error" />Git</label><label class="error"><input
            checked="checked" type="radio" name="scm" value="hg"
            class="error" />Mercurial</label>
    """
    choices = attrs.pop('choices')
    elements = []
    append = elements.append
    for key, text in choices:
        tag_attrs = {
                'name': name,
                'type': 'radio',
                'value': key
        }
        if key == value:
            tag_attrs['checked'] = 'checked'
        if attrs:
            tag_attrs.update(attrs)
        append(Tag('label',
            Fragment((Tag('input', attrs=tag_attrs), text)), attrs=attrs))
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
