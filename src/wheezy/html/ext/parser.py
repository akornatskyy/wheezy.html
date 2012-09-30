
""" ``parser`` module
"""

import re


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
        >>> sorted(parse_kwargs('autocomplete="off", maxlength=12').items())
        [('autocomplete', '"off"'), ('maxlength', '12')]
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


def parse_str_or_int(text):
    """ Interpretate ``text`` as string or int expression.

        >>> parse_str_or_int('"Hello"')
        'Hello'
        >>> parse_str_or_int("'Hello'")
        'Hello'
        >>> parse_str_or_int('100')
        '100'
        >>> parse_str_or_int('model.username')
    """
    m = RE_STR_VALUE.match(text)
    if m:
        return m.group('value')
    else:
        m = RE_INT_VALUE.match(text)
        if m:
            return m.group('value')
        else:
            return None
