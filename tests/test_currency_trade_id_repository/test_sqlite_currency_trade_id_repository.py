import os
import sqlite3
from pathlib import Path

import pytest

from src.currency_trade_id_repository import SqliteCurrencyTradeIdRepository, AlreadySavedCurrencyTradeIdError
from src.currency_trade_id_repository.exceptions import MultipleCurrencyTradeInsertionError
from tests.currency_trade_id_mother import CurrencyTradeIdMother


class TestSqliteCurrencyTradeIdRepository:

    @classmethod
    def setup_class(cls):
        cls.database_path = Path("test.db")

    @classmethod
    def setup_method(cls):
        with sqlite3.connect(cls.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA table_info(currency_trade_ids)")
            if cursor.fetchall():
                connection.execute("DELETE FROM currency_trade_ids")
                connection.commit()

    @classmethod
    def teardown_class(cls):
        if cls.database_path.exists():
            os.remove(cls.database_path)

    def assert_id_in_database(self, currency_trade_id):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM currency_trade_ids WHERE id = ?", (str(currency_trade_id),))
            row = cursor.fetchone()
        assert row is not None
        assert row[0] == str(currency_trade_id)


    def test_currency_trade_id_is_correctly_added(self):
        repository = SqliteCurrencyTradeIdRepository(db_path=self.database_path)
        currency_trade_id = CurrencyTradeIdMother.get_valid()

        repository.add_currency_trade_id(currency_trade_id)
        self.assert_id_in_database(currency_trade_id)

    def test_error_raised_when_currency_trade_id_already_exists(self):
        repository = SqliteCurrencyTradeIdRepository(db_path=self.database_path)
        currency_trade_id = CurrencyTradeIdMother.get_valid()

        repository.add_currency_trade_id(currency_trade_id)

        with pytest.raises(AlreadySavedCurrencyTradeIdError):
            repository.add_currency_trade_id(currency_trade_id)

    def test_bulk_currency_trade_ids_are_correctly_added(self):
        repository = SqliteCurrencyTradeIdRepository(db_path=self.database_path)
        currency_trade_ids = {CurrencyTradeIdMother.get_valid() for _ in range(10)}

        repository.add_bulk_currency_trade_ids(currency_trade_ids)

        for currency_trade_id in currency_trade_ids:
            self.assert_id_in_database(currency_trade_id)

    def test_error_raised_when_duplicated_currency_trade_ids_are_added_in_bulk(self):
        repository = SqliteCurrencyTradeIdRepository(db_path=self.database_path)
        currency_trade_id_1 = CurrencyTradeIdMother.get_valid()
        currency_trade_id_2 = CurrencyTradeIdMother.get_valid()
        currency_trade_id_3 = CurrencyTradeIdMother.get_valid()

        repository.add_bulk_currency_trade_ids({currency_trade_id_1, currency_trade_id_2, currency_trade_id_3})

        with pytest.raises(MultipleCurrencyTradeInsertionError) as exception:
            repository.add_bulk_currency_trade_ids({currency_trade_id_1, currency_trade_id_2})

        assert currency_trade_id_1 in exception.value.already_saved_currency_trade_ids
        assert currency_trade_id_2 in exception.value.already_saved_currency_trade_ids
