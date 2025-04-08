import pytest

from src.currency_trade_id_repository import MemoryCurrencyTradeIdRepository, AlreadySavedCurrencyTradeIdError
from tests.currency_trade_id_mother import CurrencyTradeIdMother


class TestMemoryCurrencyTradeIdRepository:

    def test_currency_trade_id_is_correctly_added(self):
        repository = MemoryCurrencyTradeIdRepository()
        currency_trade_id = CurrencyTradeIdMother.get_valid()

        repository.add_currency_trade_id(currency_trade_id)

        assert currency_trade_id in repository._currency_trade_ids

    def test_error_raised_when_currency_trade_id_already_exists(self):
        repository = MemoryCurrencyTradeIdRepository()
        currency_trade_id = CurrencyTradeIdMother.get_valid()

        repository.add_currency_trade_id(currency_trade_id)

        with pytest.raises(AlreadySavedCurrencyTradeIdError):
            repository.add_currency_trade_id(currency_trade_id)