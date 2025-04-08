from unittest.mock import MagicMock

from src.currency_trade_id import CurrencyTradeId
from src.currency_trade_id_repository import (AlreadySavedCurrencyTradeIdError, MultipleCurrencyTradeInsertionError,
                                              EmptyCurrencyTradeIdException)
from src.generation import CurrencyTradeIdGenerator
from tests.currency_trade_id_mother import CurrencyTradeIdMother


class TestGeneration:

    @classmethod
    def setup_method(cls):
        cls.repository = MagicMock()
        cls.repository.get_last_currency_trade_id.return_value = CurrencyTradeIdMother.get_valid()

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
            AlreadySavedCurrencyTradeIdError(CurrencyTradeIdMother.get_valid()),
            None
        ]
        currency_trade_id_generator.generate()
        assert self.repository.add_currency_trade_id.call_count == 2

    def test_generate_bulk_returns_a_set_of_currency_trade_ids(self):
        currency_trade_id_generator = CurrencyTradeIdGenerator(repository=self.repository)
        currency_trade_ids = currency_trade_id_generator.generate_bulk(10)
        assert len(currency_trade_ids) == 10

    def test_generate_bulk_stores_currency_trade_ids(self):
        currency_trade_id_generator = CurrencyTradeIdGenerator(repository=self.repository)
        currency_trade_id_generator.generate_bulk(2)
        assert self.repository.add_bulk_currency_trade_ids.call_count == 1

    def test_generate_bulk_calls_add_bulk_currency_trade_ids_again_if_ids_exist(self):
        currency_trade_id_generator = CurrencyTradeIdGenerator(repository=self.repository)
        self.repository.add_bulk_currency_trade_ids.side_effect = [
            MultipleCurrencyTradeInsertionError(currency_trade_ids={CurrencyTradeIdMother.get_valid()}),
            None
        ]
        currency_trade_id_generator.generate_bulk(10)
        assert self.repository.add_bulk_currency_trade_ids.call_count == 2

    def test_generate_returns_the_next_id_in_sequence(self):
        self.repository.get_last_currency_trade_id.return_value = CurrencyTradeId("AABBCCD")
        currency_trade_id_generator = CurrencyTradeIdGenerator(repository=self.repository)
        currency_trade_id = currency_trade_id_generator.generate()
        assert currency_trade_id == CurrencyTradeId("AABBCCE")

    def test_generate_bulk_returns_the_next_ids_in_sequence(self):
        self.repository.get_last_currency_trade_id.return_value = CurrencyTradeId("AABBCCD")
        currency_trade_id_generator = CurrencyTradeIdGenerator(repository=self.repository)
        currency_trade_ids = currency_trade_id_generator.generate_bulk(3)

        assert CurrencyTradeId("AABBCCE") in currency_trade_ids
        assert CurrencyTradeId("AABBCCF") in currency_trade_ids
        assert CurrencyTradeId("AABBCCG") in currency_trade_ids

    def test_generate_returns_0000000_if_no_ids_are_stored(self):
        self.repository.get_last_currency_trade_id.side_effect = EmptyCurrencyTradeIdException()
        currency_trade_id_generator = CurrencyTradeIdGenerator(repository=self.repository)
        currency_trade_id = currency_trade_id_generator.generate()
        assert currency_trade_id == CurrencyTradeId("0000000")
