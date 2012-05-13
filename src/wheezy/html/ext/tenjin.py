
""" ``tenjin`` extension module.
"""

import re

from wheezy.html.ext.lexer import Preprocessor
from wheezy.html.ext.lexer import WhitespacePreprocessor


class TenjinPreprocessor(Preprocessor):

    def __init__(self):
        super(TenjinPreprocessor, self).__init__(
            r'\s*(?P<expr_filter>[#\$])\{((?P<expr>.+?)\.'
            r'(?P<widget>%s){1}'
            r'\((?P<params>.*?)\)\s*)\}\s*')

    EXPRESSION = '%(expr_filter)s{%(expr)s}'

    ERROR_CLASS0 = """\
<?py #pass ?>
<?py if '%(name)s' in errors: ?>
 class="error"<?py #pass ?>
<?py #endif ?>"""

    ERROR_CLASS1 = """\
<?py #pass ?>
<?py if '%(name)s' in errors: ?>
 class="error %(class)s"<?py #pass ?>
<?py else: ?>
 class="%(class)s"<?py #pass ?>
<?py #endif ?>"""

    MULTIPLE_HIDDEN = """\
"""

    INPUT = """\
<input id="%(id)s" name="%(name)s" type="%(type)s"%(attrs)s%(class)s\
<?py if %(value)s%(condition)s: ?>
 value="${%(func)s}" /><?py #pass ?>
<?py else: ?>
 /><?py #pass ?>
<?py #endif ?>"""

    TEXTAREA = """\
"""

    CHECKBOX = """\
<input id="%(id)s" name="%(name)s" type="checkbox" \
value="1"%(attrs)s%(class)s\
<?py if %(value)s: ?>
 checked="checked"<?py #pass ?>
<?py #endif ?>
 />"""

    MULTIPLE_CHECKBOX = """\
"""

    RADIO = """\
<?py #pass ?>
<?py for key, text in %(choices)s: ?>
<label%(attrs)s%(class)s>\
<input type="radio" name="%(name)s"%(attrs)s \
value="%(expr_filter)s{key}"%(class)s
<?py if key == %(value)s: ?>
 checked="checked"<?py #pass ?>
<?py #endif ?>
 />%(expr_filter)s{text}</label><?py #pass ?>
<?py #endfor ?>"""

    SELECT = """\
<?py #pass ?>
<select id="%(id)s" name="%(name)s"%(select_type)s%(attrs)s%(class)s>\
<?py #pass ?>
<?py for key, text in %(choices)s: ?>
<option value="%(expr_filter)s{key}"<?py #pass ?>
<?py if key == %(value)s: ?>
 selected="selected"<?py #pass ?>
<?py #endif ?>
>%(expr_filter)s{text}</option><?py #pass ?>
<?py #endfor ?>\
</select>"""

    ERROR = """\
<?py #pass ?>
<?py if '%(name)s' in errors: ?>
<span class="%(class)s">%(expr_filter)s{errors['%(name)s'][-1]}</span>\
<?py #pass ?>
<?py #endif ?>"""

    INFO = """\
"""


widget_preprocessor = TenjinPreprocessor()

""" TODO
    >>> whitespace_preprocessor('  > < ')
    '><'
    >>> whitespace_preprocessor('  ?> <? ')
    '?> <?'
"""
whitespace_preprocessor = WhitespacePreprocessor(rules=[
        (re.compile(r'(?<!\?)>\s+<(?!\?)'),
            r'><'),
        (re.compile(r'^ \s+|\s+$', re.MULTILINE),
            r'')])
