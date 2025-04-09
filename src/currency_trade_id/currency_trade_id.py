import re
from dataclasses import dataclass

from .exceptions import InvalidCurrencyTradeIdLengthError, InvalidCharactersTradeIdError

ID_CHARACTERS = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
CURRENCY_TRADES_ID_LENGTH = 7


@dataclass(frozen=True)
class CurrencyTradeId:
    value: str

    def __post_init__(self):
        if len(self.value) != CURRENCY_TRADES_ID_LENGTH:
            raise InvalidCurrencyTradeIdLengthError(
                currency_trade_id=self.value,
                expected_length=CURRENCY_TRADES_ID_LENGTH
            )
        if not re.compile('^[' + ID_CHARACTERS + ']+$').match(self.value):
            raise InvalidCharactersTradeIdError(
                currency_trade_id=self.value,
                expected_characters=ID_CHARACTERS
            )

    def __str__(self):
        return self.value

    def __len__(self):
        return len(self.value)

    def get_final_digits(self, number_of_digits: int) -> str:
        if number_of_digits > len(self.value):
            raise ValueError("number_of_digits must be less than or equal to the length of the currency trade id")
        return self.value[-number_of_digits:]

    def get_initial_digits(self, number_of_digits: int) -> str:
        if number_of_digits > len(self.value):
            raise ValueError("number_of_digits must be less than or equal to the length of the currency trade id")
        return self.value[:number_of_digits]
