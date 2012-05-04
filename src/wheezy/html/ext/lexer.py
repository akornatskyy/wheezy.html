
""" ``parser`` module
"""

import re


known_functions = ['format']

RE_ARGS = re.compile(
    '\s*(?P<expr>((?:[\'"]).*?\1|.+?))\s*\,')
RE_KWARGS = re.compile(
    '\s*(?P<name>\w+)\s*=\s*(?P<expr>([\'"].*?[\'"]|.+?))\s*\,')
RE_STR_VALUE = re.compile(
    '[\'"](?P<value>.+)[\'"]$')
RE_FUNCTIONS = re.compile(
    '\.(%s)\(' % '|'.join(known_functions))
RE_FUNCTION = re.compile(
    '(?P<context>.+?)\.(?P<name>%s)\((?P<args>(|.+))\)'
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
    """
        >>> parse_known_function("dob")
        'dob'
        >>> parse_known_function("dob.format()")
        'format_value(dob, None)'
        >>> parse_known_function("user.dob.format(_('YYYY/MM/DD'))")
        "format_value(user.dob, _('YYYY/MM/DD'))"
        >>> parse_known_function("user.dob.format(\
format_provider=lambda value, ignore: value.strftime('%m-%d-%y'))")
        "format_value(user.dob, format_provider=lambda value, \
ignore: value.strftime('%m-%d-%y'))"
    """
    m = RE_FUNCTION.search(expr)
    if not m:
        return expr
    context = m.group('context')
    name = m.group('name')
    args = m.group('args') or 'None'
    return "%s_value(%s, %s)" % (name, context, args)


def parse_kwargs(text):
    """
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