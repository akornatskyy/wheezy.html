import unittest

from wheezy.html.ext.tests.test_lexer import PreprocessorMixin


class MakoPreprocessorTestCase(PreprocessorMixin, unittest.TestCase):
    """Test the ``MakoPreprocessor``."""

    WHITE_SPACE_PATTERNS = ["%(w)s", " %(w)s", "%(w)s ", " %(w)s "]

    def assert_render_equal(self, template, expected, **kwargs):
        assert_mako_equal(template, expected, **kwargs)

    HIDDEN = "${model.pref.hidden()|h}"
    MULTIPLE_HIDDEN = "${model.prefs.multiple_hidden()}"
    LABEL = "${model.username.label('<i>*</i>Username:')}"
    EMPTYBOX = "${model.amount.emptybox(class_='x')|h}"
    TEXTBOX = "${model.username.textbox(autocomplete='off')|h}"
    PASSWORD = "${model.pwd.password()|h}"
    TEXTAREA = "${model.comment.textarea()|h}"
    CHECKBOX = "${model.remember_me.checkbox()}"
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


class MakoWhitespacePreprocessorTestCase(unittest.TestCase):
    """Test the ``whitespace_preprocessor``."""

    def test_whitespace(self):
        """"""
        from wheezy.html.ext.mako import whitespace_preprocessor

        assert " x" == whitespace_preprocessor(" x")
        assert "x" == whitespace_preprocessor("  \n x \n  ")
        assert "x" == whitespace_preprocessor("  x")
        assert "x" == whitespace_preprocessor("x  ")
        assert "><" == whitespace_preprocessor("  > < ")


class InlinePreprocessorTestCase(unittest.TestCase):
    """Test the ``inline_preprocessor``."""

    def p(self, text, fallback=False):
        from wheezy.html.ext.mako import inline_preprocessor

        p = inline_preprocessor(directories=["."], fallback=fallback)
        return p(text)

    def test_inline(self):
        assert self.p('<%inline file="LICENSE" />')

    def test_inline_fallback(self):
        assert '<%include file="LICENSE"/>' == self.p(
            '<%inline file="LICENSE" />', fallback=True
        )

    def test_inline_not_found(self):
        import warnings

        warnings.simplefilter("ignore")
        assert not self.p('<%inline file="X" />')
        warnings.simplefilter("default")


try:
    # from mako.template import Template
    Template = __import__("mako.template", None, None, ["Template"]).Template
    from wheezy.html.ext.mako import widget_preprocessor

    def assert_mako_equal(text, expected, **kwargs):
        template = Template(text, preprocessor=[widget_preprocessor])
        value = template.render(**kwargs)
        assert expected == value

except ImportError:  # pragma: nocover

    def assert_mako_equal(text, expected, **kwargs):  # noqa
        pass
