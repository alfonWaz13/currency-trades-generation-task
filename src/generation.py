import random

from src.currency_trade_id import CurrencyTradeId, ID_CHARACTERS, CURRENCY_TRADES_ID_LENGTH
from src import currency_trade_id_repository


class CurrencyTradeIdGenerator:
    def __init__(self, repository: currency_trade_id_repository.CurrencyTradeIdRepository):
        self.repository = repository

    def generate(self):
        currency_trade_id = None

        while not currency_trade_id:
            currency_trade_id = CurrencyTradeId(''.join(random.choices(ID_CHARACTERS, k=CURRENCY_TRADES_ID_LENGTH)))
            try:
                self.repository.add_currency_trade_id(currency_trade_id)
            except currency_trade_id_repository.AlreadySavedCurrencyTradeIdError:
                currency_trade_id = None

        return currency_trade_id
