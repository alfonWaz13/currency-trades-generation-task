class InvalidCurrencyTradeIdLengthError(Exception):
    def __init__(self, currency_trade_id: str, expected_length: int):
        super().__init__(f"Incorrect length of currency trade id {currency_trade_id}, "
                         f"{expected_length} characters expected.")

class InvalidCharactersTradeIdError(Exception):
    def __init__(self, currency_trade_id: str, expected_characters: str):
        super().__init__(f"Invalid characters in currency trade id {currency_trade_id}, "
                         f"only {expected_characters} are allowed.")
