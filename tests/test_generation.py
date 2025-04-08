from unittest.mock import MagicMock

from src.currency_trade_id_repository import AlreadySavedCurrencyTradeIdError
from src.generation import CurrencyTradeIdGenerator


class TestGeneration:

    @classmethod
    def setup_method(cls):
        cls.repository = MagicMock()

    def test_generate_returns_a_currency_trade_id(self):
        currency_trade_id_generator = CurrencyTradeIdGenerator(repository=self.repository)
        currency_trade_id = currency_trade_id_generator.generate()
        assert currency_trade_id is not None

    def test_generate_stores_currency_trade_id(self):
        currency_trade_id_generator = CurrencyTradeIdGenerator(repository=self.repository)
        currency_trade_id_generator.generate()
        assert self.repository.add_currency_trade_id.call_count == 1

    def test_generate_calls_add_currency_trade_again_if_id_exists(self):
        currency_trade_id_generator = CurrencyTradeIdGenerator(repository=self.repository)
        self.repository.add_currency_trade_id.side_effect = [
            AlreadySavedCurrencyTradeIdError("Duplicated ID"),
            None
        ]
        currency_trade_id_generator.generate()
        assert self.repository.add_currency_trade_id.call_count == 2

    def test_generate_bulk_returns_a_set_of_currency_trade_ids(self):
        currency_trade_id_generator = CurrencyTradeIdGenerator(repository=self.repository)
        currency_trade_ids = currency_trade_id_generator.generate_bulk(10)
        assert len(currency_trade_ids) == 10
