# -*- coding: utf-8 -*-

import unittest

from insanities.forms import *
from webob.multidict import MultiDict


def init_conv(conv, name='name', env=None):
    class f(Form):
        fields = [Field(name, conv)]
    return f(env or {}).get_field(name).conv


class ConverterTests(unittest.TestCase):

    def test_accept(self):
        'Accept method of converter'
        conv = init_conv(convs.Converter)
        value = conv.to_python('value')
        self.assertEqual(value, 'value')

    def test_to_python(self):
        'Converter to_python method'
        conv = init_conv(convs.Converter)
        value = conv.to_python('value')
        self.assertEqual(value, 'value')

    def test_from_python(self):
        'Converter from_python method'
        conv = init_conv(convs.Converter)
        value = conv.from_python('value')
        self.assertEqual(value, 'value')

    def test_error_template(self):
        'Converter `error_templates` attribute'
        conv = init_conv(convs.Converter)
        self.assertEqual(conv.error_templates.required, u'required field')

    def test_errors(self):
        'Converter `errors` attribute'
        conv = init_conv(convs.Converter(errors={'required': u'another message'}))
        self.assertEqual(conv.error_templates.required, u'another message')

    def test_env_errors(self):
        'Converter `env.errors`'
        conv = init_conv(convs.Converter, env={'error_templates': {'required': u'another message'}})
        self.assertEqual(conv.error_templates.required, u'another message')

    def test_raise_error(self):
        'Converter `raise_error` method'
        conv = init_conv(convs.Converter)
        self.assertRaises(convs.ValidationError, conv.raise_error, conv.error_templates.required)
        try:
            conv.raise_error(conv.error_templates.required)
        except convs.ValidationError, e:
            self.assertEqual(e.message, u'required field')

    def test_default_format_error(self):
        'Converter `raise_error` method and `format_error`'
        conv = init_conv(convs.Converter(errors={'halt': 'message %(location)s'}))
        self.assertRaises(convs.ValidationError, conv.raise_error, conv.error_templates.halt, location='here')
        try:
            conv.raise_error(conv.error_templates.halt, location='here')
        except convs.ValidationError, e:
            self.assertEqual(e.message, u'message here')

    def test_custom_format_error(self):
        'Converter custom `format_error`'
        conv = init_conv(convs.Converter, env={'format_error': (lambda *a, **kw: u'custom message')})
        self.assertRaises(convs.ValidationError, conv.raise_error, conv.error_templates.required)
        try:
            conv.raise_error(conv.error_templates.required)
        except convs.ValidationError, e:
            self.assertEqual(e.message, u'custom message')
        try:
            conv.raise_error(conv.error_templates.incorrect)
        except convs.ValidationError, e:
            self.assertEqual(e.message, u'custom message')

    def test_error_required(self):
        'Converter required=True error (lib is responsible for this error)'
        conv = init_conv(convs.Converter(required=True), name='field')
        form = conv.field.form
        conv.to_python('')
        self.assertEqual(form.errors, {'field': u'required field'})


class IntConverterTests(unittest.TestCase):

    def test_accept_valid(self):
        'Accept method of Int converter'
        conv = init_conv(convs.Int)
        value = conv.to_python('12')
        self.assertEqual(value, 12)

    def test_accept_null_value(self):
        'Accept method of Int converter for None value'
        conv = init_conv(convs.Int(required=False))
        value = conv.to_python('')
        self.assertEqual(value, None)

    def test_to_python(self):
        'Int Converter to_python method'
        conv = init_conv(convs.Int)
        value = conv.to_python('12')
        self.assertEqual(value, 12)

    def test_from_python(self):
        'Int Converter from_python method'
        conv = init_conv(convs.Int)
        value = conv.from_python(12)
        self.assertEqual(value, u'12')


class CharConverterTests(unittest.TestCase):

    def test_accept_valid(self):
        'Accept method of Char converter'
        conv = init_conv(convs.Char)
        value = conv.to_python('12')
        self.assertEqual(value, u'12')

    def test_accept_null_value(self):
        'Accept method of Char converter for None value'
        conv = init_conv(convs.Char(required=False))
        value = conv.to_python('')
        self.assertEqual(value, '')

    def test_to_python(self):
        'Char Converter to_python method'
        conv = init_conv(convs.Char)
        value = conv.to_python('12')
        self.assertEqual(value, u'12')

    def test_from_python(self):
        'Char Converter from_python method'
        conv = init_conv(convs.Char)
        value = conv.from_python(12)
        self.assertEqual(value, u'12')

class TestDate(unittest.TestCase):

    def test_accept_valid(self):
        '''Date converter to_python method'''
        from datetime import date
        conv = init_conv(convs.Date(format="%d.%m.%Y"))
        self.assertEqual(conv.to_python('31.01.1999'), date(1999, 1, 31))

    def test_readable_format(self):
        '''Ensure that readable format string for DateTime conv is generated correctly'''
        conv = convs.Date(format="%d.%m.%Y")()
        self.assertEqual(conv.readable_format, 'DD.MM.YYYY')

    def test_from_python(self):
        '''Date converter from_python method'''
        from datetime import date
        conv = init_conv(convs.Date(format="%d.%m.%Y"))
        self.assertEqual(conv.from_python(date(1999, 1, 31)), '31.01.1999')

    def test_from_python_pre_1900(self):
        # XXX move this tests to tests.utils.dt
        '''Test if from_python works fine with dates under 1900'''
        from datetime import date
        conv = init_conv(convs.Date(format="%d.%m.%Y"))
        self.assertEqual(conv.from_python(date(1899, 1, 31)), '31.01.1899')
        self.assertEqual(conv.from_python(date(401, 1, 31)), '31.01.401')

        conv = init_conv(convs.Date(format="%d.%m.%y"))
        # XXX is it right?
        self.assertEqual(conv.from_python(date(1899, 1, 31)), '31.01.99')
        self.assertEqual(conv.from_python(date(5, 1, 31)), '31.01.05')

class TestTime(unittest.TestCase):

    def test_from_python(self):
        '''Time converter from_python method'''
        from datetime import time
        conv = init_conv(convs.Time)
        self.assertEqual(conv.from_python(time(12, 30)), '12:30')

    def test_to_python(self):
        '''Time converter to_python method'''
        from datetime import time
        conv = init_conv(convs.Time)
        self.assertEqual(conv.to_python('12:30'), time(12, 30))

