

""" ``jinja2`` extension module.
"""

import re

# from jinja2.ext import Extension
Extension = __import__('jinja2.ext', None, None, ['Extension']).Extension

from wheezy.html.ext.lexer import InlinePreprocessor
from wheezy.html.ext.lexer import Preprocessor
from wheezy.html.ext.lexer import WhitespacePreprocessor


class Jinja2Preprocessor(Preprocessor):

    def __init__(self,
                 variable_start_string=None,
                 variable_end_string=None):
        pattern = r'\s*\{\{((?P<expr>.+?)\.'\
            r'(?P<widget>%(widgets)s){1}\((?P<params>.*?)\)\s*'\
            r'(?P<expr_filter>(\|\s*[\w,\s]+?|\s*)))\}\}\s*'
        if variable_start_string:
            pattern = pattern.replace('\{\{',
                                      re.escape(variable_start_string))
        if variable_end_string:
            pattern = pattern.replace('\}\}',
                                      re.escape(variable_end_string))
        super(Jinja2Preprocessor, self).__init__(pattern)

        attrs = [
            'EXPRESSION', 'ERROR', 'SELECT', 'INPUT', 'CHECKBOX',
            'MULTIPLE_CHECKBOX', 'MULTIPLE_HIDDEN', 'RADIO'
        ]
        c = self.__class__.__dict__
        for attr in attrs:
            self.__dict__[attr] = c[attr].replace(
                '{{', variable_start_string).replace(
                    '}}', variable_end_string)

    EXPRESSION = '{{ %(expr)s%(expr_filter)s }}'

    ERROR_CLASS0 = """\
{%% if '%(name)s' in errors: %%}\
 class="error"\
{%% endif %%}"""

    ERROR_CLASS1 = """\
{%% if '%(name)s' in errors: %%}\
 class="error %(class)s"\
{%% else: %%}\
 class="%(class)s"\
{%% endif %%}"""

    MULTIPLE_HIDDEN = """\
{%% for item in %(value)s: %%}\
<input type="hidden" name="%(name)s" value="{{ item%(expr_filter)s }}" />\
{%% endfor %%}
"""

    INPUT = """\
<input id="%(id)s" name="%(name)s" type="%(type)s"%(attrs)s%(class)s\
{%% if %(value)s%(condition)s: %%}\
 value="{{ %(func)s%(expr_filter)s }}" />\
{%% else: %%}\
 />\
{%% endif %%}"""

    CHECKBOX = """\
<input id="%(id)s" name="%(name)s" type="checkbox" \
value="1"%(attrs)s%(class)s\
{%% if %(value)s: %%}\
 checked="checked"\
{%% endif %%}\
 />"""

    MULTIPLE_CHECKBOX = """\
{%% for key, text in %(choices)s: %%}\
<label%(attrs)s%(class)s><input id="%(id)s" name="%(name)s" type="checkbox" \
value="1"%(attrs)s%(class)s\
{%% if key in %(value)s: %%}\
 checked="checked"\
{%% endif %%}\
 />{{ text%(expr_filter)s }}</label>\
{%% endfor %%}"""

    RADIO = """\
{%% for key, text in %(choices)s: %%}\
<label%(attrs)s%(class)s>\
<input type="radio" name="%(name)s"%(attrs)s \
value="{{ key%(expr_filter)s }}"%(class)s\
{%% if key == %(value)s: %%}\
 checked="checked"\
{%% endif %%}\
 />{{ text%(expr_filter)s }}</label>\
{%% endfor %%}"""

    SELECT = """\
<select id="%(id)s" name="%(name)s"%(select_type)s%(attrs)s%(class)s>\
{%% for key, text in %(choices)s: %%}\
<option value="{{ key%(expr_filter)s }}"\
{%% if key == %(value)s: %%}\
 selected="selected"\
{%% endif %%}\
>{{ text%(expr_filter)s }}</option>\
{%% endfor %%}\
</select>"""

    ERROR = """\
{%% if '%(name)s' in errors: %%}\
<span%(attrs)s>{{ errors['%(name)s'][-1]%(expr_filter)s }}</span>\
{%% endif %%}"""

    MESSAGE = """\
{%% if %(value)s: %%}\
<span%(attrs)s>%(info)s</span>\
{%% endif %%}"""


class WidgetExtension(Extension):

    def __init__(self, environment):
        super(WidgetExtension, self).__init__(environment)
        self.preprocessor = Jinja2Preprocessor(
            variable_start_string=environment.variable_start_string,
            variable_end_string=environment.variable_end_string)

    def preprocess(self, source, name, filename=None):
        return self.preprocessor(source)


class WhitespaceExtension(Extension):

    def __init__(self, environment):
        super(WhitespaceExtension, self).__init__(environment)
        block_start_string = environment.block_start_string
        block_end_string = environment.block_end_string
        self.preprocessor = WhitespacePreprocessor(rules=[
            (re.compile(r'^ \s+|\s+$', re.MULTILINE),
                r''),
            (re.compile(r'>\s+<'),
                r'><'),
            (re.compile(
                r'>\s+\{%'.replace('\{%', re.escape(block_start_string))),
                r'>{%'.replace('{%', block_start_string)),
            (re.compile(
                r'%\}\s+<'.replace('%\}', re.escape(block_end_string))),
                r'%}<'.replace('%}', block_end_string)),
        ])

    def preprocess(self, source, name, filename=None):
        return self.preprocessor(source)


RE_INLINE = re.compile(r'{%\s*inline\s+("|\')(?P<path>.+?)\1\s*%}',
                       re.MULTILINE)


class InlineExtension(Extension):
    """ Inline preprocessor. Rewrite {% inline "..." %} tag with
        file content. If fallback is ``True`` rewrite to
        {% include "..." %} tag.

        >>> t = '1 {% inline "master.html" %} 2'
        >>> m = RE_INLINE.search(t)
        >>> m.group('path')
        'master.html'
        >>> t[:m.start()], t[m.end():]
        ('1 ', ' 2')
        >>> m = RE_INLINE.search(' {% inline "shared/footer.html" %}')
        >>> m.group('path')
        'shared/footer.html'
    """

    def __init__(self, searchpath, fallback=False):
        strategy = fallback and (
            lambda path: '{% include "' + path + '" %}') or None
        self.preprocessor = InlinePreprocessor(
            RE_INLINE, searchpath, strategy)

    def __call__(self, environment):
        super(InlineExtension, self).__init__(environment)
        return self

    def preprocess(self, source, name, filename=None):
        return self.preprocessor(source)
