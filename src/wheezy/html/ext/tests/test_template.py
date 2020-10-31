""" Unit tests for ``wheezy.html.ext.mako``.
"""

import unittest

from wheezy.html.ext.tests.test_lexer import PreprocessorMixin


class TemplatePreprocessorTestCase(PreprocessorMixin, unittest.TestCase):
    """Test the ``MakoPreprocessor``."""

    def assert_render_equal(self, template, expected, **kwargs):
        assert_template_equal(template, expected, **kwargs)

    HIDDEN = "@model.pref.hidden()!h"
    MULTIPLE_HIDDEN = "@model.prefs.multiple_hidden()"
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
    """Test the ``WhitespaceExtension``."""

    def setUp(self):
        from wheezy.html.ext.template import (
            WhitespaceExtension,
            whitespace_preprocessor,
        )

        whitespace_preprocessor1 = WhitespaceExtension.preprocessors[0]
        self.preprocess = lambda text: whitespace_preprocessor(
            whitespace_preprocessor1(text)
        )

    def test_whitespace(self):
        """"""
        assert "><" == self.preprocess("  >  < ")
        assert ">\\\na" == self.preprocess("  >\n  a")
        assert "" == self.preprocess("  ")
        assert "x" == self.preprocess("  x")
        assert "x" == self.preprocess("x  ")
        assert "<code>\n 1\n 2 </code>" == self.preprocess(
            "  <code> \n 1 \n 2 </code> "
        )
        assert "<pre>\n </pre>" == self.preprocess("  <pre> \n </pre> ")

    def test_preserve_whitespace(self):
        # single space is preserved at the beginning of line
        assert " x" == self.preprocess(" x")
        assert "a\\\n b" == self.preprocess("a\n b")
        assert ">\\\n a" == self.preprocess(">\n a")
        # whitespace is preserved at the end of line
        assert "b  \\" == self.preprocess("  b  \\\n  ")
        assert "a \\\nb" == self.preprocess("  a \\\n  b  ")
        assert "a \\\nb" == self.preprocess("a\n  b")

    def test_postprocessor(self):
        from wheezy.html.ext.template import whitespace_postprocessor

        tokens = [("1", "markup", "  a")]
        whitespace_postprocessor(tokens)
        assert tokens == [("1", "markup", "a")]


class InlineExtensionTestCase(unittest.TestCase):
    """Test the ``InlineExtension``."""

    def p(self, text, fallback=False):
        from wheezy.html.ext.template import InlineExtension

        p = InlineExtension(searchpath=["."], fallback=fallback)
        p = p.preprocessors[0]
        return p(text)

    def test_inline(self):
        assert self.p('@inline("LICENSE")')

    def test_inline_fallback(self):
        assert '@include("LICENSE")' == self.p(
            '@inline("LICENSE")', fallback=True
        )

    def test_inline_not_found(self):
        import warnings

        warnings.simplefilter("ignore")
        assert not self.p('@inline("X")')
        warnings.simplefilter("default")


try:
    from wheezy.template.engine import Engine
    from wheezy.template.ext.core import CoreExtension
    from wheezy.template.loader import DictLoader

    from wheezy.html.ext.template import WidgetExtension
    from wheezy.html.utils import html_escape

    def assert_template_equal(text, expected, **kwargs):
        engine = Engine(
            loader=DictLoader(
                {"x": "@require(model, errors, message, scm)\n" + text}
            ),
            extensions=[CoreExtension(), WidgetExtension()],
        )
        engine.global_vars.update({"h": html_escape})
        value = engine.render("x", kwargs, {}, {})
        assert expected == value


except ImportError:  # pragma: nocover

    def assert_template_equal(text, expected, **kwargs):  # noqa
        pass
