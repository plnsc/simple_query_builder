import unittest

from simple_query_builder import Query, q


class TestQuery(unittest.TestCase):
    def setUp(self):
        self.query = Query()

    def test_query_alias(self):
        expected_type = q()
        assert type(expected_type) == type(self.query)

    def test_set_entity(self):
        expected = 'some_sql_table'

        query = Query(expected)

        assert query._entity == expected

    def test_get_entity(self):
        expected = 'some_other_sql_table'
        self.query._entity = expected

        assert self.query._get_entity() == expected

    def test_set_columns(self):
        columns = ['id', 'name', 'email']

        self.query.set_columns(columns)

        for idx, column in enumerate(columns):
            assert self.query._columns[idx] == column

    def test_set_row_0(self):
        expected = ['1', "'my name'", "'email@somehost'"]

        self.query.set_row([1, 'my name', 'email@somehost'])

        for idx, row in enumerate(expected):
            assert self.query._rows[0][idx] == row

    def test_set_row_1(self):
        expected_rows = [
            ['1', "'my name'", "'email@somehost'"],
            ['2', "'my other name'", "'other_email@somehost'"]
        ]

        self.query.set_row([1, 'my name', 'email@somehost'])
        self.query.set_row([2, 'my other name', 'other_email@somehost'])

        for row_idx, row in enumerate(self.query._rows):
            for idx, expected_row in enumerate(expected_rows[row_idx]):
                assert row[idx] == expected_row

    def test_set_0(self):
        expected_columns = ['id', 'name', 'email']
        expected_row = ['1', "'my name'", "'email@somehost'"]

        self.query.set({
            'id': 1,
            'name': 'my name',
            'email': 'email@somehost'
        })

        for idx, column in enumerate(expected_columns):
            assert self.query._columns[idx] == column

        for idx, row in enumerate(expected_row):
            assert self.query._rows[0][idx] == row

    def test_set_1(self):
        expected_columns = ['id', 'name', 'email']
        expected_rows = [
            ['1', "'my name'", "'email@somehost'"],
            ['2', "'my other name'", "'other_email@somehost'"]
        ]

        self.query.set({
            'id': 1,
            'name': 'my name',
            'email': 'email@somehost'
        })

        self.query.set({
            'id': 2,
            'name': 'my other name',
            'email': 'other_email@somehost'
        })

        for idx, column in enumerate(expected_columns):
            assert self.query._columns[idx] == column

        for row_idx, row in enumerate(self.query._rows):
            for idx, expected_row in enumerate(expected_rows[row_idx]):
                assert row[idx] == expected_row
