""" Unit tests for ``wheezy.html.utils``.
"""

import unittest


class EscapeHTMLMixin:
    def test_none(self):
        assert "" == self.escape(None)

    def test_empty(self):
        assert "" == self.escape("")

    def test_no_changes(self):
        assert "abc" == self.escape("abc")

    def test_escape(self):
        assert "&amp;&lt;&gt;&quot;'" == self.escape("&<>\"'")

    def test_type_error(self):
        self.assertRaises(TypeError, lambda: self.escape(1))


class NativeEscapeHTMLTestCase(unittest.TestCase, EscapeHTMLMixin):
    def setUp(self):
        from wheezy.html.utils import escape_html_native

        self.escape = escape_html_native


try:
    from wheezy.html.boost import escape_html

    class BoostEscapeHTMLTestCase(unittest.TestCase, EscapeHTMLMixin):
        def setUp(self):
            self.escape = escape_html

except ImportError:  # pragma: nocover
    pass
