from abc import ABC

from src.currency_trade_id import CurrencyTradeId


class CurrencyTradeIdRepository(ABC):

    def add_currency_trade_id(self, currency_trade_id: CurrencyTradeId) -> None: ...

    def add_bulk_currency_trade_ids(self, currency_trade_ids: set[CurrencyTradeId]) -> None: ...
