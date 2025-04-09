import pytest

from src.currency_trade_id import CurrencyTradeId, exceptions


class TestCurrencyTradeId:

    def test_error_raised_when_id_is_not_correct_length(self):
        with pytest.raises(exceptions.InvalidCurrencyTradeIdLengthError):
            CurrencyTradeId("123456")

    def test_error_raised_when_id_contains_invalid_characters(self):
        with pytest.raises(exceptions.InvalidCharactersTradeIdError):
            CurrencyTradeId("123456!")

    def test_last_digits_are_correctly_returned(self):
        currency_trade_id = CurrencyTradeId("1234567")
        assert currency_trade_id.get_final_digits(3) == "567"

    def test_initial_digits_are_correctly_returned(self):
        currency_trade_id = CurrencyTradeId("1234567")
        assert currency_trade_id.get_initial_digits(3) == "123"

