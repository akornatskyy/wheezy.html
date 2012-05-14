
""" ``lexer`` module
"""

import re

from wheezy.html.ext.parser import parse_known_function
from wheezy.html.ext.parser import parse_name
from wheezy.html.ext.parser import parse_params
from wheezy.html.ext.parser import parse_str_or_int
from wheezy.html.utils import html_id


class Preprocessor(object):
    """ Generic widget preprocessor.
    """

    CHECKBOX = None
    ERROR = None
    ERROR_CLASS0 = None
    ERROR_CLASS1 = None
    EXPRESSION = None
    HIDDEN = '<input type="hidden" name="%(name)s" value="%(value)s" />'
    INPUT = None
    LABEL = '<label for="%(id)s"%(attrs)s%(class)s>%(value)s</label>'
    MESSAGE = None
    MULTIPLE_CHECKBOX = None
    MULTIPLE_HIDDEN = None
    PREPEND = None
    RADIO = None
    SELECT = None
    TEXTAREA = None

    # region: preprocessing

    def __init__(self, widgets_pattern):
        self.widgets = {
            'checkbox': self.checkbox,
            'dropdown': self.dropdown,
            'emptybox': self.emptybox,
            'error': self.error,
            'hidden': self.hidden,
            'info': self.info,
            'label': self.label,
            'listbox': self.listbox,
            'multiple_checkbox': self.multiple_checkbox,
            'multiple_hidden': self.multiple_hidden,
            'multiple_select': self.listbox,
            'password': self.password,
            'radio': self.radio,
            'select': self.dropdown,
            'textarea': self.textarea,
            'textbox': self.textbox,
            'warning': self.warning,
        }
        assert '%(widgets)s' in widgets_pattern
        self.RE_WIDGETS = re.compile(widgets_pattern % {
            'widgets': '|'.join(sorted(self.widgets.keys()))})

    def __call__(self, text, **kwargs):
        """ Preprocess input text.
        """
        result = []
        start = 0
        for m in self.RE_WIDGETS.finditer(text):
            result.append(text[start:m.start()])
            start = m.end()
            parts = m.groupdict()
            widget = self.widgets[parts.pop('widget')]
            widget = widget(**parts)
            result.append(widget)
        if start > 0 and self.PREPEND:
            result.insert(0, self.PREPEND)
        result.append(text[start:])
        return ''.join(result)

    # region: helpers

    def expression(self, text, expr_filter=''):
        """ Interpretate ``text`` as string expression or
            python expression.
        """
        value = parse_str_or_int(text)
        return value or self.EXPRESSION % {
                        'expr': text,
                        'expr_filter': expr_filter}

    def join_attrs(self, kwargs):
        """ Joins ``kwargs`` as html attributes.
        """
        if kwargs:
            return ' ' + ' '.join([
                '%s="%s"' % (k, self.expression(kwargs[k]))
                for k in kwargs])
        else:
            return ''

    def error_class(self, name, class_):
        """ Checks for error and add css class error.
        """
        if class_:
            return self.ERROR_CLASS1 % {
                    'name': name,
                    'class': self.expression(class_)}
        else:
            return self.ERROR_CLASS0 % {
                    'name': name}

    # region: widgets

    def hidden(self, expr, params, expr_filter):
        """ HTML element input hidden.
        """
        name = parse_name(expr)
        return self.HIDDEN % {
                'name': name,
                'value': self.expression(expr, expr_filter)}

    def multiple_hidden(self, expr, params, expr_filter):
        """ Multiple HTML element input of type hidden.
        """
        name = parse_name(expr)
        return self.MULTIPLE_HIDDEN % {
            'name': name,
            'value': expr,
            'expr_filter': expr_filter}

    def label(self, expr, params, expr_filter):
        """ HTML element label.
        """
        name = parse_name(expr)
        args, kwargs = parse_params(params)
        class_ = kwargs.pop('class', None)
        return self.LABEL % {
            'id': html_id(name),
            'name': name,
            'value': self.expression(args[0], expr_filter),
            'attrs': self.join_attrs(kwargs),
            'class': self.error_class(name, class_)}

    def emptybox(self, expr, params, expr_filter):
        """ HTML element input of type text. Value is rendered
            only if evaluated to boolean True.
        """
        return self.input_helper(expr, params, expr_filter, 'empty')

    def textbox(self, expr, params, expr_filter):
        """ HTML element input of type text. Value is rendered
            only if it is not None or ''.
        """
        return self.input_helper(expr, params, expr_filter, 'text')

    def password(self, expr, params, expr_filter):
        """ HTML element input of type password. Value is rendered
            only if it is not None or ''.
        """
        return self.input_helper(expr, params, expr_filter, 'password')

    def input_helper(self, expr, params, expr_filter, input_type):
        """ HTML element input of type input_type.
        """
        name = parse_name(expr)
        args, kwargs = parse_params(params)
        class_ = kwargs.pop('class', None)
        if input_type == 'empty':
            input_type = 'text'
            condition = ''
        else:
            condition = " not in (None, '')"
        value, func = parse_known_function(expr)
        return self.INPUT % {
            'id': html_id(name),
            'name': name,
            'type': input_type,
            'value': value,
            'condition': condition,
            'func': func,
            'expr_filter': expr_filter,
            'attrs': self.join_attrs(kwargs),
            'class': self.error_class(name, class_)}

    def textarea(self, expr, params, expr_filter):
        """ HTML element textarea.
        """
        name = parse_name(expr)
        args, kwargs = parse_params(params)
        kwargs.setdefault('rows', '"9"')
        kwargs.setdefault('cols', '"40"')
        class_ = kwargs.pop('class', None)
        return self.TEXTAREA % {
            'id': html_id(name),
            'name': name,
            'value': self.expression(expr, expr_filter),
            'attrs': self.join_attrs(kwargs),
            'class': self.error_class(name, class_)}

    def checkbox(self, expr, params, expr_filter):
        """ HTML element input of type checkbox.
        """
        name = parse_name(expr)
        args, kwargs = parse_params(params)
        class_ = kwargs.pop('class', None)
        return self.CHECKBOX % {
            'id': html_id(name),
            'name': name,
            'value': expr,
            'attrs': self.join_attrs(kwargs),
            'class': self.error_class(name, class_)}

    def multiple_checkbox(self, expr, params, expr_filter):
        """ Multiple HTML element input of type checkbox.
        """
        name = parse_name(expr)
        args, kwargs = parse_params(params)
        choices = kwargs.pop('choices')
        class_ = kwargs.pop('class', None)
        return self.MULTIPLE_CHECKBOX % {
            'id': html_id(name),
            'name': name,
            'choices': choices,
            'value': expr,
            'expr_filter': expr_filter,
            'attrs': self.join_attrs(kwargs),
            'class': self.error_class(name, class_)}

    def radio(self, expr, params, expr_filter):
        """ A group of HTML input elements of type radio.
        """
        name = parse_name(expr)
        args, kwargs = parse_params(params)
        class_ = kwargs.pop('class', None)
        choices = kwargs.pop('choices')
        return self.RADIO % {
            'id': html_id(name),
            'name': name,
            'choices': choices,
            'value': expr,
            'expr_filter': expr_filter,
            'attrs': self.join_attrs(kwargs),
            'class': self.error_class(name, class_)}

    def dropdown(self, expr, params, expr_filter):
        """
        """
        return self.select_helper(expr, params, expr_filter, '')

    def listbox(self, expr, params, expr_filter):
        """
        """
        return self.select_helper(
                expr, params, expr_filter, ' multiple="multiple"')

    def select_helper(self, expr, params, expr_filter, select_type):
        """ HTML element select.
        """
        name = parse_name(expr)
        args, kwargs = parse_params(params)
        class_ = kwargs.pop('class', None)
        choices = kwargs.pop('choices')
        return self.SELECT % {
            'id': html_id(name),
            'name': name,
            'select_type': select_type,
            'choices': choices,
            'value': expr,
            'expr_filter': expr_filter,
            'attrs': self.join_attrs(kwargs),
            'class': self.error_class(name, class_)}

    def error(self, expr, params, expr_filter):
        """ General error message or field error.
        """
        name = parse_name(expr)
        args, kwargs = parse_params(params)
        if expr.startswith(name):
            name = '__ERROR__'
            class_ = 'error-message'
        else:
            class_ = 'error'
        return self.ERROR % {
            'name': name,
            'attrs': self.join_attrs(kwargs),
            'class': class_,
            'expr_filter': expr_filter}

    def info(self, expr, params, expr_filter):
        """ General info message.
        """
        return self.message_helper(expr, params, expr_filter, 'info')

    def warning(self, expr, params, expr_filter):
        """ General warning message.
        """
        return self.message_helper(expr, params, expr_filter, 'warning')

    def message_helper(self, expr, params, expr_filter, class_):
        """ General info message.
        """
        name = parse_name(expr)
        args, kwargs = parse_params(params)
        if expr.startswith(name):
            class_ = class_ + '-message'
        return self.MESSAGE % {
            'value': expr,
            'info': self.expression(expr, expr_filter),
            'class': class_}


class WhitespacePreprocessor(object):
    """ Whitespace preprocessor.
    """

    def __init__(self, rules):
        self.rules = rules

    def __call__(self, text, **kwargs):
        for r, s in self.rules:
            text = r.sub(s, text)
        return text
