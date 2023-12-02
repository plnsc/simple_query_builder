import unittest

from simple_query_builder.dialect import _Dialect


class TestDialect(unittest.TestCase):
    def setUp(self):
        self.dialect = _Dialect()

    def test_dialect_value(self):
        expected = "NULL"
        assert self.dialect.value('null') == expected

    def test_dialect_operator(self):
        expected = "<>"
        assert self.dialect.operator('not_equals') == expected

    def test_dialect_composed(self):
        expected = ['BETWEEN', 'AND']

        for idx, part in enumerate(expected):
            assert self.dialect.composed('between')[idx] == part

    def test_dialect_separator_0(self):
        expected = '1, 2, 3'
        assert self.dialect.separator('list', ['1', '2', '3']) == expected

    def test_dialect_separator_1(self):
        expected = 'CAN NOT BE MINIFIED'
        self.dialect._minified = True
        assert self.dialect.separator(
            'empty', ['CAN', 'NOT', 'BE', 'MINIFIED']) == expected

    def test_dialect_separator_2(self):
        expected = 'CANBEMINIFIED'
        self.dialect._minified = True
        assert self.dialect.separator(
            'empty', ['CAN', 'BE', 'MINIFIED'], True) == expected

    def test_dialect_statement(self):
        expected = ['SELECT', 'FROM', 'WHERE']
        assert self.dialect.statement('select') == expected

    def test_dialect_wrapper_0(self):
        expected = "'some value'"
        assert self.dialect.wrapper('string', 'some value') == expected

    def test_dialect_wrapper_1(self):
        expected = "some_identifier"
        assert self.dialect.wrapper(
            'identifier', 'some_identifier') == expected

    def test_dialect_sanitize_0(self):
        expected = "('value1', 'value2')"
        assert self.dialect.sanitize(['value1', 'value2']) == expected

    def test_dialect_sanitize_1(self):
        expected = "NULL"
        assert self.dialect.sanitize(None) == expected

    def test_dialect_sanitize_2(self):
        expected = "FALSE"
        assert self.dialect.sanitize(False) == expected

    def test_dialect_sanitize_3(self):
        expected = "13000"
        assert self.dialect.sanitize(13000) == expected
