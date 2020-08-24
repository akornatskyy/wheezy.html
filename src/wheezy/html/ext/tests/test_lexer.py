""" Unit tests for ``wheezy.html.ext.lexer``.
"""

import unittest


def generate_white_space_patterns():  # pragma: nocover
    for t in ["x", " x", "x ", " x ", "[ x", "x ]", "[ x ]", "xx", "x x"]:
        for s in [" ", "\t", "\n", " \t", " \n", "\n "]:
            for n in [1, 3]:
                yield t.replace(" ", s * n).replace("x", "%(w)s")


class PreprocessorInitTestCase(unittest.TestCase):
    """Test the ``Preprocessor.__init__``."""

    def test_assert_widgets_placeholder(self):
        """Assert widgets pattern has a placeholder for supported
        widgets.
        """
        from wheezy.html.ext.lexer import Preprocessor

        self.assertRaises(AssertionError, lambda: Preprocessor(""))

    def test_widgets(self):
        """Ensure widgets supported."""
        from wheezy.html.ext.lexer import Preprocessor

        p = Preprocessor("%(widgets)s")
        assert 17 == len(p.widgets)
        assert (
            "checkbox|dropdown|emptybox|error|hidden|info|"
            "label|listbox|multiple_checkbox|multiple_hidden|"
            "multiple_select|password|radio|select|textarea|"
            "textbox|warning"
            == "|".join(sorted(p.RE_WIDGETS.pattern.split("|")))
        )


class PreprocessorHelpersTestCase(unittest.TestCase):
    """Test the ``Preprocessor`` helpers."""

    def setUp(self):
        from wheezy.html.ext.lexer import Preprocessor

        self.p = Preprocessor("%(widgets)s")

    def test_expression(self):
        """Expression distinguish text, number and python object access.
        Python object access is filtered.
        """
        self.p.EXPRESSION = "%(expr)s|%(expr_filter)s"

        assert "text" == self.p.expression('"text"')
        assert "100" == self.p.expression("100")
        assert "user.name|filter" == self.p.expression("user.name", "filter")

    def test_join_attrs(self):
        """Ensure HTML attributes are joined correctly."""
        assert "" == self.p.join_attrs({})

        self.p.EXPRESSION = "%(expr)s%(expr_filter)s"
        assert (
            ' autocomplete="off" disabled="${disabled}" '
            'maxlength="100"'
            == self.p.join_attrs(
                {
                    "autocomplete": "off",
                    "maxlength": "100",
                    "disabled": "${disabled}",
                }
            )
        )

    def test_error_class_no_class(self):
        """Substitute ``name`` in case ``class_`` is undefined."""
        self.p.ERROR_CLASS0 = "=%(name)s="
        assert "=x=" == self.p.error_class("x", class_="")

    def test_error_class(self):
        """Substitute ``name`` and ``class`` in case ``class_``
        is defined.
        """
        self.p.ERROR_CLASS1 = "=%(name)s %(class)s="
        assert "=x c=" == self.p.error_class("x", class_='"c"')


class PreprocessorWidgetsTestCase(unittest.TestCase):
    """Test the ``Preprocessor`` widgets."""

    def setUp(self):
        from wheezy.html.ext.lexer import Preprocessor

        self.p = Preprocessor("%(widgets)s")
        self.p.EXPRESSION = "%(expr)s%(expr_filter)s"
        self.p.ERROR_CLASS1 = "%(name)s %(class)s"

    def test_hidden(self):
        """hidden widget"""
        self.p.HIDDEN = "%(name)s %(value)s"
        assert "pref model.pref|f" == self.p.hidden("model.pref", None, "|f")

    def test_multiple_hidden(self):
        """multiple_hidden widget"""
        self.p.MULTIPLE_HIDDEN = "%(name)s %(value)s%(expr_filter)s"
        assert "prefs model.prefs|f" == self.p.multiple_hidden(
            "model.prefs", None, "|f"
        )

    def test_label(self):
        """label widget"""
        self.p.LABEL = """
            id = %(id)s
            name = %(name)s
            value = %(value)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = user-name
            name = user_name
            value = User:
            attrs =  autocomplete="off"
            class = user_name x
        """ == self.p.label(
            "model.user_name", '"User:", class="x", autocomplete="off"', "|f"
        )

    def test_emptybox(self):
        """emptybox widget"""
        self.p.INPUT = """
            id = %(id)s
            name = %(name)s
            type = %(type)s
            value = %(value)s
            condition = |%(condition)s|
            func = %(func)s
            expr_filter = %(expr_filter)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = user-name
            name = user_name
            type = text
            value = model.user_name
            condition = ||
            func = model.user_name
            expr_filter = |f
            attrs =  autocomplete="off"
            class = user_name x
        """ == self.p.emptybox(
            "model.user_name", 'class="x", autocomplete="off"', "|f"
        )

    def test_textbox(self):
        """textbox widget"""
        self.p.INPUT = """
            id = %(id)s
            name = %(name)s
            type = %(type)s
            value = %(value)s
            condition = |%(condition)s|
            func = %(func)s
            expr_filter = %(expr_filter)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = user-name
            name = user_name
            type = text
            value = model.user_name
            condition = | not in (None, '')|
            func = model.user_name
            expr_filter = |f
            attrs =  autocomplete="off"
            class = user_name x
        """ == self.p.textbox(
            "model.user_name", 'class="x", autocomplete="off"', "|f"
        )

    def test_password(self):
        """password widget"""
        self.p.INPUT = """
            id = %(id)s
            name = %(name)s
            type = %(type)s
            value = %(value)s
            condition = |%(condition)s|
            func = %(func)s
            expr_filter = %(expr_filter)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = user-pwd
            name = user_pwd
            type = password
            value = model.user_pwd
            condition = | not in (None, '')|
            func = model.user_pwd
            expr_filter = |f
            attrs =  autocomplete="off"
            class = user_pwd x
        """ == self.p.password(
            "model.user_pwd", 'class="x", autocomplete="off"', "|f"
        )

    def test_textarea(self):
        """textarea widget"""
        self.p.TEXTAREA = """
            id = %(id)s
            name = %(name)s
            value = %(value)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = comment
            name = comment
            value = model.comment|f
            attrs =  autocomplete="off" cols="40" rows="9"
            class = comment x
        """ == self.p.textarea(
            "model.comment", 'class="x", autocomplete="off"', "|f"
        )

    def test_checkbox(self):
        """checkbox widget"""
        self.p.CHECKBOX = """
            id = %(id)s
            name = %(name)s
            value = %(value)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = accepts
            name = accepts
            value = model.accepts
            attrs =  autocomplete="off"
            class = accepts x
        """ == self.p.checkbox(
            "model.accepts", 'class="x", autocomplete="off"', "|f"
        )

    def test_multiple_checkbox(self):
        """multiple_checkbox widget"""
        self.p.MULTIPLE_CHECKBOX = """
            id = %(id)s
            name = %(name)s
            choices = %(choices)s
            value = %(value)s
            expr_filter = %(expr_filter)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = colors
            name = colors
            choices = ${lst}
            value = model.colors
            expr_filter = |f
            attrs =  cursor="auto"
            class = colors x
        """ == self.p.multiple_checkbox(
            "model.colors", 'class="x", cursor="auto", choices=${lst}', "|f"
        )

    def test_radio(self):
        """radio widget"""
        self.p.RADIO = """
            id = %(id)s
            name = %(name)s
            choices = %(choices)s
            value = %(value)s
            expr_filter = %(expr_filter)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = yes-no
            name = yes_no
            choices = ${lst}
            value = model.yes_no
            expr_filter = |f
            attrs =  cursor="auto"
            class = yes_no x
        """ == self.p.radio(
            "model.yes_no", 'class="x", cursor="auto", choices=${lst}', "|f"
        )

    def test_dropdown(self):
        """dropdown widget"""
        self.p.SELECT = """
            id = %(id)s
            name = %(name)s
            choices = %(choices)s
            value = %(value)s
            expr_filter = %(expr_filter)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = security-question
            name = security_question
            choices = ${lst}
            value = model.security_question
            expr_filter = |f
            attrs =  cursor="auto"
            class = security_question x
        """ == self.p.dropdown(
            "model.security_question",
            'class="x", cursor="auto", choices=${lst}',
            "|f",
        )

    def test_listbox(self):
        """listbox widget"""
        self.p.MULTIPLE_SELECT = """
            id = %(id)s
            name = %(name)s
            choices = %(choices)s
            value = %(value)s
            expr_filter = %(expr_filter)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = languages
            name = languages
            choices = ${lst}
            value = model.languages
            expr_filter = |f
            attrs =  cursor="auto"
            class = languages x
        """ == self.p.listbox(
            "model.languages", 'class="x", cursor="auto", choices=${lst}', "|f"
        )

    def test_error(self):
        """error widget"""
        self.p.ERROR = """
            name = %(name)s
            attrs = %(attrs)s
            expr_filter = %(expr_filter)s
        """
        assert """
            name = user_name
            attrs =  class="error" cursor="auto"
            expr_filter = |f
        """ == self.p.error(
            "model.user_name", 'cursor="auto"', "|f"
        )
        assert """
            name = user_name
            attrs =  class="error x" cursor="auto"
            expr_filter = |f
        """ == self.p.error(
            "model.user_name", 'class="x", cursor="auto"', "|f"
        )
        assert """
            name = __ERROR__
            attrs =  class="error-message" cursor="auto"
            expr_filter = |f
        """ == self.p.error(
            "model", 'cursor="auto"', "|f"
        )
        assert """
            name = __ERROR__
            attrs =  class="error-message x" cursor="auto"
            expr_filter = |f
        """ == self.p.error(
            "model", 'class="x", cursor="auto"', "|f"
        )

    def test_info(self):
        """info widget"""
        self.p.MESSAGE = """
            value = %(value)s
            info = %(info)s
            attrs = %(attrs)s
        """
        assert """
            value = model.username
            info = model.username|f
            attrs =  class="info" cursor="auto"
        """ == self.p.info(
            "model.username", 'cursor="auto"', "|f"
        )
        assert """
            value = model.username
            info = model.username|f
            attrs =  class="info x" cursor="auto"
        """ == self.p.info(
            "model.username", 'class="x", cursor="auto"', "|f"
        )
        assert """
            value = model
            info = model|f
            attrs =  class="info-message" cursor="auto"
        """ == self.p.info(
            "model", 'cursor="auto"', "|f"
        )
        assert """
            value = model
            info = model|f
            attrs =  class="info-message x" cursor="auto"
        """ == self.p.info(
            "model", 'class="x", cursor="auto"', "|f"
        )

    def test_warning(self):
        """warning widget"""
        self.p.MESSAGE = """
            value = %(value)s
            info = %(info)s
            attrs = %(attrs)s
        """
        assert """
            value = model.username
            info = model.username|f
            attrs =  class="warning" cursor="auto"
        """ == self.p.warning(
            "model.username", 'cursor="auto"', "|f"
        )
        assert """
            value = model.username
            info = model.username|f
            attrs =  class="warning x" cursor="auto"
        """ == self.p.warning(
            "model.username", 'class="x", cursor="auto"', "|f"
        )
        assert """
            value = model
            info = model|f
            attrs =  class="warning-message" cursor="auto"
        """ == self.p.warning(
            "model", 'cursor="auto"', "|f"
        )
        assert """
            value = model
            info = model|f
            attrs =  class="warning-message x" cursor="auto"
        """ == self.p.warning(
            "model", 'class="x", cursor="auto"', "|f"
        )


class PreprocessorMixin(object):
    """Test the ``Preprocessor``."""

    from operator import itemgetter

    WHITE_SPACE_PATTERNS = ["%(w)s"]

    class Dummy(object):
        pass

    scm = sorted(
        {"git": "Git", "hg": "Mercurial", "svn": "SVN"}.items(),
        key=itemgetter(1),
    )

    def setUp(self):
        self.m = PreprocessorMixin.Dummy()
        self.e = {}

    def assert_render_equal(self, template, expected, **kwargs):
        pass  # pragma: nocover

    def render(self, widget, html):
        """hidden widget."""
        for wsp in self.WHITE_SPACE_PATTERNS:
            self.assert_render_equal(
                wsp % {"w": widget},
                wsp % {"w": html},
                model=self.m,
                errors=self.e,
                scm=self.scm,
                message=(hasattr(self.m, "message") and self.m.message or ""),
            )

    def test_hidden(self):
        """hidden widget."""
        self.m.pref = "ab<c>"
        self.render(
            self.HIDDEN,
            '<input type="hidden" name="pref" value="ab&lt;c&gt;" />',
        )

    def test_multiple_hidden(self):
        """multiple_hidden widget."""
        self.m.prefs = ["a", "b"]
        self.render(
            self.MULTIPLE_HIDDEN,
            '<input type="hidden" name="prefs" value="a" />'
            '<input type="hidden" name="prefs" value="b" />',
        )

    def test_label(self):
        """label widget."""
        self.m.username = ""
        self.render(
            self.LABEL, '<label for="username"><i>*</i>Username:</label>'
        )
        self.e["username"] = "Error"
        self.render(
            self.LABEL,
            '<label for="username" class="error">' "<i>*</i>Username:</label>",
        )

    def test_emptybox(self):
        """emptybox widget."""
        self.m.amount = 10
        self.render(
            self.EMPTYBOX,
            '<input id="amount" name="amount" type="text" class="x" '
            'value="10" />',
        )
        self.m.amount = 0
        self.render(
            self.EMPTYBOX,
            '<input id="amount" name="amount" type="text" class="x" />',
        )
        self.e["amount"] = "Error"
        self.render(
            self.EMPTYBOX,
            '<input id="amount" name="amount" type="text"'
            ' class="error x" />',
        )

    def test_textbox(self):
        """textbox widget."""
        self.m.username = "John"
        self.render(
            self.TEXTBOX,
            '<input id="username" name="username" type="text" '
            'autocomplete="off" value="John" />',
        )
        self.m.username = ""
        self.render(
            self.TEXTBOX,
            '<input id="username" name="username" type="text" '
            'autocomplete="off" />',
        )
        self.e["username"] = "Error"
        self.render(
            self.TEXTBOX,
            '<input id="username" name="username" type="text" '
            'autocomplete="off" class="error" />',
        )

    def test_password(self):
        """password widget."""
        self.m.pwd = ""
        self.render(
            self.PASSWORD, '<input id="pwd" name="pwd" type="password" />'
        )
        self.e["pwd"] = "Error"
        self.render(
            self.PASSWORD,
            '<input id="pwd" name="pwd" type="password" class="error" />',
        )

    def test_textarea(self):
        """textarea widget."""
        self.m.comment = "x"
        self.render(
            self.TEXTAREA,
            '<textarea id="comment" name="comment" '
            'cols="40" rows="9">x</textarea>',
        )
        self.e["comment"] = "Error"
        self.render(
            self.TEXTAREA,
            '<textarea id="comment" name="comment" '
            'cols="40" rows="9" class="error">x</textarea>',
        )

    def test_checkbox(self):
        """checkbox widget."""
        self.m.remember_me = True
        self.render(
            self.CHECKBOX,
            '<input id="remember-me" name="remember_me" '
            'type="checkbox" value="1" checked="checked" />',
        )
        self.m.remember_me = False
        self.render(
            self.CHECKBOX,
            '<input id="remember-me" name="remember_me" '
            'type="checkbox" value="1" />',
        )
        self.e["remember_me"] = "Error"
        self.render(
            self.CHECKBOX,
            '<input id="remember-me" name="remember_me" '
            'type="checkbox" value="1" class="error" />',
        )

    def test_multiple_checkbox(self):
        """multiple_checkbox widget."""
        self.m.scm = ["hg", "git"]
        self.render(
            self.MULTIPLE_CHECKBOX,
            '<label><input id="scm" name="scm" type="checkbox" '
            'value="1" checked="checked" />Git</label>'
            '<label><input id="scm" name="scm" type="checkbox" '
            'value="1" checked="checked" />Mercurial</label>'
            '<label><input id="scm" name="scm" type="checkbox" '
            'value="1" />SVN</label>',
        )
        self.m.scm = []
        self.render(
            self.MULTIPLE_CHECKBOX,
            '<label><input id="scm" name="scm" type="checkbox" '
            'value="1" />Git</label>'
            '<label><input id="scm" name="scm" type="checkbox" '
            'value="1" />Mercurial</label>'
            '<label><input id="scm" name="scm" type="checkbox" '
            'value="1" />SVN</label>',
        )
        self.e["scm"] = "Error"
        self.render(
            self.MULTIPLE_CHECKBOX,
            '<label class="error"><input id="scm" name="scm" '
            'type="checkbox" value="1" class="error" />Git</label>'
            '<label class="error"><input id="scm" name="scm" '
            'type="checkbox" value="1" class="error" />Mercurial</label>'
            '<label class="error"><input id="scm" name="scm" '
            'type="checkbox" value="1" class="error" />SVN</label>',
        )

    def test_radio(self):
        """radio widget."""
        self.m.scm = "hg"
        self.render(
            self.RADIO,
            '<label><input type="radio" name="scm" value="git" />'
            "Git</label>"
            '<label><input type="radio" name="scm" value="hg" '
            'checked="checked" />Mercurial</label>'
            '<label><input type="radio" name="scm" value="svn" />'
            "SVN</label>",
        )
        self.m.scm = ""
        self.render(
            self.RADIO,
            '<label><input type="radio" name="scm" value="git" />'
            "Git</label>"
            '<label><input type="radio" name="scm" value="hg" />'
            "Mercurial</label>"
            '<label><input type="radio" name="scm" value="svn" />'
            "SVN</label>",
        )
        self.e["scm"] = "Error"
        self.render(
            self.RADIO,
            '<label class="error"><input type="radio" name="scm" '
            'value="git" class="error" />Git</label>'
            '<label class="error"><input type="radio" name="scm" '
            'value="hg" class="error" />Mercurial</label>'
            '<label class="error"><input type="radio" name="scm" '
            'value="svn" class="error" />SVN</label>',
        )

    def test_dropdown(self):
        """dropdown widget."""
        self.m.scm = "hg"
        self.render(
            self.DROPDOWN,
            '<select id="scm" name="scm">'
            '<option value="git">Git</option>'
            '<option value="hg" selected="selected">Mercurial</option>'
            '<option value="svn">SVN</option>'
            "</select>",
        )
        self.m.scm = ""
        self.render(
            self.DROPDOWN,
            '<select id="scm" name="scm">'
            '<option value="git">Git</option>'
            '<option value="hg">Mercurial</option>'
            '<option value="svn">SVN</option>'
            "</select>",
        )
        self.e["scm"] = "Error"
        self.render(
            self.DROPDOWN,
            '<select id="scm" name="scm" class="error">'
            '<option value="git">Git</option>'
            '<option value="hg">Mercurial</option>'
            '<option value="svn">SVN</option>'
            "</select>",
        )

    def test_listbox(self):
        """listbox widget."""
        self.m.scm = ("hg", "svn")
        self.render(
            self.LISTBOX,
            '<select id="scm" name="scm" multiple="multiple" class="x">'
            '<option value="git">Git</option>'
            '<option value="hg" selected="selected">Mercurial</option>'
            '<option value="svn" selected="selected">SVN</option>'
            "</select>",
        )
        self.m.scm = []
        self.render(
            self.LISTBOX,
            '<select id="scm" name="scm" multiple="multiple" class="x">'
            '<option value="git">Git</option>'
            '<option value="hg">Mercurial</option>'
            '<option value="svn">SVN</option>'
            "</select>",
        )
        self.e["scm"] = "Error"
        self.render(
            self.LISTBOX,
            '<select id="scm" name="scm" multiple="multiple" '
            'class="error x">'
            '<option value="git">Git</option>'
            '<option value="hg">Mercurial</option>'
            '<option value="svn">SVN</option>'
            "</select>",
        )

    def test_attribute_error(self):
        """attribute error widget."""
        self.render(self.ERROR, "")
        self.e["username"] = ["Error1", "Error2"]
        self.render(self.ERROR, '<span class="error">Error2</span>')

    def test_general_error(self):
        """general error widget."""
        self.render(self.GENERAL_ERROR, "")
        self.e["__ERROR__"] = ["Error1", "Error2"]
        self.render(
            self.GENERAL_ERROR, '<span class="error-message">Error2</span>'
        )

    def test_attribute_info(self):
        """attribute info widget."""
        self.m.user_info = None
        self.render(self.INFO, "")
        self.m.user_info = "Info"
        self.render(self.INFO, '<span class="info">Info</span>')

    def test_general_info(self):
        """general info widget."""
        self.render(self.GENERAL_INFO, "")
        self.m.message = "Message"
        self.render(
            self.GENERAL_INFO, '<span class="info-message">Message</span>'
        )

    def test_attribute_warning(self):
        """attribute warning widget."""
        self.m.user_info = None
        self.render(self.WARNING, "")
        self.m.user_info = "Warn"
        self.render(self.WARNING, '<span class="warning">Warn</span>')

    def test_general_warning(self):
        """general warning widget."""
        self.render(self.GENERAL_WARNING, "")
        self.m.message = "Message"
        self.render(
            self.GENERAL_WARNING,
            '<span class="warning-message">Message</span>',
        )
