import unittest

from simple_query_builder.symbol_map import _SymbolMap


class TestSymbolMap(unittest.TestCase):
    def setUp(self):
        self.map = _SymbolMap()

    def validate_list(self, symbols):
        for symbol in symbols:
            self.assertIsInstance(symbols[symbol], str)

    def validade_dict(self, symbols_list):
        for symbol in symbols_list:
            self.assertIsInstance(symbols_list[symbol], tuple)
            for symbol_part in symbols_list[symbol]:
                self.assertIsInstance(symbol_part, str)

    def test_values(self):
        self.validate_list(self.map.values)

    def test_operators(self):
        self.validate_list(self.map.operators)

    def test_composed(self):
        self.validade_dict(self.map.composed)

    def test_statements(self):
        self.validade_dict(self.map.statements)

    def test_separators(self):
        self.validate_list(self.map.separators)

    def test_wrappers(self):
        self.validate_list(self.map.wrappers)
