""" Unit tests for ``wheezy.html.ext.tenjin``.
"""

import unittest

from wheezy.html.ext.tests.test_lexer import PreprocessorMixin


class TenjinPreprocessorTestCase(PreprocessorMixin, unittest.TestCase):
    """Test the ``TenjinPreprocessor``."""

    WHITE_SPACE_PATTERNS = ["%(w)s", "[ %(w)s", "%(w)s ", "[ %(w)s "]

    def assert_render_equal(self, template, expected, **kwargs):
        assert_tenjin_equal(template, expected, **kwargs)

    HIDDEN = "${model.pref.hidden()}"
    MULTIPLE_HIDDEN = "#{model.prefs.multiple_hidden()}"
    LABEL = "#{model.username.label('<i>*</i>Username:')}"
    EMPTYBOX = "${model.amount.emptybox(class_='x')}"
    TEXTBOX = "${model.username.textbox(autocomplete='off')}"
    PASSWORD = "${model.pwd.password()}"
    TEXTAREA = "${model.comment.textarea()}"
    CHECKBOX = "#{model.remember_me.checkbox()}"
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
    """Test the ``whitespace_preprocessor``."""

    def test_whitespace(self):
        """"""
        from wheezy.html.ext.tenjin import whitespace_preprocessor

        assert " x" == whitespace_preprocessor(" x")
        assert "x" == whitespace_preprocessor("  \n x \n  ")
        assert "x" == whitespace_preprocessor("  x")
        assert "x" == whitespace_preprocessor("x  ")
        assert "><" == whitespace_preprocessor("  > < ")
        assert ">  <?" == whitespace_preprocessor("  >  <? ")
        assert "?>  <" == whitespace_preprocessor("  ?>  < ")
        assert "?> <?" == whitespace_preprocessor("  ?> <? ")


class InlinePreprocessorTestCase(unittest.TestCase):
    """Test the ``inline_preprocessor``."""

    def p(self, text, fallback=False):
        from wheezy.html.ext.tenjin import inline_preprocessor

        p = inline_preprocessor(directories=["."], fallback=fallback)
        return p(text)

    def test_inline(self):
        assert self.p('<?py inline("LICENSE") ?>')

    def test_inline_fallback(self):
        assert '<?py include("LICENSE") ?>' == self.p(
            '<?py inline("LICENSE") ?>', fallback=True
        )

    def test_inline_not_found(self):
        import warnings

        warnings.simplefilter("ignore")
        assert not self.p('<?py inline("X") ?>')
        warnings.simplefilter("default")


try:
    # from tenjin import Template
    Template = __import__("tenjin", None, None, ["Template"]).Template
    from tenjin.helpers import escape, to_str

    assert escape, to_str
    from wheezy.html.ext.tenjin import widget_preprocessor

    def assert_tenjin_equal(text, expected, **kwargs):
        template = Template(input=widget_preprocessor(text))
        value = template.render(kwargs)
        assert expected == value

except ImportError:  # pragma: nocover

    def assert_tenjin_equal(text, expected, **kwargs):  # noqa
        pass
