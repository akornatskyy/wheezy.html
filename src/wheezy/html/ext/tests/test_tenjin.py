
""" Unit tests for ``wheezy.html.ext.mako``.
"""

import unittest

from wheezy.html.ext.tests.test_lexer import PreprocessorMixin


class Dummy(object):
    pass


class TenjinPreprocessorTestCase(unittest.TestCase, PreprocessorMixin):
    """ Test the ``TenjinPreprocessor``.
    """

    def setUp(self):
        from wheezy.html.ext.tenjin import widget_preprocessor
        self.p = widget_preprocessor
        self.m = Dummy()
        self.e = {}

    def assert_render_equal(self, template, expected, **kwargs):
        assert_tenjin_equal(template, expected, **kwargs)

    HIDDEN = '${model.pref.hidden()}'
    MULTIPLE_HIDDEN = '#{model.prefs.multiple_hidden()}'
    LABEL = "#{model.username.label('<i>*</i>Username:')}"
    EMPTYBOX = "${model.amount.emptybox(class_='x')}"
    TEXTBOX = "${model.username.textbox(autocomplete='off')}"
    PASSWORD = "${model.pwd.password()}"
    TEXTAREA = "${model.comment.textarea()}"
    CHECKBOX = "#{model.accepts.checkbox()}"
    MULTIPLE_CHECKBOX = "#{model.scm.multiple_checkbox(choices=scm)}"
    RADIO = "#{model.scm.radio(choices=scm)}"
    DROPDOWN = "#{model.scm.dropdown(choices=scm)}"
    LISTBOX = "#{model.scm.listbox(choices=scm, class_='x')}"
    ERROR = "#{model.username.error()}"
    GENERAL_ERROR = "#{model.error()}"
    INFO = "#{model.user_info.info()}"
    GENERAL_INFO = "${message.info()}"
    WARNING = "#{model.user_info.warning()}"
    GENERAL_WARNING = "${message.warning()}"


class TenjinWhitespacePreprocessorTestCase(unittest.TestCase):
    """ Test the ``whitespace_preprocessor``.
    """

    def test_whitespace(self):
        """
        """
        from wheezy.html.ext.tenjin import whitespace_preprocessor
        assert 'x' == whitespace_preprocessor('  \n x \n  ')
        assert 'x' == whitespace_preprocessor('  x')
        assert 'x' == whitespace_preprocessor('x  ')
        assert '><' == whitespace_preprocessor('  > < ')
        assert '>  <?' == whitespace_preprocessor('  >  <? ')
        assert '?>  <' == whitespace_preprocessor('  ?>  < ')
        assert '?> <?' == whitespace_preprocessor('  ?> <? ')


try:
    # from tenjin import Template
    Template = __import__('tenjin', None, None,
            ['Template']).Template

    from tenjin.helpers import escape, to_str
    assert escape, to_str

    def assert_tenjin_equal(text, expected, **kwargs):
        template = Template(input=text)
        value = template.render(kwargs)
        assert expected == value

except ImportError:  # pragma: nocover

    def assert_tenjin_equal(text, expected, **kwargs):
        pass
