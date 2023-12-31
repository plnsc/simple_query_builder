import unittest

from simple_query_builder import Filter, f


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.filter = Filter()

    def test_alias(self):
        expected_type = f()
        self.assertIsInstance(expected_type, Filter)

    def test_dump_parts(self):
        expected = ["a = b", "c LIKE d", "e <> f"]
        self.filter._parts = expected
        received = self.filter.dump_parts()
        self.assertEqual(received, " ".join(expected))

    def test_dump_globals(self):
        expected = "ORDER BY name LIMIT 10 OFFSET 0"
        self.filter._globals = {
            "order_by": ["ORDER BY", "name"],
            "limit": ["LIMIT", "10"],
            "offset": ["OFFSET", "0"],
        }
        received = self.filter.dump_globals()
        self.assertEqual(received, expected)

    def test_wrap_it_0(self):
        expected = "(something = 'some_value')"
        self.filter._parts = ["something", "=", "'some_value'"]
        self.filter.wrap_it()
        received = self.filter.dump_parts()
        self.assertEqual(received, expected)

    def test_wrap_it_1(self):
        expected = "some_bool = TRUE AND (something = 'some_value' AND something_else = 'some_value')"
        self.filter._parts = ["some_bool", "=", "TRUE"]
        nested = (Filter()
                  .add(Filter.equals("something", "some_value"))
                  .add_and(Filter.equals("something_else", "some_value"))
                  .wrap_it())
        self.filter.add_and(nested)
        received = self.filter.dump_parts()
        self.assertEqual(received, expected)

    def test_wrap_it_2(self):
        expected = "some_bool = TRUE OR (something = 'some_value' AND something_else = 'some_value')"
        self.filter._parts = ["some_bool", "=", "TRUE"]
        nested = (Filter()
                  .add(Filter.equals("something", "some_value"))
                  .add_and(Filter.equals("something_else", "some_value"))
                  .wrap_it())
        self.filter.add_or(nested)
        received = self.filter.dump_parts()
        self.assertEqual(received, expected)

    def test_add(self):
        expected = "something = 'some_value'"
        self.filter.add(Filter()
                        .add(Filter.equals("something", "some_value")))
        received = self.filter.dump_parts()
        self.assertEqual(received, expected)

    def test_add_and(self):
        expected = "something = 'some_value' AND something_else = 'some_value'"
        self.filter.add(Filter()
                        .add(Filter.equals("something", "some_value"))
                        .add_and(Filter.equals("something_else", "some_value")))
        received = self.filter.dump_parts()
        self.assertEqual(received, expected)

    def test_add_or(self):
        expected = "something = 'some_value' OR something_else = 'some_value'"
        self.filter.add(Filter()
                        .add(Filter.equals("something", "some_value"))
                        .add_or(Filter.equals("something_else", "some_value")))
        received = self.filter.dump_parts()
        self.assertEqual(received, expected)

    def test_order_by_0(self):
        expected = ["ORDER BY", "name ASC"]
        self.filter.order_by("name")
        for idx, part in enumerate(expected):
            self.assertEqual(self.filter._globals["order_by"][idx], part)
        received = self.filter.dump_globals()
        self.assertEqual(received, " ".join(expected))

    def test_order_by_1(self):
        expected = ["ORDER BY", "age DESC"]
        self.filter.order_by("age", -1)
        for idx, part in enumerate(expected):
            self.assertEqual(self.filter._globals["order_by"][idx], part)
        received = self.filter.dump_globals()
        self.assertEqual(received, " ".join(expected))

    def test_order_by_2(self):
        expected = ["ORDER BY", "name ASC, age DESC"]
        (self.filter
            .order_by("name")
            .order_by("age", -1))
        for idx, part in enumerate(expected):
            self.assertEqual(self.filter._globals["order_by"][idx], part)
        received = self.filter.dump_globals()
        self.assertEqual(received, " ".join(expected))

    def test_limit(self):
        expected = ["LIMIT", "10"]
        self.filter.limit(10)
        for idx, part in enumerate(expected):
            self.assertEqual(self.filter._globals["limit"][idx], part)
        received = self.filter.dump_globals()
        self.assertEqual(received, " ".join(expected))

    def test_offset(self):
        expected = ["OFFSET", "0"]
        self.filter.offset(0)
        for idx, part in enumerate(expected):
            self.assertEqual(self.filter._globals["offset"][idx], part)
        received = self.filter.dump_globals()
        self.assertEqual(received, " ".join(expected))

    def test_between(self):
        expected = "something BETWEEN 0 AND 100"
        filter = Filter.between("something", 0, 100)
        received = filter.dump_parts()
        self.assertEqual(received, expected)

    def test_equals(self):
        expected = "something = 'some_value'"
        filter = Filter.equals("something", "some_value")
        received = filter.dump_parts()
        self.assertEqual(received, expected)

    def test_not_equals(self):
        expected = "something <> 'some_value'"
        filter = Filter.not_equals("something", "some_value")
        received = filter.dump_parts()
        self.assertEqual(received, expected)

    def test_like(self):
        expected = "something LIKE '%some_value%'"
        filter = Filter.like("something", "%some_value%")
        received = filter.dump_parts()
        self.assertEqual(received, expected)

    def test_not_like(self):
        expected = "something NOT LIKE '%some_value%'"
        filter = Filter.not_like("something", "%some_value%")
        received = filter.dump_parts()
        self.assertEqual(received, expected)

    def test_lt(self):
        expected = "something < 1"
        filter = Filter.lt("something", 1)
        received = filter.dump_parts()
        self.assertEqual(received, expected)

    def test_lte(self):
        expected = "something <= 2"
        filter = Filter.lte("something", 2)
        received = filter.dump_parts()
        self.assertEqual(received, expected)

    def test_gt(self):
        expected = "something > 3"
        filter = Filter.gt("something", 3)
        received = filter.dump_parts()
        self.assertEqual(received, expected)

    def test_gte(self):
        expected = "something >= 4"
        filter = Filter.gte("something", 4)
        received = filter.dump_parts()
        self.assertEqual(received, expected)
