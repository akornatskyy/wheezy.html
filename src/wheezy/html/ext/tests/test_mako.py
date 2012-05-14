
""" Unit tests for ``wheezy.html.ext.mako``.
"""

import unittest

from wheezy.html.ext.tests.test_lexer import PreprocessorMixin


class Dummy(object):
    pass


class MakoPreprocessorTestCase(unittest.TestCase, PreprocessorMixin):
    """ Test the ``MakoPreprocessor``.
    """

    def setUp(self):
        from wheezy.html.ext.mako import widget_preprocessor
        self.p = widget_preprocessor
        self.m = Dummy()
        self.e = {}

    def assert_render_equal(self, template, expected, **kwargs):
        assert_mako_equal(template, expected, **kwargs)

    HIDDEN = '${model.pref.hidden()|h}'
    MULTIPLE_HIDDEN = '${model.prefs.multiple_hidden()}'
    LABEL = "${model.username.label('<i>*</i>Username:')}"
    EMPTYBOX = "${model.amount.emptybox(class_='x')|h}"
    TEXTBOX = "${model.username.textbox(autocomplete='off')|h}"
    PASSWORD = "${model.pwd.password()|h}"
    TEXTAREA = "${model.comment.textarea()|h}"
    CHECKBOX = "${model.accepts.checkbox()}"
    MULTIPLE_CHECKBOX = "${model.scm.multiple_checkbox(choices=scm)}"
    RADIO = "${model.scm.radio(choices=scm)}"
    DROPDOWN = "${model.scm.dropdown(choices=scm)}"
    LISTBOX = "${model.scm.listbox(choices=scm, class_='x')}"
    ERROR = "${model.username.error()}"
    GENERAL_ERROR = "${model.error()}"
    INFO = "${model.user_info.info()}"
    GENERAL_INFO = "${message.info()|h}"
    WARNING = "${model.user_info.warning()}"
    GENERAL_WARNING = "${message.warning()|h}"

try:
    # from mako.template import Template
    Template = __import__('mako.template', None, None,
            ['Template']).Template

    def assert_mako_equal(text, expected, **kwargs):
        template = Template(text)
        value = template.render(**kwargs)
        assert expected == value

except ImportError:  # pragma: nocover

    def assert_mako_equal(text, expected, **kwargs):
        pass
