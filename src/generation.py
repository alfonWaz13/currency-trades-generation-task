import random

from src.currency_trade_id import CurrencyTradeId, ID_CHARACTERS, CURRENCY_TRADES_ID_LENGTH
from src import currency_trade_id_repository
from src.currency_trade_id_repository.exceptions import MultipleCurrencyTradeInsertionError


class CurrencyTradeIdGenerator:
    def __init__(self, repository: currency_trade_id_repository.CurrencyTradeIdRepository):
        self.repository = repository

    def generate(self):
        currency_trade_id = None

        while not currency_trade_id:
            currency_trade_id = self._get_random_currency_trade_id()
            try:
                self.repository.add_currency_trade_id(currency_trade_id)
            except currency_trade_id_repository.AlreadySavedCurrencyTradeIdError:
                currency_trade_id = None

        return currency_trade_id

    def generate_bulk(self, number_of_ids: int) -> set[CurrencyTradeId]:
        new_currency_trade_ids = set()
        currency_trade_ids_to_insert = set()

        while len(new_currency_trade_ids) < number_of_ids:

            number_new_currency_trades_to_generate = number_of_ids - len(new_currency_trade_ids) - len(currency_trade_ids_to_insert)
            currency_trade_ids_to_insert.update(self._get_multiple_random_currency_trade_ids(number_new_currency_trades_to_generate))

            try:
                self.repository.add_bulk_currency_trade_ids(currency_trade_ids_to_insert)
                new_currency_trade_ids.update(currency_trade_ids_to_insert)
                currency_trade_ids_to_insert = set()
            except MultipleCurrencyTradeInsertionError as exception:
                duplicated_ids = exception.already_saved_currency_trade_ids
                currency_trade_ids_to_insert.difference_update(duplicated_ids)

        return new_currency_trade_ids

    @classmethod
    def _get_multiple_random_currency_trade_ids(cls, number_new_currency_trades_to_generate):
        return set(cls._get_random_currency_trade_id() for _ in range(number_new_currency_trades_to_generate))

    @classmethod
    def _get_random_currency_trade_id(cls):
        return CurrencyTradeId(''.join(random.choices(ID_CHARACTERS, k=CURRENCY_TRADES_ID_LENGTH)))