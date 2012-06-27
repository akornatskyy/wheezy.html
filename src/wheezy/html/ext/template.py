

""" ``wheezy.template`` extension module.
"""

import re


from wheezy.html.comp import xrange
from wheezy.html.ext.lexer import Preprocessor
from wheezy.html.ext.lexer import WhitespacePreprocessor


class WheezyPreprocessor(Preprocessor):

    def __init__(self):
        super(WheezyPreprocessor, self).__init__(
            r'@((?P<expr>.+?)\.'
            r'(?P<widget>%(widgets)s){1}\((?P<params>.*?)\)\s*'
            r'(?P<expr_filter>((?<!!)!\w+(!\w+)*|\s*)))(\s|$)')

    EXPRESSION = '@%(expr)s%(expr_filter)s'

    ERROR_CLASS0 = """\\
@if '%(name)s' in errors:
 class="error"\\
@end
"""

    ERROR_CLASS1 = """\\
@if '%(name)s' in errors:
 class="error %(class)s"\\
@else:
 class="%(class)s"\\
@end
"""

    MULTIPLE_HIDDEN = """\\
@for item in %(value)s:
<input type="hidden" name="%(name)s" value="@item%(expr_filter)s" />\
@end
"""

    INPUT = """\\
<input id="%(id)s" name="%(name)s" type="%(type)s"%(attrs)s%(class)s\\
@if %(value)s%(condition)s:
 value="@%(func)s%(expr_filter)s" />\\
@else:
 />\\
@end
"""

    CHECKBOX = """\\
<input id="%(id)s" name="%(name)s" type="checkbox" \
value="1"%(attrs)s%(class)s\\
@if %(value)s:
 checked="checked"\\
@end
 />"""

    MULTIPLE_CHECKBOX = """\\
@for key, text in %(choices)s:
<label%(attrs)s%(class)s><input id="%(id)s" name="%(name)s" type="checkbox" \
value="1"%(attrs)s%(class)s\\
@if key in %(value)s:
 checked="checked"\\
@end
 />@text%(expr_filter)s</label>\\
@end
"""

    RADIO = """\\
@for key, text in %(choices)s:
<label%(attrs)s%(class)s>\
<input type="radio" name="%(name)s"%(attrs)s \
value="@key%(expr_filter)s"%(class)s\\
@if key == %(value)s:
 checked="checked"\\
@end
 />@text%(expr_filter)s</label>\\
@end
"""

    SELECT = """\\
<select id="%(id)s" name="%(name)s"%(select_type)s%(attrs)s%(class)s>\\
@for key, text in %(choices)s:
<option value="@key%(expr_filter)s"\\
@if key == %(value)s:
 selected="selected"\\
@end
>@text%(expr_filter)s</option>\\
@end
</select>"""

    ERROR = """\\
@if '%(name)s' in errors:
<span%(attrs)s>@errors['%(name)s'][-1]%(expr_filter)s</span>\\
@end
"""

    MESSAGE = """\\
@if %(value)s:
<span%(attrs)s>%(info)s</span>\\
@end
"""


class WidgetExtension(object):

    preprocessors = [WheezyPreprocessor()]


whitespace_preprocessor = WhitespacePreprocessor(
    rules=[
        (re.compile(r'^ [ \t]+', re.MULTILINE),
            r''),
        (re.compile(r'>\s*<', re.MULTILINE),
            r'><'),
        (re.compile(r'\s*(?<!\\)\n', re.MULTILINE),
            r'\\\n'),
    ],
    ignore_rules=[
        re.compile(r'<(pre|code).*?>.*?</\1>', re.DOTALL)
    ])


def whitespace_postprocessor(tokens):
    for i in xrange(len(tokens)):
        lineno, token, value = tokens[i]
        if token == 'markup':
            value = whitespace_preprocessor(value)
            tokens[i] = (lineno, token, value)


class WhitespaceExtension(object):

    preprocessors = [WhitespacePreprocessor(rules=[
        (re.compile(r'\s+$', re.MULTILINE), r'')
    ])]

    postprocessors = [whitespace_postprocessor]
