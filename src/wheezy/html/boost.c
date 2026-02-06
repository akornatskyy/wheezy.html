
#include <Python.h>

static PyObject*
escape_html_unicode(PyUnicodeObject *s)
{
    const Py_ssize_t s_size = PyUnicode_GET_LENGTH(s);
    if (s_size == 0)
    {
        Py_INCREF(s);
        return s;
    }

    int kind = PyUnicode_KIND(s);
    void *data = PyUnicode_DATA(s);
    Py_ssize_t count = 0;
    Py_UCS4 max_char = 0;

    for (Py_ssize_t i = 0; i < s_size; i++)
    {
        Py_UCS4 ch = PyUnicode_READ(kind, data, i);
        switch(ch)
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

        if (ch > max_char) {
            max_char = ch;
        }
    }

    if (count == 0)
    {
        Py_INCREF(s);
        return s;
    }

    PyObject *result = PyUnicode_New(s_size + count, max_char);
    if (!result)
    {
        return NULL;
    }

    int result_kind = PyUnicode_KIND(result);
    void *result_data = PyUnicode_DATA(result);
    Py_ssize_t pos = 0;

    if (kind == PyUnicode_1BYTE_KIND && max_char <= 127) {
        const Py_UCS1 *in = (Py_UCS1 *)data;
        Py_UCS1 *out = (Py_UCS1 *)result_data;

        for (Py_ssize_t i = 0; i < s_size; i++) {
            Py_UCS1 ch = in[i];
            switch(ch) {
                case '<':
                    out[pos++] = '&'; out[pos++] = 'l'; out[pos++] = 't';
                    out[pos++] = ';';
                    break;
                case '>':
                    out[pos++] = '&'; out[pos++] = 'g'; out[pos++] = 't';
                    out[pos++] = ';';
                    break;
                case '&':
                    out[pos++] = '&'; out[pos++] = 'a'; out[pos++] = 'm';
                    out[pos++] = 'p'; out[pos++] = ';';
                    break;
                case '"':
                    out[pos++] = '&'; out[pos++] = 'q'; out[pos++] = 'u';
                    out[pos++] = 'o'; out[pos++] = 't'; out[pos++] = ';';
                    break;
                default:
                    out[pos++] = ch;
                    break;
            }
        }
    }
    else {
        for (Py_ssize_t i = 0; i < s_size; i++) {
            Py_UCS4 ch = PyUnicode_READ(kind, data, i);
            switch (ch) {
                case '<':
                    PyUnicode_WRITE(result_kind, result_data, pos++, '&');
                    PyUnicode_WRITE(result_kind, result_data, pos++, 'l');
                    PyUnicode_WRITE(result_kind, result_data, pos++, 't');
                    PyUnicode_WRITE(result_kind, result_data, pos++, ';');
                    break;
                case '>':
                    PyUnicode_WRITE(result_kind, result_data, pos++, '&');
                    PyUnicode_WRITE(result_kind, result_data, pos++, 'g');
                    PyUnicode_WRITE(result_kind, result_data, pos++, 't');
                    PyUnicode_WRITE(result_kind, result_data, pos++, ';');
                    break;
                case '&':
                    PyUnicode_WRITE(result_kind, result_data, pos++, '&');
                    PyUnicode_WRITE(result_kind, result_data, pos++, 'a');
                    PyUnicode_WRITE(result_kind, result_data, pos++, 'm');
                    PyUnicode_WRITE(result_kind, result_data, pos++, 'p');
                    PyUnicode_WRITE(result_kind, result_data, pos++, ';');
                    break;
                case '"':
                    PyUnicode_WRITE(result_kind, result_data, pos++, '&');
                    PyUnicode_WRITE(result_kind, result_data, pos++, 'q');
                    PyUnicode_WRITE(result_kind, result_data, pos++, 'u');
                    PyUnicode_WRITE(result_kind, result_data, pos++, 'o');
                    PyUnicode_WRITE(result_kind, result_data, pos++, 't');
                    PyUnicode_WRITE(result_kind, result_data, pos++, ';');
                    break;
                default:
                    PyUnicode_WRITE(result_kind, result_data, pos++, ch);
                    break;
            }
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
        return escape_html_unicode(s);
    }

    if (PyBytes_CheckExact(s))
    {
        return escape_html_string(s);
    }

    if (s == Py_None) {
        return PyUnicode_FromStringAndSize(NULL, 0);
    }

    PyErr_Format(PyExc_TypeError,
                 "expected str or bytes, got %s",
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
