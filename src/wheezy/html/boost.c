
#include <Python.h>

static PyObject*
escape_html_unicode(PyUnicodeObject *s)
{
    const Py_ssize_t s_size = PyUnicode_GET_SIZE(s);
    if (s_size == 0)
    {
        Py_INCREF(s);
        return (PyObject*)s;
    }

    Py_ssize_t count = 0;
    Py_UNICODE *start = PyUnicode_AS_UNICODE(s);
    const Py_UNICODE *end = start + s_size;
    Py_UNICODE *p = start;
    while(p < end)
    {
        switch(*p++)
        {
            case '<':
            case '>':
                count += 3; break;
            case '&':
                count += 4; break;
            case '"':
                count += 5; break;
            default:
                break;
        }
    }

    if (count == 0)
    {
        Py_INCREF(s);
        return (PyObject*)s;
    }

    PyObject *result = PyUnicode_FromUnicode(NULL, s_size + count);
    if (! result)
    {
        return NULL;
    }

    p = start;
    Py_UNICODE *r = PyUnicode_AS_UNICODE(result);
    while(p < end)
    {
        Py_UNICODE ch = *p++;
        switch(ch)
        {
            case '<':
                *r++ = '&'; *r++ = 'l'; *r++ = 't'; *r++ = ';';
                break;
            case '>':
                *r++ = '&'; *r++ = 'g'; *r++ = 't'; *r++ = ';';
                break;
            case '&':
                *r++ = '&'; *r++ = 'a'; *r++ = 'm'; *r++ = 'p';
                *r++ = ';';
                break;
            case '"':
                *r++ = '&'; *r++ = 'q'; *r++ = 'u'; *r++ = 'o';
                *r++ = 't'; *r++ = ';';
                break;
            default:
                *r++ = ch;
                break;
        }
    }

    return result;
}



static PyObject*
escape_html_string(PyObject *s)
{
    const Py_ssize_t s_size = PyBytes_GET_SIZE(s);
    if (s_size == 0)
    {
        Py_INCREF(s);
        return (PyObject*)s;
    }

    Py_ssize_t count = 0;
    char *start = PyBytes_AS_STRING(s);
    const char *end = start + s_size;
    char *p = start;
    while(p < end)
    {
        switch(*p++)
        {
            case '<':
            case '>':
                count += 3; break;
            case '&':
                count += 4; break;
            case '"':
                count += 5; break;
            default:
                break;
        }
    }

    if (count == 0)
    {
        Py_INCREF(s);
        return (PyObject*)s;
    }

    PyObject *result = PyBytes_FromStringAndSize(NULL, s_size + count);
    if (! result)
    {
        return NULL;
    }

    p = start;
    char *r = PyBytes_AS_STRING(result);
    while(p < end)
    {
        char ch = *p++;
        switch(ch)
        {
            case '<':
                *r++ = '&'; *r++ = 'l'; *r++ = 't'; *r++ = ';';
                break;
            case '>':
                *r++ = '&'; *r++ = 'g'; *r++ = 't'; *r++ = ';';
                break;
            case '&':
                *r++ = '&'; *r++ = 'a'; *r++ = 'm'; *r++ = 'p';
                *r++ = ';';
                break;
            case '"':
                *r++ = '&'; *r++ = 'q'; *r++ = 'u'; *r++ = 'o';
                *r++ = 't'; *r++ = ';';
                break;
            default:
                *r++ = ch;
                break;
        }
    }

    return result;
}


static PyObject*
escape_html(PyObject *self, PyObject *args)
{
    PyObject *s;
    if (! PyArg_ParseTuple(args, "O", &s))
    {
        return NULL;
    }

    if (PyUnicode_CheckExact(s))
    {
        return escape_html_unicode((PyUnicodeObject*)s);
    }

    if (PyBytes_CheckExact(s))
    {
        return escape_html_string(s);
    }

    if (s == Py_None) {
        return PyUnicode_FromStringAndSize(NULL, 0);
    }

    PyErr_Format(PyExc_TypeError,
                 "expected string or unicode object, %s found",
                 Py_TYPE(s)->tp_name);
    return NULL;
}


static PyMethodDef module_methods[] = {
    {"escape_html", escape_html, METH_VARARGS,
        "Escapes a string so it is valid within HTML."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static struct PyModuleDef module_definition = {
    PyModuleDef_HEAD_INIT,
	"wheezy.html.boost",
	NULL,
	-1,
	module_methods
};

PyMODINIT_FUNC
PyInit_boost(void)
{
	return PyModule_Create(&module_definition);
}
