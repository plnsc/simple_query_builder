import unittest

from simple_query_builder import Query, q


class TestQuery(unittest.TestCase):
    def setUp(self):
        self.query = Query()

    def test_query_alias(self):
        expected_type = q()
        assert type(expected_type) == type(self.query)
