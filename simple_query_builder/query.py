"""
Builds SQL statements.

TODO:
[ ]: Maybe add the feature to call a new instance from any methods that care invoked the class staticly (?)
[ ]: Feature to add another filter by passing it in __new__ (?)
[ ]: called it Query instead of Statement to make the class name short
[ ]: the validation to make sure that the rows and columns to match eachother need some thought about it
"""

from simple_query_builder import Filter
from simple_query_builder.dialect import _Dialect


class Query(_Dialect):
    _statement: str
    _entity: str
    _filter: Filter
    _columns: list[str]
    _rows: list[list[str]]

    def __init__(self, statement: str = ""):
        super().__init__()

        self._statement = statement
        self._entity = ""
        self._filter = None
        self._columns = []
        self._rows = []

    def entity(self, identifier) -> "Query":
        self._entity = identifier
        return self

    def filter(self, filter: Filter) -> "Query":
        self._filter = filter
        return self

    def set_columns(self, columns: list[str]) -> "Query":
        self._columns = [self.wrapper("identifier", column)
                         for column in columns]
        return self

    def set_row(self, row: list[str]) -> "Query":
        self._rows.append([self.sanitize(row) for row in row])
        return self

    def set_data(self, data) -> "Query":
        self.set_columns(data.keys())
        self.set_row(data.values())
        return self

    def dump(self) -> str:
        if self._statement == 'insert':
            return self.dump_insert()
        elif self._statement == 'update':
            return self.dump_update()
        elif self._statement == 'delete':
            return self.dump_delete()
        elif self._statement == 'select':
            return self.dump_select()

    def dump_insert(self) -> str:
        (insert_symbol, values_symbol) = self.statement("insert")
        entity = self.wrapper("identifier", self._entity)
        columns = self.wrapper("group", self.separator("list", self._columns))
        rows = self.separator("list", [self.wrapper("group", self.separator("list", row))
                                       for row in self._rows])

        result = self.separator(
            "empty", [insert_symbol, entity, columns, values_symbol, rows])

        return self.separator("statement", [result])

    def dump_update(self) -> str:
        (update_symbol, set_symbol, assign_symbol,
         where_symbol) = self.statement("update")
        entity = self.wrapper("identifier", self._entity)
        rows = self.separator("list", [self.separator("empty", [column, assign_symbol, value])
                                       for column, value in zip(self._columns, self._rows[0])])

        result = [update_symbol, entity, set_symbol, rows]

        if self._filter and len(self._filter._parts):
            filter_criteria = self._filter.dump_parts()
            result.append(self.separator(
                "empty", [where_symbol, filter_criteria]))

        return self.separator("statement", [self.separator("empty", result)])

    def dump_delete(self) -> str:
        delete_symbol, where_symbol = self.statement("delete")
        entity = self.wrapper("identifier", self._entity)

        result = [delete_symbol, entity]

        if self._filter and len(self._filter._parts):
            filter_criteria = self._filter.dump_parts()
            result.append(self.separator(
                "empty", [where_symbol, filter_criteria]))

        return self.separator("statement", [self.separator("empty", result)])

    def dump_select(self) -> str:
        select_symbol, from_symbol, where_symbol = self.statement("select")
        entity = self.wrapper("identifier", self._entity)
        columns = self.separator("list", self._columns)

        result = [select_symbol, columns, from_symbol, entity]

        if self._filter and len(self._filter._parts):
            filter_criteria = self._filter.dump_parts()
            result.append(self.separator(
                "empty", [where_symbol, filter_criteria]))

        if self._filter and len(self._filter._globals):
            filter_global_criteria = self._filter.dump_globals()
            result.append(filter_global_criteria)

        return self.separator("statement", [self.separator("empty", result)])
