
""" ``builder`` module.
"""

from wheezy.html.widgets import default


class Widget(object):
    """
    """

    def __init__(self, tag, name, value):
        self.tag = default[tag]
        self.name = name
        self.value = value

    def __call__(self, attr=None, **kwargs):
        return self.tag(self.name, self.value, attr, **kwargs)


class WidgetBuilder(object):
    """

        >>> class User(object): pass
        >>> model = User()

        textbox

        >>> model.age = 33
        >>> h = WidgetBuilder(model, 'age')
        >>> print(h.textbox({'class': 'error'}))
        <input class="error" type="text" id="age" value="33" name="age" />
    """

    __slots__ = ['model', 'name']

    def __init__(self, model, name):
        self.model = model
        self.name = name

    def __repr__(self):
        return str(self.value())

    def value(self):
        return str(getattr(self.model, self.name))

    def __getattr__(self, tag_name):
        return Widget(tag_name, self.name, self.value())
