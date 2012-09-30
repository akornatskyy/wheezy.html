
""" ``widgets`` module.
"""

from wheezy.html.markup import Fragment
from wheezy.html.markup import Tag
from wheezy.html.utils import html_id


def hidden(name, value, attrs=None):
    """ HTML element input of type hidden.

        >>> hidden('pref', 'abc')
        <input name="pref" type="hidden" value="abc" />
    """
    return Tag('input', None, {
        'name': name,
        'type': 'hidden',
        'value': value
    })


def multiple_hidden(name, value, attrs=None):
    """ Renders several HTML input elements of type hidden per
        item in the value list.

        >>> items = ('a', 'b')
        >>> multiple_hidden('pref', items)  #doctest: +NORMALIZE_WHITESPACE
        <input name="pref" type="hidden" value="a" /><input name="pref"
            type="hidden" value="b" />
    """
    return Fragment([hidden(name, item) for item in value])


def emptybox(name, value, attrs=None):
    """ HTML element input of type text.

        >>> emptybox('zip_code', '',
        ...         attrs={'class': 'error'})  #doctest: +NORMALIZE_WHITESPACE
        <input class="error" id="zip-code" name="zip_code" type="text" />

        >>> emptybox('zip_code', '79053',
        ...         attrs={'class': 'error'})  #doctest: +NORMALIZE_WHITESPACE
        <input class="error" id="zip-code" name="zip_code" type="text"
            value="79053" />
    """
    tag_attrs = {
        'id': html_id(name),
        'name': name,
        'type': 'text'
    }
    if value:
        tag_attrs['value'] = value
    if attrs:
        tag_attrs.update(attrs)
    return Tag('input', None, tag_attrs)


def textbox(name, value, attrs=None):
    """ HTML element input of type text.

        >>> textbox('zip_code', '',
        ...         attrs={'class': 'error'})  #doctest: +NORMALIZE_WHITESPACE
        <input class="error" id="zip-code" name="zip_code" type="text" />

        >>> textbox('zip_code', '79053',
        ...         attrs={'class': 'error'})  #doctest: +NORMALIZE_WHITESPACE
        <input class="error" id="zip-code" name="zip_code" type="text"
            value="79053" />
    """
    tag_attrs = {
        'id': html_id(name),
        'name': name,
        'type': 'text'
    }
    if value not in (None, ''):
        tag_attrs['value'] = value
    if attrs:
        tag_attrs.update(attrs)
    return Tag('input', None, tag_attrs)


def password(name, value, attrs=None):
    """ HTML element input of type password.

        >>> password('passwd', '',
        ...         attrs={'class': 'error'})  #doctest: +NORMALIZE_WHITESPACE
        <input class="error" id="passwd" name="passwd" type="password" />

        >>> password('passwd', 'x',
        ...         attrs={'class': 'error'})  #doctest: +NORMALIZE_WHITESPACE
        <input class="error" id="passwd" name="passwd" type="password"
            value="x" />
    """
    tag_attrs = {
        'id': html_id(name),
        'name': name,
        'type': 'password'
    }
    if value not in (None, ''):
        tag_attrs['value'] = value
    if attrs:
        tag_attrs.update(attrs)
    return Tag('input', None, tag_attrs)


def textarea(name, value, attrs):
    """ HTML element textarea.

        >>> textarea('message_text', 'x', {})  #doctest: +NORMALIZE_WHITESPACE
        <textarea cols="40" id="message-text" name="message_text"
            rows="9">x</textarea>

        ``value`` is empty.

        >>> textarea('message_text', '', attrs={
        ...    'class': 'error', 'rows': '10'
        ... })  #doctest: +NORMALIZE_WHITESPACE
        <textarea class="error" cols="40" id="message-text"
            name="message_text" rows="10"></textarea>
    """
    tag_attrs = {
        'id': html_id(name),
        'name': name,
        'rows': '9',
        'cols': '40'
    }
    if attrs:
        tag_attrs.update(attrs)
    return Tag('textarea', value, tag_attrs)


def checkbox(name, checked, attrs):
    """ HTML element input of type checkbox.

        >>> checkbox('accept', 'True', {})  #doctest: +NORMALIZE_WHITESPACE
        <input checked="checked" id="accept" name="accept" type="checkbox"
            value="1" />
        >>> checkbox('accept', 'False', {})  #doctest: +NORMALIZE_WHITESPACE
        <input id="accept" name="accept" type="checkbox" value="1" />

        >>> checkbox('accept', 'True',
        ...         attrs={'class': 'b'})  #doctest: +NORMALIZE_WHITESPACE
        <input checked="checked" class="b" id="accept" name="accept"
            type="checkbox" value="1" />
     """
    tag_attrs = {
        'id': html_id(name),
        'name': name,
        'type': 'checkbox',
        'value': '1'
    }
    if checked == 'True':
        tag_attrs['checked'] = 'checked'
    if attrs:
        tag_attrs.update(attrs)
    return Tag('input', None, tag_attrs)


def multiple_checkbox(name, value, attrs):
    """ Renders several HTML elements of type checkbox per item
        in the value list nested into HTML label element.

        >>> from operator import itemgetter
        >>> scm = sorted({
        ...         'git': 'Git', 'hg': 'Mercurial', 'svn': 'SVN'
        ...     }.items(),
        ...     key=itemgetter(1))
        >>> scm
        [('git', 'Git'), ('hg', 'Mercurial'), ('svn', 'SVN')]

        >>> multiple_checkbox('scm', ['hg', 'git'], attrs={
        ...     'choices': scm, 'class': 'error'
        ... })  #doctest: +NORMALIZE_WHITESPACE
        <label class="error"><input checked="checked" class="error"
            name="scm" type="checkbox" value="git" />Git</label><label
            class="error"><input checked="checked" class="error" name="scm"
            type="checkbox" value="hg" />Mercurial</label><label
            class="error"><input class="error" name="scm" type="checkbox"
            value="svn" />SVN</label>
    """
    choices = attrs.pop('choices')
    elements = []
    append = elements.append
    for key, text in choices:
        tag_attrs = {
            'name': name,
            'type': 'checkbox',
            'value': key
        }
        if key in value:
            tag_attrs['checked'] = 'checked'
        if attrs:
            tag_attrs.update(attrs)
        append(Tag('label',
                   Fragment((Tag('input', None, tag_attrs), text)), attrs))
    return Fragment(elements)


def label(name, value, attrs):
    """ HTML element label.

        >>> label('zip_code', 'Zip Code', {})
        <label for="zip-code">Zip Code</label>
        >>> label('zip_code', 'Zip Code', attrs={'class_': 'inline'})
        <label class="inline" for="zip-code">Zip Code</label>
    """
    tag_attrs = {
        'for': html_id(name)
    }
    if attrs:
        tag_attrs.update(attrs)
    return Tag('label', value, tag_attrs)


def dropdown(name, value, attrs):
    """ HTML element select (there is also synonym ``select``).
        Attribute ``choices`` is a list of HTML options.

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
    options = []
    append = options.append
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
        append(Tag('option', text, tag_attrs))
    tag_attrs = {
        'id': html_id(name),
        'name': name
    }
    if attrs:
        tag_attrs.update(attrs)
    return Tag('select', Fragment(options), tag_attrs)


def listbox(name, value, attrs):
    """ HTML element select of type multiple (there is also
        synonym ``multiple_select``). Attribute ``choices`` is a
        list of HTML options.

        >>> from operator import itemgetter
        >>> colors = sorted({'1': 'Yellow', '2': 'Red', '3': 'Blue'}.items(),
        ...         key=itemgetter(1))
        >>> colors
        [('3', 'Blue'), ('2', 'Red'), ('1', 'Yellow')]
        >>> listbox('favorite_color', ['1', '3'], attrs={
        ...     'choices': colors,
        ...     'class': 'error'
        ... })  #doctest: +NORMALIZE_WHITESPACE
        <select class="error" id="favorite-color" multiple="multiple"
            name="favorite_color"><option selected="selected"
            value="3">Blue</option><option value="2">Red</option><option
            selected="selected" value="1">Yellow</option></select>
    """
    choices = attrs.pop('choices')
    options = []
    append = options.append
    for key, text in choices:
        if key in value:
            tag_attrs = {
                'value': key,
                'selected': 'selected'
            }
        else:
            tag_attrs = {
                'value': key
            }
        append(Tag('option', text, tag_attrs))
    tag_attrs = {
        'id': html_id(name),
        'name': name,
        'multiple': 'multiple'
    }
    if attrs:
        tag_attrs.update(attrs)
    return Tag('select', Fragment(options), tag_attrs)


def radio(name, value, attrs):
    """ A group of html input elements of type radio. Attribute
        ``choices`` is a list of options.

        >>> from operator import itemgetter
        >>> scm = sorted({'git': 'Git', 'hg': 'Mercurial'}.items(),
        ...         key=itemgetter(1))

        >>> scm
        [('git', 'Git'), ('hg', 'Mercurial')]

        >>> radio('scm', 'hg', attrs={
        ...     'choices': scm, 'class': 'error'
        ... })  #doctest: +NORMALIZE_WHITESPACE
        <label class="error"><input class="error" name="scm" type="radio"
            value="git" />Git</label><label class="error"><input
            checked="checked" class="error" name="scm" type="radio"
            value="hg" />Mercurial</label>
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
                   Fragment((Tag('input', None, tag_attrs), text)), attrs))
    return Fragment(elements)

default = {
    'hidden': hidden,
    'multiple_hidden': multiple_hidden,
    'emptybox': emptybox,
    'textbox': textbox,
    'password': password,
    'textarea': textarea,
    'checkbox': checkbox,
    'multiple_checkbox': multiple_checkbox,
    'label': label,
    'dropdown': dropdown,
    'select': dropdown,
    'listbox': listbox,
    'multiple_select': listbox,
    'radio': radio
}
