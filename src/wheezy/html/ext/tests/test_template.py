
""" Unit tests for ``wheezy.html.ext.mako``.
"""

import unittest

from wheezy.html.ext.tests.test_lexer import PreprocessorMixin


class TemplatePreprocessorTestCase(PreprocessorMixin, unittest.TestCase):
    """ Test the ``MakoPreprocessor``.
    """

    def assert_render_equal(self, template, expected, **kwargs):
        assert_template_equal(template, expected, **kwargs)

    HIDDEN = '@model.pref.hidden()!h'
    MULTIPLE_HIDDEN = '@model.prefs.multiple_hidden()'
    LABEL = "@model.username.label('<i>*</i>Username:')"
    EMPTYBOX = "@model.amount.emptybox(class_='x')!s"
    TEXTBOX = "@model.username.textbox(autocomplete='off')"
    PASSWORD = "@model.pwd.password()"
    TEXTAREA = "@model.comment.textarea()"
    CHECKBOX = "@model.remember_me.checkbox()"
    MULTIPLE_CHECKBOX = "@model.scm.multiple_checkbox(choices=scm)"
    RADIO = "@model.scm.radio(choices=scm)"
    DROPDOWN = "@model.scm.dropdown(choices=scm)"
    LISTBOX = "@model.scm.listbox(choices=scm, class_='x')"
    ERROR = "@model.username.error()"
    GENERAL_ERROR = "@model.error()"
    INFO = "@model.user_info.info()"
    GENERAL_INFO = "@message.info()"
    WARNING = "@model.user_info.warning()"
    GENERAL_WARNING = "@message.warning()"


class WheezyWhitespaceExtensionTestCase(unittest.TestCase):
    """ Test the ``WhitespaceExtension``.
    """

    def setUp(self):
        from wheezy.html.ext.template import WhitespaceExtension
        self.preprocess = WhitespaceExtension.preprocessors[0]

    def test_whitespace(self):
        """
        """
        assert '><' == self.preprocess('  >  <')
        assert '' == self.preprocess('  ')
        assert 'x' == self.preprocess('  x')
        assert '>' == self.preprocess('>  ')
        assert '>\\\n@def' == self.preprocess('>\n@def')
        assert '>\\\n@end' == self.preprocess('>\n@end')
        assert ':\n@end' == self.preprocess(':\n@end')
        assert 'x\\\n@end' == self.preprocess('x\\\n@end')

try:
    from wheezy.html.ext.template import WidgetExtension
    from wheezy.html.utils import html_escape
    from wheezy.template.engine import Engine
    from wheezy.template.ext.core import CoreExtension
    from wheezy.template.loader import DictLoader

    def assert_template_equal(text, expected, **kwargs):
        engine = Engine(
                loader=DictLoader({
                    'x': "@require(model, errors, message, scm)\n" + text}),
                extensions=[CoreExtension, WidgetExtension])
        engine.global_vars.update({'h': html_escape})
        template = engine.get_template('x')
        value = template.render(kwargs)
        assert expected == value

except ImportError:  # pragma: nocover

    def assert_template_equal(text, expected, **kwargs):
        pass
