import unittest

from simple_query_builder.dialect import _Dialect


class TestDialect(unittest.TestCase):
    def setUp(self):
        self.dialect = _Dialect()

    def test_value(self):
        expected = "NULL"
        received = self.dialect.value("null")
        self.assertEqual(received, expected)

    def test_operator(self):
        expected = "<>"
        received = self.dialect.operator("not_equals")
        self.assertEqual(received, expected)

    def test_composed(self):
        for idx, expected in enumerate(("BETWEEN", "AND")):
            self.assertEqual(self.dialect.composed("between")[idx], expected)

    def test_statement(self):
        expected = ("SELECT", "FROM", "WHERE")
        received = self.dialect.statement("select")
        self.assertEqual(received, expected)

    def test_separator_0(self):
        expected = "1, 2, 3"
        received = self.dialect.separator("list", ["1", "2", "3"])
        self.assertEqual(received, expected)

    def test_separator_1(self):
        expected = "CAN NOT BE MINIFIED"
        self.dialect._minified = True
        received = self.dialect.separator(
            "empty", ["CAN", "NOT", "BE", "MINIFIED"])
        self.assertEqual(received, expected)

    def test_separator_2(self):
        expected = "CANBEMINIFIED"
        self.dialect._minified = True
        received = (self.dialect.separator(
            "empty", ["CAN", "BE", "MINIFIED"], True))
        self.assertEqual(received, expected)

    def test_wrapper_0(self):
        expected = "'some value'"
        received = self.dialect.wrapper("string", "some value")
        self.assertEqual(received, expected)

    def test_wrapper_1(self):
        expected = "some_identifier"
        received = self.dialect.wrapper("identifier", "some_identifier")
        self.assertEqual(received, expected)

    def test_sanitize_0(self):
        expected = "('value1', 'value2')"
        received = self.dialect.sanitize(["value1", "value2"])
        self.assertEqual(received, expected)

    def test_sanitize_1(self):
        expected = "NULL"
        received = self.dialect.sanitize(None)
        self.assertEqual(received, expected)

    def test_sanitize_2(self):
        expected = "FALSE"
        received = self.dialect.sanitize(False)
        self.assertEqual(received, expected)

    def test_sanitize_3(self):
        expected = "13000"
        received = self.dialect.sanitize(13000)
        self.assertEqual(received, expected)
