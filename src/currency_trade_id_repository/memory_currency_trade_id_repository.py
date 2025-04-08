from src.currency_trade_id import CurrencyTradeId

from .currency_trade_id_repository import CurrencyTradeIdRepository
from .exceptions import AlreadySavedCurrencyTradeIdError



class MemoryCurrencyTradeIdRepository(CurrencyTradeIdRepository):

    def __init__(self):
        self._currency_trade_ids = set()

    def add_currency_trade_id(self, currency_trade_id: CurrencyTradeId) -> None:
        if currency_trade_id in self._currency_trade_ids:
            raise AlreadySavedCurrencyTradeIdError(currency_trade_id)
        self._currency_trade_ids.add(currency_trade_id)
