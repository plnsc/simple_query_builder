import unittest

from simple_query_builder import Filter, Query, q


class TestQuery(unittest.TestCase):
    def setUp(self):
        self.query = Query()

    def test_query_alias(self):
        expected_type = q()
        assert type(expected_type) == type(self.query)

    def test_query_set_statement(self):
        expected = 'insert'

        query = Query(expected)

        assert query._statement == expected

    def test_query_set_entity(self):
        expected = 'some_sql_table'

        self.query.entity(expected)

        assert self.query._entity == expected

    def test_query_set_filter(self):
        expected_filter = Filter()

        self.query.filter(expected_filter)

        assert self.query._filter is expected_filter

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

    def test_set_data_0(self):
        expected_columns = ['id', 'name', 'email']
        expected_row = ['1', "'my name'", "'email@somehost'"]

        self.query.set_data({
            'id': 1,
            'name': 'my name',
            'email': 'email@somehost'
        })

        for idx, column in enumerate(expected_columns):
            assert self.query._columns[idx] == column

        for idx, row in enumerate(expected_row):
            assert self.query._rows[0][idx] == row

    def test_set_data_1(self):
        expected_columns = ['id', 'name', 'email']
        expected_rows = [
            ['1', "'my name'", "'email@somehost'"],
            ['2', "'my other name'", "'other_email@somehost'"]
        ]

        self.query.set_data({
            'id': 1,
            'name': 'my name',
            'email': 'email@somehost'
        })

        self.query.set_data({
            'id': 2,
            'name': 'my other name',
            'email': 'other_email@somehost'
        })

        for idx, column in enumerate(expected_columns):
            assert self.query._columns[idx] == column

        for row_idx, row in enumerate(self.query._rows):
            for idx, expected_row in enumerate(expected_rows[row_idx]):
                assert row[idx] == expected_row

    def test_query_dump_insert_0(self):
        expected = ('INSERT INTO users (id, name, email) VALUES ' +
                    "(1, 'my name', 'email@somehost');")

        query = (Query('insert')
                 .entity('users')
                 .set_data({
                     'id': 1,
                     'name': 'my name',
                     'email': 'email@somehost'
                 }))

        assert query.dump_insert() == expected

    def test_query_dump_insert_1(self):
        expected = ('INSERT INTO users (id, name, email) VALUES ' +
                    "(1, 'my name', 'email@somehost'), " +
                    "(2, 'my other name', 'other_email@somehost');")

        query = (Query('insert')
                 .entity('users')
                 .set_data({
                     'id': 1,
                     'name': 'my name',
                     'email': 'email@somehost'
                 })
                 .set_data({
                     'id': 2,
                     'name': 'my other name',
                     'email': 'other_email@somehost'
                 }))

        assert query.dump_insert() == expected

    def test_query_dump_update(self):
        expected = ('UPDATE users SET ' +
                    "name = 'my other name', " +
                    "email = 'other_email@somehost' " +
                    "WHERE id = 2;")

        query = (Query('insert')
                 .entity('users')
                 .filter(Filter.equals('id', 2))
                 .set_data({
                     'name': 'my other name',
                     'email': 'other_email@somehost'
                 }))

        assert query.dump_update() == expected

    def test_query_dump_delete(self):
        expected = "DELETE FROM users WHERE id = 2;"

        query = (Query('delete')
                 .entity('users')
                 .filter(Filter.equals('id', 2)))

        assert query.dump_delete() == expected

    def test_query_dump_select(self):
        expected = ('SELECT id, name, email FROM users ' +
                    "WHERE name LIKE 'some_name%' " +
                    'ORDER BY id DESC, name ASC LIMIT 10 OFFSET 0;')

        query = (Query('select')
                 .entity('users')
                 .set_columns(['id', 'name', 'email'])
                 .filter(Filter
                         .like('name', 'some_name%')
                         .order_by('id', -1)
                         .order_by('name')
                         .limit(10)
                         .offset(0)))

        assert query.dump_select() == expected
