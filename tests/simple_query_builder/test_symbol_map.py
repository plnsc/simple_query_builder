import unittest

from simple_query_builder.symbol_map import _SymbolMap


class TestSymbolMap(unittest.TestCase):
    def setUp(self):
        self.map = _SymbolMap()

    def map_validate_list(self, entries):
        for entry in entries:
            assert type(entries[entry]) is str

    def map_validade_dict(self, entries):
        for entry in entries:
            assert type(entries[entry]) is list
            assert all(
                [type(part) is str for part in entries[entry]])

    def test_map_values(self):
        self.map_validate_list(self.map.values)

    def test_map_operators(self):
        self.map_validate_list(self.map.operators)

    def test_map_composed(self):
        self.map_validade_dict(self.map.composed)

    def test_map_statements(self):
        self.map_validade_dict(self.map.statements)

    def test_map_separators(self):
        self.map_validate_list(self.map.separators)

    def test_map_wrappers(self):
        self.map_validate_list(self.map.wrappers)
