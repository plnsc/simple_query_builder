"""

TODO: list of what needs to be done in **query.py**
(#): called it Query instead of Statement to make the class name short
(#): the validation to make sure that the rows and columns to match eachother
     need some thought about it
"""

from simple_query_builder.dialect import _Dialect


class Query(_Dialect):
    _entity: str
    _columns: list[str]
    _rows: list[list[str]]
    _sql: list[str]

    def __init__(self, entity: str = ''):
        super().__init__()

        self._entity = entity
        self._columns = []
        self._rows = []

    def _get_entity(self) -> str:
        return self.wrapper('identifier', self._entity)

    def set_columns(self, columns: list[str]) -> 'Query':
        self._columns = [self.wrapper('identifier', column)
                         for column in columns]
        return self

    def set_row(self, row: list[str]) -> 'Query':
        self._rows.append([self.sanitize(row) for row in row])
        return self

    def set(self, data: dict[str, any]) -> 'Query':
        self.set_columns(data.keys())
        self.set_row(data.values())

        return self
