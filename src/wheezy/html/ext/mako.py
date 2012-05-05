
""" ``mako`` extension module.
"""

import re

from wheezy.html.ext.lexer import RE_INT_VALUE
from wheezy.html.ext.lexer import RE_STR_VALUE
from wheezy.html.ext.lexer import parse_known_function
from wheezy.html.ext.lexer import parse_name
from wheezy.html.ext.lexer import parse_params
from wheezy.html.utils import html_id


# region: widgets

def hidden(expr, params, filter):
    """ HTML element input hidden.

        >>> t = "${user.pref.hidden()}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        <input type="hidden" name="pref" value="${user.pref}" />

        >>> t = "${user.pref.hidden()|h}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        <input type="hidden" name="pref" value="${user.pref|h}" />

        >>> class User(object):
        ...     pref = 'abc'
        >>> assert_mako_equal(mako_template,
        ... '<input type="hidden" name="pref" value="abc" />', user=User())
    """
    name = parse_name(expr)
    return """\
<input type="hidden" name="%(name)s" value="%(value)s" />""" % {
        'name': name,
        'value': expression(expr, filter)}


def multiple_hidden(expr, params, filter):
    """
        >>> t = "${user.prefs.multiple_hidden()}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        \\
        % for item in user.prefs:
        <input type="hidden" name="prefs" value="${item}" />\\
        % endfor
        <BLANKLINE>

        >>> t = "${user.prefs.multiple_hidden()|h}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        \\
        % for item in user.prefs:
        <input type="hidden" name="prefs" value="${item|h}" />\\
        % endfor
        <BLANKLINE>
        >>> class User(object):
        ...     prefs = ['a', 'b']
        >>> assert_mako_equal(mako_template,
        ... '<input type="hidden" name="prefs" value="a" \
/><input type="hidden" name="prefs" value="b" />', user=User())
    """
    name = parse_name(expr)
    return """\\
%% for item in %(value)s:
<input type="hidden" name="%(name)s" value="${item%(filter)s}" />\\
%% endfor
""" % {
        'name': name,
        'value': expr,
        'filter': filter}


def label(expr, params, filter):
    """ HTML element label.

        >>> t = "${credential.username.label(_('<Username>'))|h}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        <label for="username"\\
        % if 'username' in errors:
         class="error"\\
        % endif
        >${_('<Username>')|h}</label>

        >>> _ = lambda s: s
        >>> assert_mako_equal(mako_template,
        ... '<label for="username">&lt;Username&gt;</label>', _=_)

        >>> t = "${credential.username.label('<i>*</i>Username:')}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        <label for="username"\\
        % if 'username' in errors:
         class="error"\\
        % endif
        ><i>*</i>Username:</label>

        >>> assert_mako_equal(mako_template,
        ... '<label for="username"><i>*</i>Username:</label>')
    """
    name = parse_name(expr)
    args, kwargs = parse_params(params)
    class_ = kwargs.pop('class', None)
    return """\
<label for="%(id)s"%(attrs)s%(class)s>%(value)s</label>""" % {
        'id': html_id(name),
        'name': name,
        'value': expression(args[0], filter),
        'attrs': join_attrs(kwargs),
        'class': error_class(name, class_)}


def input(expr, params, filter, input_type):
    """ HTML element input of type input_type.

        >>> t = "${transfer_spec.min_amount.emptybox(maxlength=5)}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        <input id="min-amount" name="min_amount" type="text" \
maxlength="5"\\
        % if 'min_amount' in errors:
         class="error"\\
        % endif
        % if transfer_spec.min_amount:
         value="${transfer_spec.min_amount}" />\\
        % else:
         />\\
        % endif
        <BLANKLINE>

        >>> t = "${credential.password.password(autocomplete='off')|h}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        <input id="password" name="password" type="password" \
autocomplete="off"\\
        % if 'password' in errors:
         class="error"\\
        % endif
        % if credential.password not in (None, ''):
         value="${credential.password|h}" />\\
        % else:
         />\\
        % endif
        <BLANKLINE>

        >>> class Credential(object):
        ...     password = '<x'
        >>> assert_mako_equal(mako_template, '<input id="password" \
name="password" type="password" autocomplete="off" value="&lt;x" />',
        ...     credential=Credential())


        >>> t = "${registration.date_of_birth.format(_('YYYY/MM/DD'))\
        ... .textbox(autocomplete='off')}"
        >>> mako_template = widget_preprocessor(t)
        >>> print(mako_template)
        <%!
        from wheezy.html.utils import format_value
        %><input id="date-of-birth" name="date_of_birth" type="text" \
autocomplete="off"\\
        % if 'date_of_birth' in errors:
         class="error"\\
        % endif
        % if registration.date_of_birth not in (None, ''):
         value="${format_value(registration.date_of_birth, \
_('YYYY/MM/DD'))}" />\\
        % else:
         />\\
        % endif
        <BLANKLINE>

        >>> from datetime import date
        >>> class Registration(object):
        ...     def __init__(self):
        ...         self.date_of_birth = date(2012, 2, 20)
        >>> _ = lambda s: s
        >>> assert_mako_equal(mako_template, '<input id="date-of-birth" \
name="date_of_birth" type="text" autocomplete="off" value="YYYY/MM/DD" />',
        ...         registration=Registration(), _=_)
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
    return """\
<input id="%(id)s" name="%(name)s" type="%(type)s"%(attrs)s%(class)s\
%% if %(value)s%(condition)s:
 value="${%(func)s%(filter)s}" />\\
%% else:
 />\\
%% endif
""" % {
        'id': html_id(name),
        'name': name,
        'type': input_type,
        'value': value,
        'condition': condition,
        'func': func,
        'filter': filter,
        'attrs': join_attrs(kwargs),
        'class': error_class(name, class_)}


def textarea(expr, params, filter):
    """ HTML element textarea.

        >>> t = "${user.notes.textarea()|h}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        <textarea id="notes" name="notes" rows="9" cols="40"\\
        % if 'notes' in errors:
         class="error"\\
        % endif
        >${user.notes|h}</textarea>

        >>> class User(object):
        ...     notes = 'abc'
        >>> t = "${user.notes.textarea(rows='10')}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> assert_mako_equal(mako_template,
        ... '<textarea id="notes" name="notes" rows="10" cols="40">\
abc</textarea>', user=User())
    """
    name = parse_name(expr)
    args, kwargs = parse_params(params)
    kwargs.setdefault('rows', '"9"')
    kwargs.setdefault('cols', '"40"')
    class_ = kwargs.pop('class', None)
    return """\
<textarea id="%(id)s" name="%(name)s"%(attrs)s%(class)s>\
%(value)s</textarea>""" % {
        'id': html_id(name),
        'name': name,
        'value': expression(expr, filter),
        'attrs': join_attrs(kwargs),
        'class': error_class(name, class_)}


def checkbox(expr, params, filter):
    """ HTML element input of type checkbox.

        >>> t = "${model.remember_me.checkbox()}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        <input id="remember-me" name="remember_me" type="checkbox" value="1"\\
        % if 'remember_me' in errors:
         class="error"\\
        % endif
        % if model.remember_me:
         checked="checked"\\
        % endif
         />

        >>> class User(object):
        ...     remember_me = True
        >>> t = "${model.remember_me.checkbox()}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> assert_mako_equal(mako_template,
        ... '<input id="remember-me" name="remember_me" type="checkbox" \
value="1" checked="checked" />', model=User())
    """
    assert not filter
    name = parse_name(expr)
    args, kwargs = parse_params(params)
    class_ = kwargs.pop('class', None)
    return """\
<input id="%(id)s" name="%(name)s" type="checkbox" \
value="1"%(attrs)s%(class)s\
%% if %(value)s:
 checked="checked"\\
%% endif
 />""" % {
        'id': html_id(name),
        'name': name,
        'value': expr,
        'attrs': join_attrs(kwargs),
        'class': error_class(name, class_)}


def multiple_checkbox(expr, params, filter):
    """ HTML element input of type checkbox.

        >>> t = "${model.scm.multiple_checkbox(choices=scm)|h}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        \\
        % for key, text in scm:
        <label\\
        % if 'scm' in errors:
         class="error"\\
        % endif
        ><input id="scm" name="scm" type="checkbox" value="1"\\
        % if 'scm' in errors:
         class="error"\\
        % endif
        % if key in model.scm:
         checked="checked"\\
        % endif
         />${text|h}</label>\\
        % endfor
        <BLANKLINE>

        >>> from operator import itemgetter
        >>> scm = sorted({
        ...         'git': 'Git', 'hg': 'Mercurial', 'svn': 'SVN'
        ...     }.items(),
        ...     key=itemgetter(1))
        >>> scm
        [('git', 'Git'), ('hg', 'Mercurial'), ('svn', 'SVN')]
        >>> class User(object):
        ...     scm = ['hg', 'git']
        >>> t = "${model.scm.multiple_checkbox(choices=scm)}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> assert_mako_equal(mako_template,
        ... '<label><input id="scm" name="scm" type="checkbox" value="1" \
checked="checked" />Git</label><label><input id="scm" name="scm" \
type="checkbox" value="1" checked="checked" />Mercurial</label>\
<label><input id="scm" name="scm" type="checkbox" value="1" />SVN</label>',
        ... model=User(), scm=scm)
    """
    name = parse_name(expr)
    args, kwargs = parse_params(params)
    choices = kwargs.pop('choices')
    class_ = kwargs.pop('class', None)
    return """\\
%% for key, text in %(choices)s:
<label%(attrs)s%(class)s><input id="%(id)s" name="%(name)s" type="checkbox" \
value="1"%(attrs)s%(class)s\
%% if key in %(value)s:
 checked="checked"\\
%% endif
 />${text%(filter)s}</label>\\
%% endfor
""" % {
        'id': html_id(name),
        'name': name,
        'choices': choices,
        'value': expr,
        'filter': filter,
        'attrs': join_attrs(kwargs),
        'class': error_class(name, class_)}


def radio(expr, params, filter):
    """ A group of html input elements of type radio.

        >>> t = "${account.account_type.radio(choices=account_types)}"
        >>> print(widget_preprocessor(t, skip_imports=True))
        \\
        % for key, text in account_types:
        <label\\
        % if 'account_type' in errors:
         class="error"\\
        % endif
        ><input type="radio" name="account_type" value="${key}"\\
        % if 'account_type' in errors:
         class="error"\\
        % endif
        % if key == account.account_type:
         checked="checked"\\
        % endif
         />${text}</label>\\
        % endfor
        <BLANKLINE>

        >>> from operator import itemgetter
        >>> scm = sorted({
        ...         'git': 'Git', 'hg': 'Mercurial', 'svn': 'SVN'
        ...     }.items(),
        ...     key=itemgetter(1))
        >>> scm
        [('git', 'Git'), ('hg', 'Mercurial'), ('svn', 'SVN')]
        >>> class User(object):
        ...     scm = 'hg'
        >>> t = "${model.scm.radio(choices=scm)}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> assert_mako_equal(mako_template,
        ... '<label><input type="radio" name="scm" value="git" \
/>Git</label><label><input type="radio" name="scm" value="hg" \
checked="checked" />Mercurial</label><label><input type="radio" \
name="scm" value="svn" />SVN</label>',
        ... model=User(), scm=scm)
    """
    name = parse_name(expr)
    args, kwargs = parse_params(params)
    class_ = kwargs.pop('class', None)
    choices = kwargs.pop('choices')
    return """\\
%% for key, text in %(choices)s:
<label%(attrs)s%(class)s>\
<input type="radio" name="%(name)s"%(attrs)s \
value="${key%(filter)s}"%(class)s\
%% if key == %(value)s:
 checked="checked"\\
%% endif
 />${text%(filter)s}</label>\\
%% endfor
""" % {
        'id': html_id(name),
        'name': name,
        'value': expr,
        'filter': filter,
        'attrs': join_attrs(kwargs),
        'class': error_class(name, class_),
        'choices': choices}


def select(expr, params, filter, select_type):
    """
        >>> t = "${model.questionid.dropdown(choices=questions)|h}"
        >>> print(widget_preprocessor(t, skip_imports=True))
        <select id="questionid" name="questionid"\\
        % if 'questionid' in errors:
         class="error"\\
        % endif
        >\\
        % for key, text in questions:
        <option value="${key|h}"\\
        % if key == model.questionid:
         selected="selected"\\
        % endif
        >${text|h}</option>\\
        % endfor
        </select>
        >>> t = "${model.questionid.listbox(choices=questions)|h}"
        >>> print(widget_preprocessor(t, skip_imports=True))
        <select id="questionid" name="questionid" multiple="multiple"\\
        % if 'questionid' in errors:
         class="error"\\
        % endif
        >\\
        % for key, text in questions:
        <option value="${key|h}"\\
        % if key == model.questionid:
         selected="selected"\\
        % endif
        >${text|h}</option>\\
        % endfor
        </select>

        >>> from operator import itemgetter
        >>> scm = sorted({
        ...         'git': 'Git', 'hg': 'Mercurial', 'svn': 'SVN'
        ...     }.items(),
        ...     key=itemgetter(1))
        >>> scm
        [('git', 'Git'), ('hg', 'Mercurial'), ('svn', 'SVN')]
        >>> class User(object):
        ...     scm = 'hg'
        >>> t = "${model.scm.select(choices=scm)}"
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> assert_mako_equal(mako_template,
        ... '<select id="scm" name="scm"><option value="git">Git</option>\
<option value="hg" selected="selected">Mercurial</option><option \
value="svn">SVN</option></select>',
        ... model=User(), scm=scm)
    """
    name = parse_name(expr)
    args, kwargs = parse_params(params)
    class_ = kwargs.pop('class', None)
    choices = kwargs.pop('choices')
    return """\
<select id="%(id)s" name="%(name)s"%(select_type)s%(attrs)s%(class)s>\\
%% for key, text in %(choices)s:
<option value="${key%(filter)s}"\\
%% if key == %(value)s:
 selected="selected"\\
%% endif
>${text%(filter)s}</option>\\
%% endfor
</select>""" % {
        'id': html_id(name),
        'name': name,
        'select_type': select_type,
        'value': expr,
        'filter': filter,
        'attrs': join_attrs(kwargs),
        'class': error_class(name, class_),
        'choices': choices}


def error(expr, params, filter):
    """
        >>> t = "${model.error()|h}"
        >>> print(widget_preprocessor(t, skip_imports=True))
        \\
        % if '__ERROR__' in errors:
        <span class="error-message">${errors['__ERROR__'][-1]|h}</span>\\
        % endif
        <BLANKLINE>

        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> assert_mako_equal(mako_template,
        ... '')

        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> assert_mako_equal(mako_template,
        ... '<span class="error-message">Error Message</span>',
        ... errors={'__ERROR__': ['Error Message']})

        >>> t = "${credential.username.error()}"
        >>> print(widget_preprocessor(t, skip_imports=True))
        \\
        % if 'username' in errors:
        <span class="error">${errors['username'][-1]}</span>\\
        % endif
        <BLANKLINE>

        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> assert_mako_equal(mako_template,
        ... '')

        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> assert_mako_equal(mako_template,
        ... '<span class="error">Error Message</span>',
        ... errors={'username': ['Error Message']})
    """
    name = parse_name(expr)
    args, kwargs = parse_params(params)
    if expr.startswith(name):
        name = '__ERROR__'
        class_ = 'error-message'
    else:
        class_ = 'error'
    return """\\
%% if '%(name)s' in errors:
<span class="%(class)s">${errors['%(name)s'][-1]%(filter)s}</span>\\
%% endif
""" % {
        'name': name,
        'attrs': join_attrs(kwargs),
        'class': class_,
        'filter': filter}


def info(expr, params, filter, class_):
    """
        >>> t = "${message.warning()}"
        >>> print(widget_preprocessor(t, skip_imports=True))
        \\
        % if message:
        <span class="warning-message">${message}</span>\\
        % endif
        <BLANKLINE>

        >>> t = "${message.info()}"
        >>> print(widget_preprocessor(t, skip_imports=True))
        \\
        % if message:
        <span class="info-message">${message}</span>\\
        % endif
        <BLANKLINE>

        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> assert_mako_equal(mako_template,
        ... '<span class="info-message">Saved.</span>', message='Saved.')

        >>> t = "${user.name_status.warning()|h}"
        >>> print(widget_preprocessor(t, skip_imports=True))
        \\
        % if user.name_status:
        <span class="warning">${user.name_status|h}</span>\\
        % endif
        <BLANKLINE>

        >>> t = "${user.name_status.info()|h}"
        >>> print(widget_preprocessor(t, skip_imports=True))
        \\
        % if user.name_status:
        <span class="info">${user.name_status|h}</span>\\
        % endif
        <BLANKLINE>

        >>> class User(object):
        ...     name_status = 'Available'
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> assert_mako_equal(mako_template,
        ... '<span class="info">Available</span>', user=User())
    """
    name = parse_name(expr)
    args, kwargs = parse_params(params)
    if expr.startswith(name):
        class_ = class_ + '-message'
    return """\\
%% if %(value)s:
<span class="%(class)s">%(info)s</span>\\
%% endif
""" % {
        'value': expr,
        'info': expression(expr, filter),
        'class': class_}


# region: helpers

def expression(text, filter=''):
    """ Interpretate ``text`` as string expression or
        python expression.

        >>> expression('"Hello"')
        'Hello'
        >>> expression('"Hello"', '|h')
        'Hello'
        >>> expression('100')
        '100'
        >>> expression('model.username')
        '${model.username}'
        >>> expression('model.username', '|h')
        '${model.username|h}'
    """
    m = RE_STR_VALUE.match(text)
    if m:
        return m.group('value')
    else:
        m = RE_INT_VALUE.match(text)
        if m:
            return m.group('value')
        else:
            return '${%s%s}' % (text, filter)


def join_attrs(kwargs):
    """ Joins ``kwargs`` as html attributes.

        >>> join_attrs({})
        ''
        >>> join_attrs({'class': '"inline"', 'choices': 'account_types'})
        ' class="inline" choices="${account_types}"'
    """
    if kwargs:
        return ' ' + ' '.join(['%s="%s"' % (k, expression(kwargs[k]))
                for k in kwargs])
    else:
        return ''


def error_class(name, class_):
    """ Checks for error and add css class error.

        >>> t = error_class('username', '')
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        \\
        % if 'username' in errors:
         class="error"\\
        % endif
        <BLANKLINE>

        >>> assert_mako_equal(mako_template,
        ... '')
        >>> assert_mako_equal(mako_template,
        ... ' class="error"', errors={'username': []})

        >>> t = error_class('username', '"inline"')
        >>> mako_template = widget_preprocessor(t, skip_imports=True)
        >>> print(mako_template)
        \\
        % if 'username' in errors:
         class="error inline"\\
        % else:
         class="inline"\\
        % endif
        <BLANKLINE>

        >>> assert_mako_equal(mako_template,
        ... ' class="inline"')
        >>> assert_mako_equal(mako_template,
        ... ' class="error inline"', errors={'username': []})
    """
    if class_:
        return """\\
%% if '%(name)s' in errors:
 class="error %(class)s"\\
%% else:
 class="%(class)s"\\
%% endif
""" % {'name': name, 'class': expression(class_)}
    else:
        return """\\
%% if '%(name)s' in errors:
 class="error"\\
%% endif
""" % {'name': name}

# region: preprocessing

widgets = {
    'hidden': hidden,
    'multiple_hidden': multiple_hidden,
    'label': label,
    'emptybox': lambda expr, params, filter: input(
            expr, params, filter, 'empty'),
    'textbox': lambda expr, params, filter: input(
            expr, params, filter, 'text'),
    'password': lambda expr, params, filter: input(
            expr, params, filter, 'password'),
    'textarea': textarea,
    'checkbox': checkbox,
    'multiple_checkbox': multiple_checkbox,
    'radio': radio,
    'dropdown': lambda expr, params, filter: select(
            expr, params, filter, ''),
    'select': lambda expr, params, filter: select(
            expr, params, filter, ''),
    'listbox': lambda expr, params, filter: select(
            expr, params, filter, ' multiple="multiple"'),
    'multiple_select': lambda expr, params, filter: select(
            expr, params, filter, ' multiple="multiple"'),
    'error': error,
    'info': lambda expr, params, filter: info(
            expr, params, filter, 'info'),
    'warning': lambda expr, params, filter: info(
            expr, params, filter, 'warning')
}

RE_WIDGETS = re.compile(
        '(?<!##)\s*\$\{((?P<expr>.+?)\.(?P<widget>%s){1}\((?P<params>.*?)\)\s*'
        '(?P<filter>(\|\s*[\w,\s]+?|\s*)))\}\s*'
        % '|'.join(widgets))


def widget_preprocessor(text, skip_imports=False):
    """
        >>> t = "&nbsp;   ${credential.username.label('Username:')}\
${credential.username.textbox()}${credential.username.error()} &nbsp;"
        >>> mako_template = widget_preprocessor(t)
        >>> print(mako_template)
        <%!
        from wheezy.html.utils import format_value
        %>&nbsp;<label for="username"\\
        % if 'username' in errors:
         class="error"\\
        % endif
        >Username:</label><input id="username" name="username" type="text"\\
        % if 'username' in errors:
         class="error"\\
        % endif
        % if credential.username not in (None, ''):
         value="${credential.username}" />\\
        % else:
         />\\
        % endif
        \\
        % if 'username' in errors:
        <span class="error">${errors['username'][-1]}</span>\\
        % endif
        &nbsp;
    """
    result = []
    start = 0
    for m in RE_WIDGETS.finditer(text):
        result.append(text[start:m.start()])
        start = m.end()
        parts = m.groupdict()
        widget = widgets[parts.pop('widget')]
        widget = widget(**parts)
        result.append(widget)
    if not skip_imports and start > 0:
        result.insert(0, """\
<%!
from wheezy.html.utils import format_value
%>""")
    result.append(text[start:])
    return ''.join(result)

try:
    # from mako.template import Template
    Template = __import__('mako.template', None, None,
            ['Template']).Template

    def assert_mako_equal(text, expected, **kwargs):
        template = Template(text)
        kwargs.setdefault('errors', {})
        value = template.render(**kwargs)
        assert expected == value

except ImportError:  # pragma: nocover

    def assert_mako_equal(text, expected, **kwargs):
        pass
