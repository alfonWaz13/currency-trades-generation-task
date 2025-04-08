from src.currency_trade_id import CurrencyTradeId


class AlreadySavedCurrencyTradeIdError(Exception):
    def __init__(self, currency_trade_id: CurrencyTradeId):
        super().__init__(f"Currency trade id {currency_trade_id} already exists in system.")

class MultipleCurrencyTradeInsertionError(Exception):
    def __init__(self, currency_trade_ids: set[CurrencyTradeId]):
        super().__init__(f"Multiple currency trade ids {currency_trade_ids} already exist in system.")
        self.already_saved_currency_trade_ids = currency_trade_ids
