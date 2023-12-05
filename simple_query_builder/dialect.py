"""
Operations that are common between all entities to normalize the SQL
values, operators, identifiers and statements.

TODO:
[ ]: (1) Think of a way to improve sanitization of numeric values
[ ]: (2) Think of a way to safely sanitize other values (json may be a good way
     of doing it for when a dict is found
"""

from typing import final

from simple_query_builder.symbol_map import _SymbolMap


class _Dialect:
    _map: "_SymbolMap"
    _minified: bool

    def __init__(self):
        self._map = _SymbolMap()
        self._minified = False

    @final
    def value(self, key: str) -> str:
        return self._map.values[key]

    @final
    def operator(self, key: str) -> str:
        return self._map.operators[key]

    @final
    def composed(self, key: str) -> tuple[str]:
        return self._map.composed[key]

    @final
    def statement(self, key: str) -> tuple[str]:
        return self._map.statements[key]

    @final
    def separator(self, key: str, value: list, minifiable=False) -> str:
        separator = "{} ".format(self._map.separators[key])
        result = value

        if key == "statement":
            result.append("")
        elif key == "empty":
            separator = self._map.separators[key]

        if self._minified is True and minifiable is True:
            separator = separator.strip()

        return separator.join(value).strip()

    @final
    def wrapper(self, key: str, value) -> str:
        wrapper = self._map.wrappers[key]
        return "".join([wrapper[:1], value, wrapper[1:]])

    @final
    def sanitize(self, value) -> str:  # (1)(2)
        if isinstance(value, list):
            return self.wrapper("group", self.separator("list", [
                self.sanitize(v) for v in value]))
        elif isinstance(value, str):
            return self.wrapper("string", value)
        elif isinstance(value, bool):
            return self.value("true" if value else "false")
        elif value is None:
            return self.value("null")

        return str(value)
