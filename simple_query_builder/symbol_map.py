"""
Map of elements that may differ between different SQL dialects.

TODO:
[ ]: Commented out operators still need more thought to it
[ ]: Implement a way of overriding the symbols when other dialects are included
[ ]: (1) Has no shortcut method 'cause I can't figure it out yet a non-restrict name for it
[ ]: (2) Still did not thought in what way this is used alone
[ ]: (3) Did not done anything with arithmetic operators yet
[ ]: (4) Alias is alone there because didn't found a way of "group call it" yet wanted to throw it together with the ones in 'values' and call it 'typing' but forgot that typing is a reserved word :p
[ ]: (5) Dragging it to be the last one to make
"""
from types import MappingProxyType


class _SymbolMap:
    values: dict[str, str] = {}
    operators: dict[str, str] = {}
    composed: dict[str, tuple[str]] = {}
    statements: dict[str, tuple[str]] = {}
    separators: dict[str, str] = {}
    wrappers: dict[str, str] = {}

    def __init__(self):
        default_map = _SYMBOL_MAP["default"]

        self.values = default_map["values"]
        self.operators = default_map["operators"]
        self.composed = default_map["composed"]
        self.statements = default_map["statements"]
        self.separators = default_map["separators"]
        self.wrappers = default_map["wrappers"]


_SYMBOL_MAP = MappingProxyType({
    "default": {
        "values": {
            "true": "TRUE",
            "false": "FALSE",
            "null": "NULL",
        },
        "operators": {
            # Basic comparison
            "equals": "=",
            "not_equals": "<>",  # also !=
            "like": "LIKE",
            "not_like": "NOT LIKE",
            "less_than": "<",
            "less_than_or_equal": "<=",
            "greater_than": ">",
            "greater_than_or_equal": ">=",
            # No basic comparion, but still in {val} {operator} {val} format
            "in": "IN",  # (1)
            "not_in": "NOT IN",  # (1)
            "is": "IS",  # (1)
            "is_not": "IS NOT",  # (1)
            # Logical
            "and": "AND",
            "or": "OR",
            # "not": "NOT", (2)
            # Arithmetic (3)
            # "addition": "+",
            # "subtraction": "-",
            # "multiplication": "*",
            # "division": "/",
            # "modulo": "%",
            # Other
            "alias": "AS",  # (4)
        },
        # Global clauses and operators outside {val} {operator} {val} format
        "composed": {
            "between": ("BETWEEN", "AND"),
            # "group_by": ("GROUP BY", "HAVING"),  # (5)
            "order_by": ("ORDER BY", "ASC", "DESC"),
            "limit": ("LIMIT",),
            "offset": ("OFFSET",),
        },
        "statements": {
            "insert": ("INSERT INTO", "VALUES"),
            "update": ("UPDATE", "SET", "=", "WHERE"),
            "delete": ("DELETE FROM", "WHERE"),
            "select": ("SELECT", "FROM", "WHERE"),
        },
        "separators": {
            "list": ",",
            "statement": ";",
            "empty": " ",
        },
        "wrappers": {
            "string": "''",
            "identifier": "",  # also `` or []
            "group": "()",
        },
    }
})
