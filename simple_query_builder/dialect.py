"""
Operations that are common between all entities to normalize the SQL
values, operators, identifiers and clauses.

TODO: list of what needs to be done in **dialect.py**
(#): think of a way of warning if the file is called outside package context
     because this is a internal only class is not needed outside it
(1): think of a way to improve sanitization of numeric values
(2): think of a way to safely sanitize other values (json may be a good way
     of doing it for when a dict is found
"""

from typing import final

from simple_query_builder.symbol_map import _SymbolMap


class _Dialect():
    map: '_SymbolMap'

    def __init__(self):
        self.map = _SymbolMap()

    @final
    def value(self, key: str) -> str:
        return self.map.values[key]

    @final
    def operator(self, key: str) -> str:
        return self.map.operators[key]

    @final
    def composed(self, key: str) -> list[str]:
        return self.map.composed[key]

    @final
    def separator(self, key: str) -> str:
        return self.map.separators[key]

    @final
    def clause(self, key: str) -> str:
        return self.map.clauses[key]

    @final
    def wrapper(self, key: str, value: any) -> str:
        result = list(self.map.wrappers[key])
        result.insert(1, value)
        return ''.join(result)

    @final
    def sanitize(self, value: any) -> str:  # (1)(2)
        if type(value) is list:
            separator = '%s ' % self.separator('list')
            result = separator.join([self.sanitize(v) for v in value])
            return self.wrapper('group', result)
        elif type(value) is str:
            return self.wrapper('string', value)
        elif type(value) is bool:
            return self.value('true' if value else 'false')
        elif value is None:
            return self.value('null')

        return str(value)
