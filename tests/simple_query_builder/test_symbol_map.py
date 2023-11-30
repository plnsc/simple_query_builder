import unittest

from simple_query_builder.symbol_map import _SymbolMap


class TestSymbolMap(unittest.TestCase):
    def setUp(self):
        self.map = _SymbolMap()

    def map_validate_property(self, entries):
        for entry in entries:
            assert type(entries[entry]) is str

    def test_map_values(self):
        self.map_validate_property(self.map.values)

    def test_map_operators(self):
        self.map_validate_property(self.map.operators)

    def test_map_composed(self):
        for entry in self.map.composed:
            assert type(self.map.composed[entry]) is list
            assert all(
                [type(part) is str for part in self.map.composed[entry]])

    def test_map_separators(self):
        self.map_validate_property(self.map.separators)

    def test_map_clauses(self):
        self.map_validate_property(self.map.clauses)

    def test_map_wrappers(self):
        self.map_validate_property(self.map.wrappers)
