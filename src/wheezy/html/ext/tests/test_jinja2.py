
""" Unit tests for ``wheezy.html.ext.jinja2``.
"""

import unittest

from wheezy.html.ext.tests.test_lexer import PreprocessorMixin


class Jinja2PreprocessorTestCase(PreprocessorMixin, unittest.TestCase):
    """ Test the ``Jinja2Preprocessor``.
    """

    WHITE_SPACE_PATTERNS = ['%(w)s', ' %(w)s', '%(w)s ', ' %(w)s ']

    def assert_render_equal(self, template, expected, **kwargs):
        assert_jinja2_equal({
            'variable_start_string': '{{',
            'variable_end_string': '}}'
        }, template, expected, **kwargs)

    HIDDEN = '{{ model.pref.hidden()|e }}'
    MULTIPLE_HIDDEN = '{{ model.prefs.multiple_hidden() }}'
    LABEL = "{{ model.username.label('<i>*</i>Username:') }}"
    EMPTYBOX = "{{ model.amount.emptybox(class_='x')|e }}"
    TEXTBOX = "{{ model.username.textbox(autocomplete='off')|e }}"
    PASSWORD = "{{ model.pwd.password()|e }}"
    TEXTAREA = "{{ model.comment.textarea()|e }}"
    CHECKBOX = "{{ model.remember_me.checkbox() }}"
    MULTIPLE_CHECKBOX = "{{ model.scm.multiple_checkbox(choices=scm) }}"
    RADIO = "{{ model.scm.radio(choices=scm) }}"
    DROPDOWN = "{{ model.scm.dropdown(choices=scm) }}"
    LISTBOX = "{{ model.scm.listbox(choices=scm, class_='x') }}"
    ERROR = "{{ model.username.error() }}"
    GENERAL_ERROR = "{{ model.error() }}"
    INFO = "{{ model.user_info.info() }}"
    GENERAL_INFO = "{{ message.info()|e }}"
    WARNING = "{{ model.user_info.warning() }}"
    GENERAL_WARNING = "{{ message.warning()|e }}"


class Jinja2PreprocessorTestCase2(PreprocessorMixin, unittest.TestCase):
    """ Test the ``Jinja2Preprocessor``.
    """

    WHITE_SPACE_PATTERNS = ['%(w)s', ' %(w)s', '%(w)s ', ' %(w)s ']

    def assert_render_equal(self, template, expected, **kwargs):
        assert_jinja2_equal({
            'variable_start_string': '${',
            'variable_end_string': '}'
        }, template, expected, **kwargs)

    HIDDEN = '${model.pref.hidden()|e}'
    MULTIPLE_HIDDEN = '${model.prefs.multiple_hidden()}'
    LABEL = "${model.username.label('<i>*</i>Username:')}"
    EMPTYBOX = "${model.amount.emptybox(class_='x')|e}"
    TEXTBOX = "${model.username.textbox(autocomplete='off')|e}"
    PASSWORD = "${model.pwd.password()|e}"
    TEXTAREA = "${model.comment.textarea()|e}"
    CHECKBOX = "${model.remember_me.checkbox()}"
    MULTIPLE_CHECKBOX = "${model.scm.multiple_checkbox(choices=scm)}"
    RADIO = "${model.scm.radio(choices=scm)}"
    DROPDOWN = "${model.scm.dropdown(choices=scm)}"
    LISTBOX = "${model.scm.listbox(choices=scm, class_='x')}"
    ERROR = "${model.username.error()}"
    GENERAL_ERROR = "${model.error()}"
    INFO = "${model.user_info.info()}"
    GENERAL_INFO = "${message.info()|e}"
    WARNING = "${model.user_info.warning()}"
    GENERAL_WARNING = "${message.warning()|e}"


class Jinja2WhitespaceExtensionTestCase(unittest.TestCase):
    """ Test the ``WhitespaceExtension``.
    """

    block_start_string = '{%'
    block_end_string = '%}'

    def setUp(self):
        from wheezy.html.ext.jinja2 import WhitespaceExtension
        extension = WhitespaceExtension(self)
        self.preprocess = lambda s: extension.preprocess(s, None)

    def test_whitespace(self):
        """
        """
        assert ' x' == self.preprocess(' x')
        assert 'x' == self.preprocess('  \n x \n  ')
        assert 'x' == self.preprocess('  x')
        assert 'x' == self.preprocess('x  ')
        assert '><' == self.preprocess('  > < ')
        assert '>' + self.block_start_string == self.preprocess(
            '>  ' + self.block_start_string)
        assert self.block_end_string + '<' == self.preprocess(
            self.block_end_string + '  <')


class Jinja2WhitespaceExtensionTestCase2(Jinja2WhitespaceExtensionTestCase):
    """ Test the ``WhitespaceExtension``.
    """

    block_start_string = '<%'
    block_end_string = '%>'


try:
    # from jinja2 import Environment
    Environment = __import__('jinja2', None, None,
                             ['Environment']).Environment
    from wheezy.html.ext.jinja2 import WidgetExtension

    def assert_jinja2_equal(options, text, expected, **kwargs):
        template = Environment(
            extensions=[WidgetExtension],
            **options
        ).from_string(text)
        value = template.render(kwargs)
        assert expected == value

except ImportError:  # pragma: nocover

    def assert_jinja2_equal(text, expected, **kwargs):  # noqa
        pass
