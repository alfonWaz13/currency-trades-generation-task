import re
from dataclasses import dataclass

from src.exceptions import InvalidCurrencyTradeIdLengthError, InvalidCharactersTradeIdError

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
