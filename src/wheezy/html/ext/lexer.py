
""" ``parser`` module
"""

import re

from wheezy.html.utils import html_id


known_functions = ['format']

RE_ARGS = re.compile(
    r'\s*(?P<expr>(([\'"]).*?\3|.+?))\s*\,')
RE_KWARGS = re.compile(
    r'\s*(?P<name>\w+)\s*=\s*(?P<expr>([\'"].*?[\'"]|.+?))\s*\,')
RE_STR_VALUE = re.compile(
    r'^[\'"](?P<value>.+)[\'"]$')
RE_INT_VALUE = re.compile(
    r'^(?P<value>(\d+))$')
RE_FUNCTIONS = re.compile(
    r'\.(%s)\(' % '|'.join(known_functions))
RE_FUNCTION = re.compile(
    r'(?P<context>.+?)\.(?P<name>%s)\((?P<args>(|.+))\)'
    % '|'.join(known_functions))


def parse_name(expr):
    """ Parses name from expression of the following form::

        [object.]name[.format(...]

        >>> parse_name('display_name')
        'display_name'
        >>> parse_name('account.display_name')
        'display_name'
        >>> parse_name('account.display_name.format(')
        'display_name'
    """
    expr = RE_FUNCTIONS.split(expr)[0]
    name = expr.rsplit('.', 1)[-1]
    return name


def parse_known_function(expr):
    """ Parses known functions.

        >>> parse_known_function("dob")
        ('dob', 'dob')
        >>> parse_known_function("dob.format()")
        ('dob', 'format_value(dob, None)')
        >>> parse_known_function("user.dob.format(_('YYYY/MM/DD'))")
        ('user.dob', "format_value(user.dob, _('YYYY/MM/DD'))")
        >>> parse_known_function("user.dob.format(\
format_provider=lambda value, ignore: value.strftime('%m-%d-%y'))")
        ('user.dob', "format_value(user.dob, format_provider=lambda value, \
ignore: value.strftime('%m-%d-%y'))")
    """
    m = RE_FUNCTION.search(expr)
    if not m:
        return expr, expr
    context = m.group('context')
    name = m.group('name')
    args = m.group('args') or 'None'
    return context, "%s_value(%s, %s)" % (name, context, args)


def parse_kwargs(text):
    """ Parses key-value type of parameters.

        >>> parse_kwargs('choices=account_types')
        {'choices': 'account_types'}
        >>> parse_kwargs('autocomplete="off", maxlength=12')
        {'autocomplete': '"off"', 'maxlength': '12'}
    """
    kwargs = {}
    for m in RE_KWARGS.finditer(text + ','):
        groups = m.groupdict()
        kwargs[groups['name'].rstrip('_')] = groups['expr']
    return kwargs


def parse_args(text):
    """ Parses argument type of parameters.

        >>> parse_args('')
        []
        >>> parse_args('10, "x"')
        ['10', '"x"']
        >>> parse_args("'x', 100")
        ["'x'", '100']
        >>> parse_args('"Account Type:"')
        ['"Account Type:"']
    """
    args = []
    for m in RE_ARGS.finditer(text + ','):
        args.append(m.group('expr'))
    return args


def parse_params(text):
    """ Parses function parameters.

        >>> parse_params('')
        ([], {})
        >>> parse_params('choices=account_types')
        ([], {'choices': 'account_types'})
        >>> parse_params('"Account Type:"')
        (['"Account Type:"'], {})
        >>> parse_params('"Account Type:", class_="inline"')
        (['"Account Type:"'], {'class': '"inline"'})
    """
    if '=' in text:
        args = text.split('=')[0]
        if ',' in args:
            args = args.rsplit(',', 1)[0]
            kwargs = text[len(args):]
            return parse_args(args), parse_kwargs(kwargs)
        else:
            return [], parse_kwargs(text)
    else:
        return parse_args(text), {}


class Preprocessor(object):
    """ Generic widget preprocessor.
    """

    PREPEND = None
    EXPRESSION = '%(expr)s%(expr_filter)s'
    ERROR_CLASS0 = """\
"""
    ERROR_CLASS1 = """\
"""
    HIDDEN = """\
<input type="hidden" name="%(name)s" value="%(value)s" />"""
    MULTIPLE_HIDDEN = """\
"""
    LABEL = """\
<label for="%(id)s"%(attrs)s%(class)s>%(value)s</label>"""
    INPUT = """\
"""
    TEXTAREA = """\
"""
    CHECKBOX = """\
"""
    MULTIPLE_CHECKBOX = """\
"""
    RADIO = """\
"""
    SELECT = """\
"""
    ERROR = """\
"""
    INFO = """\
"""

    # region: preprocessing

    def __init__(self, widgets_pattern):
        self.widgets = {
            'hidden': self.hidden,
            'multiple_hidden': self.multiple_hidden,
            'label': self.label,
            'emptybox': lambda expr, params, expr_filter: self.input(
                    expr, params, expr_filter, 'empty'),
            'textbox': lambda expr, params, expr_filter: self.input(
                    expr, params, expr_filter, 'text'),
            'password': lambda expr, params, expr_filter: self.input(
                    expr, params, expr_filter, 'password'),
            'textarea': self.textarea,
            'checkbox': self.checkbox,
            'multiple_checkbox': self.multiple_checkbox,
            'radio': self.radio,
            'dropdown': lambda expr, params, expr_filter: self.select(
                    expr, params, expr_filter, ''),
            'select': lambda expr, params, expr_filter: self.select(
                    expr, params, expr_filter, ''),
            'listbox': lambda expr, params, expr_filter: self.select(
                    expr, params, expr_filter, ' multiple="multiple"'),
            'multiple_select': lambda expr, params, expr_filter: self.select(
                    expr, params, expr_filter, ' multiple="multiple"'),
            'error': self.error,
            'info': lambda expr, params, expr_filter: self.info(
                    expr, params, expr_filter, 'info'),
            'warning': lambda expr, params, expr_filter: self.info(
                    expr, params, expr_filter, 'warning')
        }
        self.RE_WIDGETS = re.compile(
                widgets_pattern % '|'.join(self.widgets))

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
        m = RE_STR_VALUE.match(text)
        if m:
            return m.group('value')
        else:
            m = RE_INT_VALUE.match(text)
            if m:
                return m.group('value')
            else:
                return self.EXPRESSION % {
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

    def input(self, expr, params, expr_filter, input_type):
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
            'value': expr,
            'expr_filter': expr_filter,
            'attrs': self.join_attrs(kwargs),
            'class': self.error_class(name, class_),
            'choices': choices}

    def select(self, expr, params, expr_filter, select_type):
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
            'value': expr,
            'expr_filter': expr_filter,
            'attrs': self.join_attrs(kwargs),
            'class': self.error_class(name, class_),
            'choices': choices}

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

    def info(self, expr, params, filter, class_):
        """ General info message.
        """
        name = parse_name(expr)
        args, kwargs = parse_params(params)
        if expr.startswith(name):
            class_ = class_ + '-message'
        return self.INFO % {
            'value': expr,
            'info': self.expression(expr, filter),
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
