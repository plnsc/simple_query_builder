"""
Builds criteria to be used in the full SQL statements.

TODO:
[ ]: Maybe add the feature to call a new instance from any methods that care invoked the class staticly (?)
[ ]: Feature to add another filter by passing it in __new__ (?)
[ ]: (1) Find a way to someshow attach _globals recursively 'til it reaches the first upmost filter making it avaible and replaceble throughtout all nested filter chain (should it be broken into another class?
[ ]: (2) GROUP BY and HAVING need some thought about it before implement it be cause it uses SQL functions and thats other thing that I didn't think about it yet too
"""

from simple_query_builder.dialect import _Dialect


class Filter(_Dialect):
    """ """

    """Simple criteria meant to filter data, can be nested together and may appear more than once in the statement"""
    _parts: list[str]
    """Criteria meant for limiting data and can be defined only once throughout the entire statement"""
    _globals: dict[str, list[str]]  # (1)

    def __init__(self):
        super().__init__()
        self._parts = []
        self._globals = {}

    def dump_parts(self, wrap_it=False) -> str:
        result = self.separator("empty", self._parts)

        if wrap_it:
            return self.wrapper("group", result)

        return result

    def dump_globals(self) -> str:
        result = []

        for name in ("order_by", "limit", "offset"):  # (2)
            if name in self._globals:
                result.append(self.separator("empty", self._globals[name]))

        return self.separator("empty", result)

    def set_parts(self, parts: list) -> "Filter":
        self._parts = parts
        return self

    def set_globals(self, name: str, parts: list) -> "Filter":  # (1)
        self._globals[name] = parts
        return self

    def wrap_it(self) -> "Filter":
        self.set_parts([self.dump_parts(wrap_it=True)])
        return self

    def add(self, filter: "Filter", operator="and") -> "Filter":
        parts = [filter.dump_parts()]

        if len(self._parts):
            parts.insert(0, self.operator(operator))

        self.set_parts([*self._parts, *parts])
        return self

    def add_and(self, filter: "Filter") -> "Filter":
        return self.add(filter, operator="and")

    def add_or(self, filter: "Filter") -> "Filter":
        return self.add(filter, operator="or")

    def order_by(self, identifier: str, direction=1) -> "Filter":
        (order_by_symbol, asc_symbol, desc_symbol) = self.composed("order_by")

        result = (self._globals["order_by"]
                  if "order_by" in self._globals
                  else [order_by_symbol])
        result.append(self.separator("empty", [self.wrapper("identifier", identifier),
                                               asc_symbol if direction >= 0 else desc_symbol]))

        self.set_globals(
            "order_by", [result[0], self.separator("list", result[1:])])

        return self

    def limit(self, value) -> "Filter":
        (limit_symbol,) = self.composed("limit")
        self.set_globals("limit", [limit_symbol, self.sanitize(value)])
        return self

    def offset(self, value) -> "Filter":
        (offset_symbol,) = self.composed("offset")
        self.set_globals("offset", [offset_symbol, self.sanitize(value)])
        return self

    @staticmethod
    def create(identifier: str, operator: str, value) -> "Filter":
        filter = Filter()
        return filter.set_parts([filter.wrapper("identifier", identifier),
                                 filter.operator(operator),
                                 filter.sanitize(value)])

    @staticmethod
    def between(identifier: str, start, end) -> "Filter":
        filter = Filter()
        between_symbol, and_symbol = filter.composed("between")
        return filter.set_parts([filter.wrapper("identifier", identifier),
                                 between_symbol,
                                 filter.sanitize(start),
                                 and_symbol,
                                 filter.sanitize(end)])

    @staticmethod
    def equals(identifier: str, value) -> "Filter":
        return Filter.create(identifier, "equals", value)

    @staticmethod
    def not_equals(identifier: str, value) -> "Filter":
        return Filter.create(identifier, "not_equals", value)

    @staticmethod
    def like(identifier: str, value) -> "Filter":
        return Filter.create(identifier, "like", value)

    @staticmethod
    def not_like(identifier: str, value) -> "Filter":
        return Filter.create(identifier, "not_like", value)

    @staticmethod
    def lt(identifier: str, value) -> "Filter":
        return Filter.create(identifier, "less_than", value)

    @staticmethod
    def lte(identifier: str, value) -> "Filter":
        return Filter.create(identifier, "less_than_or_equal", value)

    @staticmethod
    def gt(identifier: str, value) -> "Filter":
        return Filter.create(identifier, "greater_than", value)

    @staticmethod
    def gte(identifier: str, value) -> "Filter":
        return Filter.create(identifier, "greater_than_or_equal", value)
