"""

TODO: list of what needs to be done in **query.py**
(#): called it Query instead of Statement to make the class name short
(#): the validation to make sure that the rows and columns to match eachother
     need some thought about it
"""

from simple_query_builder import Filter
from simple_query_builder.dialect import _Dialect


class Query(_Dialect):
    _statement: str
    _entity: str
    _filter: Filter
    _columns: list[str]
    _rows: list[list[str]]

    def __init__(self, statement: str = ''):
        super().__init__()

        self._statement = statement
        self._entity = ''
        self._columns = []
        self._rows = []

    def entity(self, identifier) -> 'Query':
        self._entity = identifier
        return self

    def filter(self, filter: Filter) -> 'Query':
        self._filter = filter
        return self

    def set_columns(self, columns: list[str]) -> 'Query':
        self._columns = [self.wrapper('identifier', column)
                         for column in columns]
        return self

    def set_row(self, row: list[str]) -> 'Query':
        self._rows.append([self.sanitize(row) for row in row])
        return self

    def set_data(self, data: dict[str, any]) -> 'Query':
        self.set_columns(data.keys())
        self.set_row(data.values())
        return self

    def dump_insert(self) -> str:
        insert_symbol, values_symbol = self.statement('insert')

        result = self.separator('empty', [
            insert_symbol,
            self.wrapper('identifier', self._entity),
            self.wrapper('group', self.separator('list', self._columns)),
            values_symbol,
            self.separator('list', [
                self.wrapper('group', self.separator('list', row))
                for row in self._rows
            ]),
        ])

        return self.separator('statement', [result])

    def dump_update(self) -> str:
        update_symbol, set_symbol, assign_symbol, where_symbol = (
            self.statement('update'))

        result = [
            update_symbol,
            self.wrapper('identifier', self._entity),
            set_symbol,
            self.separator('list', [
                self.separator('empty', [column, assign_symbol, value])
                for column, value in zip(self._columns, self._rows[0])
            ]),
        ]

        if self._filter and len(self._filter._parts):
            result.append(self.separator('empty', [
                where_symbol, self._filter.dump_parts()
            ]))

        return self.separator('statement', [self.separator('empty', result)])

    def dump_delete(self) -> str:
        delete_symbol, where_symbol = self.statement('delete')

        result = [
            delete_symbol,
            self.wrapper('identifier', self._entity)
        ]

        if self._filter and len(self._filter._parts):
            result.append(self.separator('empty', [
                where_symbol, self._filter.dump_parts()
            ]))

        return self.separator('statement', [self.separator('empty', result)])

    def dump_select(self) -> str:
        select_symbol, from_symbol, where_symbol = self.statement('select')

        result = [
            select_symbol,
            self.separator('list', self._columns),
            from_symbol,
            self.wrapper('identifier', self._entity)
        ]

        if self._filter and len(self._filter._parts):
            result.append(self.separator('empty', [
                where_symbol, self._filter.dump_parts()
            ]))

        if self._filter and len(self._filter._globals):
            result.append(self._filter.dump_globals())

        return self.separator('statement', [self.separator('empty', result)])
