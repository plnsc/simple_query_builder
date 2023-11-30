"""
Map of elements that may differ between different SQL dialects.

TODO: list of what needs to be done in **symbol_map.py**
(#): think of a way of warning if the file is called outside package context
     because this is a internal only class is not needed outside it
(#): commented out operators still need more thought to it
(#): implement a way of overriding the symbols when other dialects are included
(1): has no shortcut method 'cause I can't figure it out yet a non-restrict name for it
(2): still did not thought in what way this is used alone
(3): did not done anything with arithmetic operators yet
(4): alias is alone there because didn't found a way of "group call it" yet
     wanted to throw it together with the ones in 'values' and call it 'typing'
     but forgot that typing is a reserved word :p
(5): dragging it to be the last one to make
"""


class _SymbolMap():
    values: dict[str, str] = {}
    operators: dict[str, str] = {}
    composed: dict[str, list[str]] = {}
    separators: dict[str, str] = {}
    clauses: dict[str, str] = {}
    wrappers: dict[str, str] = {}

    def __init__(self):
        default_map = _SYMBOL_MAP['default']

        self.values = default_map['values']
        self.operators = default_map['operators']
        self.composed = default_map['composed']
        self.separators = default_map['separators']
        self.clauses = default_map['clauses']
        self.wrappers = default_map['wrappers']


_SYMBOL_MAP = {
    'default': {
        'values': {
            'true': 'TRUE',
            'false': 'FALSE',
            'null': 'NULL',
        },
        'operators': {
            # ** basic comparison **
            'equals': '=',
            'not_equals': '<>',  # also !=
            'like': 'LIKE',
            'not_like': 'NOT LIKE',
            'less_than': '<',
            'less_than_or_equal': '<=',
            'greater_than': '>',
            'greater_than_or_equal': '>=',
            # ** special comparison, but still "{val} {operator} {val}" format **
            'in': 'IN',  # (1)
            'not_in': 'NOT IN',  # (1)
            'is': 'IS',  # (1)
            'is_not': 'IS NOT',  # (1)
            # ** logical **
            'and': 'AND',
            'or': 'OR',
            # 'not': 'NOT', (2)
            # ** arithmetic **  (3)
            # 'addition': '+',
            # 'subtraction': '-',
            # 'multiplication': '*',
            # 'division': '/',
            # 'modulo': '%',
            # ** other **
            # 'alias': 'AS', (4)
        },
        # ** outside "{val} {operator} {val}" **
        'composed': {
            'between': ['BETWEEN', 'AND'],
            # 'group_by': ['GROUP BY', 'HAVING'], (5)
            'order_by': ['ORDER BY', 'ASC', 'DESC'],
            'limit': ['LIMIT'],
            'offset': ['OFFSET'],
        },
        'separators': {
            'list': ',',
            'statement': ';',
        },
        'clauses': {
            'insert_into': 'INSERT INTO',
            'insert_values': 'VALUES',
            'select': 'SELECT',
            'select_from': 'FROM',
            'update': 'UPDATE',
            'update_set': 'SET',
            'update_assign': '=',
            'delete_from': 'DELETE FROM',
            'where': 'WHERE',
        },
        'wrappers': {
            'string': "''",
            'identifier': '',  # also `` or []
            'group': '()',
        },
    }
}
