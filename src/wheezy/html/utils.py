
""" ``utils`` module.
"""


def html_escape(s):
    """ Escapes a string so it is valid within HTML.

        >>> html_escape('abc')
        'abc'
        >>> html_escape('&<>"\\'')
        "&amp;&lt;&gt;&quot;\'"
    """
    return s.replace('&', '&amp;').replace('<', '&lt;'
            ).replace('>', '&gt;').replace('"', '&quot;')
