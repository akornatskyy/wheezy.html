
""" ``mako`` extension module.
"""

import re

from wheezy.html.ext.lexer import Preprocessor
from wheezy.html.ext.lexer import WhitespacePreprocessor


class MakoPreprocessor(Preprocessor):

    def __init__(self, skip_imports=False):
        super(MakoPreprocessor, self).__init__(
            r'(?<!##)\s*\$\{((?P<expr>.+?)\.'
            r'(?P<widget>%(widgets)s){1}\((?P<params>.*?)\)\s*'
            r'(?P<expr_filter>(\|\s*[\w,\s]+?|\s*)))\}\s*')

    PREPEND = """\
<%!
from wheezy.html.utils import format_value
%>"""

    EXPRESSION = '${%(expr)s%(expr_filter)s}'

    ERROR_CLASS0 = """\\
%% if '%(name)s' in errors:
 class="error"\\
%% endif
"""

    ERROR_CLASS1 = """\\
%% if '%(name)s' in errors:
 class="error %(class)s"\\
%% else:
 class="%(class)s"\\
%% endif
"""

    MULTIPLE_HIDDEN = """\\
%% for item in %(value)s:
<input type="hidden" name="%(name)s" value="${item%(expr_filter)s}" />\\
%% endfor
"""

    INPUT = """\
<input id="%(id)s" name="%(name)s" type="%(type)s"%(attrs)s%(class)s\
%% if %(value)s%(condition)s:
 value="${%(func)s%(expr_filter)s}" />\\
%% else:
 />\\
%% endif
"""

    CHECKBOX = """\
<input id="%(id)s" name="%(name)s" type="checkbox" \
value="1"%(attrs)s%(class)s\
%% if %(value)s:
 checked="checked"\\
%% endif
 />"""

    MULTIPLE_CHECKBOX = """\\
%% for key, text in %(choices)s:
<label%(attrs)s%(class)s><input id="%(id)s" name="%(name)s" type="checkbox" \
value="1"%(attrs)s%(class)s\
%% if key in %(value)s:
 checked="checked"\\
%% endif
 />${text%(expr_filter)s}</label>\\
%% endfor
"""

    RADIO = """\\
%% for key, text in %(choices)s:
<label%(attrs)s%(class)s>\
<input type="radio" name="%(name)s"%(attrs)s \
value="${key%(expr_filter)s}"%(class)s\
%% if key == %(value)s:
 checked="checked"\\
%% endif
 />${text%(expr_filter)s}</label>\\
%% endfor
"""

    SELECT = """\
<select id="%(id)s" name="%(name)s"%(select_type)s%(attrs)s%(class)s>\\
%% for key, text in %(choices)s:
<option value="${key%(expr_filter)s}"\\
%% if key == %(value)s:
 selected="selected"\\
%% endif
>${text%(expr_filter)s}</option>\\
%% endfor
</select>"""

    ERROR = """\\
%% if '%(name)s' in errors:
<span class="%(class)s">${errors['%(name)s'][-1]%(expr_filter)s}</span>\\
%% endif
"""

    MESSAGE = """\\
%% if %(value)s:
<span class="%(class)s">%(info)s</span>\\
%% endif
"""


widget_preprocessor = MakoPreprocessor()

""" TODO
    >>> whitespace_preprocessor('  > < ')
    '><'
"""
whitespace_preprocessor = WhitespacePreprocessor(rules=[
        (re.compile(r'>\s+<'),
            r'><'),
        (re.compile(r'^ \s+|\s+$', re.MULTILINE),
            r'')])
