import pytest

from src import currency_trade_id
from src.currency_trade_id import CurrencyTradeId


class TestCurrencyTradeId:

    def test_error_raised_when_id_is_not_correct_length(self):
        with pytest.raises(currency_trade_id.exceptions.InvalidCurrencyTradeIdLengthError):
            CurrencyTradeId("123456")

    def test_error_raised_when_id_contains_invalid_characters(self):
        with pytest.raises(currency_trade_id.exceptions.InvalidCharactersTradeIdError):
            CurrencyTradeId("123456!")
