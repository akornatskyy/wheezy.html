
""" Unit tests for ``wheezy.html.ext.lexer``.
"""

import unittest


class PreprocessorInitTestCase(unittest.TestCase):
    """ Test the ``Preprocessor.__init__``.
    """

    def test_assert_widgets_placeholder(self):
        """ Assert widgets pattern has a placeholder for supported
            widgets.
        """
        from wheezy.html.ext.lexer import Preprocessor
        self.assertRaises(AssertionError, lambda: Preprocessor(''))

    def test_widgets(self):
        """ Ensure widgets supported.
        """
        from wheezy.html.ext.lexer import Preprocessor
        p = Preprocessor('%(widgets)s')
        assert 17 == len(p.widgets)
        assert 'checkbox|dropdown|emptybox|error|hidden|info|'\
                'label|listbox|multiple_checkbox|multiple_hidden|'\
                'multiple_select|password|radio|select|textarea|'\
                'textbox|warning' == p.RE_WIDGETS.pattern


class PreprocessorHelpersTestCase(unittest.TestCase):
    """ Test the ``Preprocessor`` helpers.
    """

    def setUp(self):
        from wheezy.html.ext.lexer import Preprocessor
        self.p = Preprocessor('%(widgets)s')

    def test_expression(self):
        """ Expression distinguish text, number and python object access.
            Python object access is filtered.
        """
        self.p.EXPRESSION = '%(expr)s|%(expr_filter)s'

        assert 'text' == self.p.expression('"text"')
        assert '100' == self.p.expression('100')
        assert 'user.name|filter' == self.p.expression('user.name', 'filter')

    def test_join_attrs(self):
        """ Ensure HTML attributes are joined correctly.
        """
        assert '' == self.p.join_attrs({})

        self.p.EXPRESSION = '%(expr)s%(expr_filter)s'
        assert ' autocomplete="off" disabled="${disabled}" ' \
                'maxlength="100"' == self.p.join_attrs({
                'autocomplete': 'off',
                'maxlength': '100',
                'disabled': '${disabled}'})

    def test_error_class_no_class(self):
        """ Substitute ``name`` in case ``class_`` is undefined.
        """
        self.p.ERROR_CLASS0 = '=%(name)s='
        assert '=x=' == self.p.error_class('x', class_='')

    def test_error_class(self):
        """ Substitute ``name`` and ``class`` in case ``class_``
            is defined.
        """
        self.p.ERROR_CLASS1 = '=%(name)s %(class)s='
        assert '=x c=' == self.p.error_class('x', class_='"c"')


class PreprocessorWidgetsTestCase(unittest.TestCase):
    """ Test the ``Preprocessor`` widgets.
    """

    def setUp(self):
        from wheezy.html.ext.lexer import Preprocessor
        self.p = Preprocessor('%(widgets)s')
        self.p.EXPRESSION = '%(expr)s%(expr_filter)s'
        self.p.ERROR_CLASS1 = '%(name)s %(class)s'

    def test_hidden(self):
        """ hidden widget
        """
        self.p.HIDDEN = '%(name)s %(value)s'
        assert 'pref model.pref|f' == self.p.hidden(
                'model.pref', None, '|f')

    def test_multiple_hidden(self):
        """ multiple_hidden widget
        """
        self.p.MULTIPLE_HIDDEN = '%(name)s %(value)s%(expr_filter)s'
        assert 'prefs model.prefs|f' == self.p.multiple_hidden(
                'model.prefs', None, '|f')

    def test_label(self):
        """ label widget
        """
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
        """ == self.p.label('model.user_name',
                '"User:", class="x", autocomplete="off"', '|f')

    def test_emptybox(self):
        """ emptybox widget
        """
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
        """ == self.p.emptybox('model.user_name',
                'class="x", autocomplete="off"', '|f')

    def test_textbox(self):
        """ textbox widget
        """
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
        """ == self.p.textbox('model.user_name',
                'class="x", autocomplete="off"', '|f')

    def test_password(self):
        """ password widget
        """
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
        """ == self.p.password('model.user_pwd',
                'class="x", autocomplete="off"', '|f')

    def test_textarea(self):
        """ textarea widget
        """
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
            attrs =  autocomplete="off" rows="9" cols="40"
            class = comment x
        """ == self.p.textarea('model.comment',
                'class="x", autocomplete="off"', '|f')

    def test_checkbox(self):
        """ checkbox widget
        """
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
        """ == self.p.checkbox('model.accepts',
                'class="x", autocomplete="off"', '|f')

    def test_multiple_checkbox(self):
        """ multiple_checkbox widget
        """
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
        """ == self.p.multiple_checkbox('model.colors',
                'class="x", cursor="auto", choices=${lst}', '|f')

    def test_radio(self):
        """ radio widget
        """
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
        """ == self.p.radio('model.yes_no',
                'class="x", cursor="auto", choices=${lst}', '|f')

    def test_dropdown(self):
        """ dropdown widget
        """
        self.p.SELECT = """
            id = %(id)s
            name = %(name)s
            select_type = |%(select_type)s|
            choices = %(choices)s
            value = %(value)s
            expr_filter = %(expr_filter)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = security-question
            name = security_question
            select_type = ||
            choices = ${lst}
            value = model.security_question
            expr_filter = |f
            attrs =  cursor="auto"
            class = security_question x
        """ == self.p.dropdown('model.security_question',
                'class="x", cursor="auto", choices=${lst}', '|f')

    def test_listbox(self):
        """ listbox widget
        """
        self.p.SELECT = """
            id = %(id)s
            name = %(name)s
            select_type = %(select_type)s
            choices = %(choices)s
            value = %(value)s
            expr_filter = %(expr_filter)s
            attrs = %(attrs)s
            class = %(class)s
        """
        assert """
            id = languages
            name = languages
            select_type =  multiple="multiple"
            choices = ${lst}
            value = model.languages
            expr_filter = |f
            attrs =  cursor="auto"
            class = languages x
        """ == self.p.listbox('model.languages',
                'class="x", cursor="auto", choices=${lst}', '|f')

    def test_error(self):
        """ error widget
        """
        self.p.ERROR = """
            name = %(name)s
            attrs = %(attrs)s
            expr_filter = %(expr_filter)s
        """
        assert """
            name = user_name
            attrs =  cursor="auto" class="error"
            expr_filter = |f
        """ == self.p.error('model.user_name',
                'cursor="auto"', '|f')
        assert """
            name = user_name
            attrs =  cursor="auto" class="error x"
            expr_filter = |f
        """ == self.p.error('model.user_name',
                'class="x", cursor="auto"', '|f')
        assert """
            name = __ERROR__
            attrs =  cursor="auto" class="error-message"
            expr_filter = |f
        """ == self.p.error('model',
                'cursor="auto"', '|f')
        assert """
            name = __ERROR__
            attrs =  cursor="auto" class="error-message x"
            expr_filter = |f
        """ == self.p.error('model',
                'class="x", cursor="auto"', '|f')

    def test_info(self):
        """ info widget
        """
        self.p.MESSAGE = """
            value = %(value)s
            info = %(info)s
            attrs = %(attrs)s
        """
        assert """
            value = model.username
            info = model.username|f
            attrs =  cursor="auto" class="info"
        """ == self.p.info('model.username', 'cursor="auto"', '|f')
        assert """
            value = model.username
            info = model.username|f
            attrs =  cursor="auto" class="info x"
        """ == self.p.info('model.username', 'class="x", cursor="auto"', '|f')
        assert """
            value = model
            info = model|f
            attrs =  cursor="auto" class="info-message"
        """ == self.p.info('model', 'cursor="auto"', '|f')
        assert """
            value = model
            info = model|f
            attrs =  cursor="auto" class="info-message x"
        """ == self.p.info('model', 'class="x", cursor="auto"', '|f')

    def test_warning(self):
        """ warning widget
        """
        self.p.MESSAGE = """
            value = %(value)s
            info = %(info)s
            attrs = %(attrs)s
        """
        assert """
            value = model.username
            info = model.username|f
            attrs =  cursor="auto" class="warning"
        """ == self.p.warning('model.username', 'cursor="auto"', '|f')
        assert """
            value = model.username
            info = model.username|f
            attrs =  cursor="auto" class="warning x"
        """ == self.p.warning('model.username',
                'class="x", cursor="auto"', '|f')
        assert """
            value = model
            info = model|f
            attrs =  cursor="auto" class="warning-message"
        """ == self.p.warning('model', 'cursor="auto"', '|f')
        assert """
            value = model
            info = model|f
            attrs =  cursor="auto" class="warning-message x"
        """ == self.p.warning('model', 'class="x", cursor="auto"', '|f')
