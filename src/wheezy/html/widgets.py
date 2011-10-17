
""" ``widgets`` module.
"""

from wheezy.html.comp import iteritems
from wheezy.html.markup import Fragment
from wheezy.html.markup import Tag


id = lambda name: name.replace('_', '-')


def hidden(name, value, attr=None, **kwargs):
    """
        >>> hidden('pref', 'abc')
        <input type="hidden" name="pref" value="abc" />
    """
    tag_attr = {
            'name': name,
            'type': 'hidden',
            'value': value
    }
    if attr:
        tag_attr.update(attr)
    return Tag('input', attr=tag_attr, **kwargs)


def textbox(name, value, attr=None, **kwargs):
    """
        >>> textbox('zip_code', '79053',
        ...         attr={'size': '10'})  #doctest: +NORMALIZE_WHITESPACE
        <input size="10" type="text" id="zip-code"
            value="79053" name="zip_code" />
    """
    tag_attr = {
            'id': id(name),
            'name': name,
            'type': 'text',
            'value': value
    }
    if attr:
        tag_attr.update(attr)
    return Tag('input', attr=tag_attr, **kwargs)


def checkbox(name, checked, attr=None, **kwargs):
    """
        >>> checkbox('accept', True)  #doctest: +NORMALIZE_WHITESPACE
        <input checked="checked" type="checkbox" id="accept"
            value="1" name="accept" /><input type="hidden"
            name="accept" />
        >>> checkbox('accept', False)  #doctest: +NORMALIZE_WHITESPACE
        <input type="checkbox" id="accept" value="1" name="accept"
            /><input type="hidden" name="accept" />
    """
    tag_attr = {
        'id': id(name),
        'name': name,
        'type': 'checkbox',
        'value': '1'
    }
    if checked:
        tag_attr['checked'] = 'checked'
    if attr:
        tag_attr.update(attr)
    return Fragment(
            Tag('input', attr=tag_attr, **kwargs),
            Tag('input', attr={'name': name, 'type': 'hidden'})
    )


def label(name, text, attr=None, **kwargs):
    """
        >>> label('zip_code', 'Zip Code')
        <label for="zip-code">Zip Code</label>
    """
    tag_attr = {
            'for': id(name)
    }
    if attr:
        tag_attr.update(attr)
    return Tag('label', inner=text, attr=tag_attr, **kwargs)


def dropdown(name, selected, attr=None, **kwargs):
    """
        >>> colors = {'yellow': 'Yellow', 'red': 'Red'}
        >>> dropdown('favorite_color', 'yellow', attr={
        ...     'choices': colors})  #doctest: +NORMALIZE_WHITESPACE
        <select id="favorite-color" name="favorite_color"><option
        value="red">Red</option><option selected="selected"
        value="yellow">Yellow</option></select>
    """
    choices = attr.pop('choices')
    options = []
    for value, text in iteritems(choices):
        if value == selected:
            tag_attr = {
                    'value': value,
                    'selected': 'selected'
            }
        else:
            tag_attr = {
                    'value': value
            }
        options.append(Tag('option', inner=text, attr=tag_attr))
    options = Fragment(*options)
    tag_attr = {
            'id': id(name),
            'name': name
    }
    if attr:
        tag_attr.update(attr)
    return Tag('select', inner=options, attr=tag_attr, **kwargs)

default = {
        'hidden': hidden,
        'textbox': textbox,
        'checkbox': checkbox,
        'label': label
}
