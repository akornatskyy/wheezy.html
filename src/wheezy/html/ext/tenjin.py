""" ``tenjin`` extension module.
"""

import re

from wheezy.html.ext.lexer import (
    InlinePreprocessor,
    Preprocessor,
    WhitespacePreprocessor,
)


class TenjinPreprocessor(Preprocessor):
    def __init__(self):
        super(TenjinPreprocessor, self).__init__(
            r"(?P<expr_filter>[#\$])\{((?P<expr>.+?)\."
            r"(?P<widget>%(widgets)s){1}"
            r"\((?P<params>.*?)\)\s*)\}"
        )

    EXPRESSION = "%(expr_filter)s{%(expr)s}"

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
<?py #pass ?>
<?py for item in %(value)s: ?>
<input type="hidden" name="%(name)s" value="%(expr_filter)s{item}" />\
<?py #pass ?>
<?py #endfor ?>"""

    INPUT = """\
<input id="%(id)s" name="%(name)s" type="%(type)s"%(attrs)s%(class)s\
<?py if %(value)s%(condition)s: ?>
 value="${%(func)s}" /><?py #pass ?>
<?py else: ?>
 /><?py #pass ?>
<?py #endif ?>"""

    CHECKBOX = """\
<input id="%(id)s" name="%(name)s" type="checkbox" \
value="1"%(attrs)s%(class)s\
<?py if %(value)s: ?>
 checked="checked"<?py #pass ?>
<?py #endif ?>
 />"""

    MULTIPLE_CHECKBOX = """\
<?py #pass ?>
<?py for key, text in %(choices)s: ?>
<label%(attrs)s%(class)s><input id="%(id)s" name="%(name)s" type="checkbox" \
value="1"%(attrs)s%(class)s<?py #pass ?>
<?py if key in %(value)s: ?>
 checked="checked"<?py #pass ?>
<?py #endif ?>
 />%(expr_filter)s{text}</label><?py #pass ?>
<?py #endfor ?>"""

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
<select id="%(id)s" name="%(name)s"%(attrs)s%(class)s>\
<?py #pass ?>
<?py for key, text in %(choices)s: ?>
<option value="%(expr_filter)s{key}"<?py #pass ?>
<?py if key == %(value)s: ?>
 selected="selected"<?py #pass ?>
<?py #endif ?>
>%(expr_filter)s{text}</option><?py #pass ?>
<?py #endfor ?>\
</select>"""

    MULTIPLE_SELECT = """\
<?py #pass ?>
<select id="%(id)s" name="%(name)s" multiple="multiple"%(attrs)s%(class)s>\
<?py #pass ?>
<?py for key, text in %(choices)s: ?>
<option value="%(expr_filter)s{key}"<?py #pass ?>
<?py if key in %(value)s: ?>
 selected="selected"<?py #pass ?>
<?py #endif ?>
>%(expr_filter)s{text}</option><?py #pass ?>
<?py #endfor ?>\
</select>"""

    ERROR = """\
<?py #pass ?>
<?py if '%(name)s' in errors: ?>
<span%(attrs)s>%(expr_filter)s{errors['%(name)s'][-1]}</span>\
<?py #pass ?>
<?py #endif ?>"""

    MESSAGE = """\
<?py #pass ?>
<?py if %(value)s: ?>
<span%(attrs)s>%(info)s</span><?py #pass ?>
<?py #endif ?>"""


widget_preprocessor = TenjinPreprocessor()
whitespace_preprocessor = WhitespacePreprocessor(
    rules=[
        (re.compile(r"^ \s+|\s+$", re.MULTILINE), r""),
        (re.compile(r"(?<!\?)>\s+<(?!\?)"), r"><"),
    ]
)


RE_INLINE = re.compile(
    r'<\?py\s+inline\(("|\')(?P<path>.+?)\1\)\s*\?>', re.MULTILINE
)


def inline_preprocessor(directories, fallback=False):
    """Inline preprocessor. Rewrite <?py inline("...") ?> tag with
    file content. If fallback is ``True`` rewrite to
    <?py include("...") ?> tag.

    >>> t = '1 <?py inline("master.html") ?> 2'
    >>> m = RE_INLINE.search(t)
    >>> m.group('path')
    'master.html'
    >>> t[:m.start()], t[m.end():]
    ('1 ', ' 2')
    >>> m = RE_INLINE.search(' <?py inline("shared/footer.html") ?>')
    >>> m.group('path')
    'shared/footer.html'
    """
    strategy = (
        fallback and (lambda path: '<?py include("' + path + '") ?>') or None
    )
    return InlinePreprocessor(RE_INLINE, directories, strategy)
