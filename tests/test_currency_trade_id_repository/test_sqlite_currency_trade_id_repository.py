import os
import sqlite3
from pathlib import Path

import pytest

from src.currency_trade_id_repository import SqliteCurrencyTradeIdRepository, AlreadySavedCurrencyTradeIdError
from tests.currency_trade_id_mother import CurrencyTradeIdMother


class TestSqliteCurrencyTradeIdRepository:

    @classmethod
    def setup_class(cls):
        cls.database_path = Path("test.db")
        cls.db_connection = sqlite3.connect(cls.database_path)

    @classmethod
    def setup_method(cls):
        cursor = cls.db_connection.cursor()
        cursor.execute("PRAGMA table_info(currency_trade_ids)")
        if cursor.fetchall():
            cls.db_connection.execute("DELETE FROM currency_trade_ids")
            cls.db_connection.commit()

    @classmethod
    def teardown_class(cls):
        if cls.database_path.exists():
            os.remove(cls.database_path)

    def assert_id_in_database(self, currency_trade_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM currency_trade_ids WHERE id = ?", (str(currency_trade_id),))
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == str(currency_trade_id)


    def test_currency_trade_id_is_correctly_added(self):
        repository = SqliteCurrencyTradeIdRepository(db_connection=self.db_connection)
        currency_trade_id = CurrencyTradeIdMother.get_valid()

        repository.add_currency_trade_id(currency_trade_id)
        self.assert_id_in_database(currency_trade_id)

    def test_error_raised_when_currency_trade_id_already_exists(self):
        repository = SqliteCurrencyTradeIdRepository(db_connection=self.db_connection)
        currency_trade_id = CurrencyTradeIdMother.get_valid()

        repository.add_currency_trade_id(currency_trade_id)

        with pytest.raises(AlreadySavedCurrencyTradeIdError):
            repository.add_currency_trade_id(currency_trade_id)
