
""" ``comp`` module.
"""

import sys


PY3 = sys.version_info[0] >= 3


if PY3:  # pragma: nocover
    str_type = str
    xrange = range
else:  # pragma: nocover
    str_type = unicode  # noqa: F821
    xrange = xrange


if PY3:  # pragma: nocover

    def iteritems(d):
        return d.items()
else:  # pragma: nocover

    def iteritems(d):
        return d.iteritems()  # noqa: B301
