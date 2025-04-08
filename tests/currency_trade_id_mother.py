import random

from src.currency_trade_id import CurrencyTradeId, ID_CHARACTERS, CURRENCY_TRADES_ID_LENGTH


class CurrencyTradeIdMother:

    @staticmethod
    def get_valid() -> CurrencyTradeId:
        return CurrencyTradeId(''.join(random.choices(ID_CHARACTERS, k=CURRENCY_TRADES_ID_LENGTH)))
