from src.currency_trade_id import CurrencyTradeId


class AlreadySavedCurrencyTradeIdError(Exception):
    def __init__(self, currency_trade_id: CurrencyTradeId):
        super().__init__(f"Currency trade id {currency_trade_id} already exists in system.")
