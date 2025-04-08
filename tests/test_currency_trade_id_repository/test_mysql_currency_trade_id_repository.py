import mysql.connector
import pytest

import config
from src.currency_trade_id_repository import MySqlCurrencyTradeIdRepository, exceptions
from tests.currency_trade_id_mother import CurrencyTradeIdMother


class TestMySqlCurrencyTradeIdRepository:

    @classmethod
    def setup_class(cls):
        cls.connection_configuration = config.MySqlConfig.to_dict()

    @classmethod
    def setup_method(cls):
        connection = mysql.connector.connect(**cls.connection_configuration)
        cursor = connection.cursor()

        cursor.execute("SHOW TABLES LIKE 'currency_trades'")

        if cursor.fetchone():
            cursor.execute("DELETE FROM currency_trades")
            connection.commit()

        cursor.close()
        connection.close()

    def assert_id_in_database(self, currency_trade_id):

        connection = mysql.connector.connect(**self.connection_configuration)
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM currency_trades WHERE id = %s", (str(currency_trade_id),))
        row = cursor.fetchone()

        cursor.close()
        connection.close()

        assert row is not None
        assert row[0] == str(currency_trade_id)


    def test_currency_trade_id_is_correctly_added(self):
        repository = MySqlCurrencyTradeIdRepository(connection_configuration=self.connection_configuration)
        currency_trade_id = CurrencyTradeIdMother.get_valid()

        repository.add_currency_trade_id(currency_trade_id)
        self.assert_id_in_database(currency_trade_id)

    def test_error_raised_when_currency_trade_id_already_exists(self):
        repository = MySqlCurrencyTradeIdRepository(connection_configuration=self.connection_configuration)
        currency_trade_id = CurrencyTradeIdMother.get_valid()

        repository.add_currency_trade_id(currency_trade_id)

        with pytest.raises(exceptions.AlreadySavedCurrencyTradeIdError):
            repository.add_currency_trade_id(currency_trade_id)

    def test_bulk_currency_trade_ids_are_correctly_added(self):
        repository = MySqlCurrencyTradeIdRepository(connection_configuration=self.connection_configuration)
        currency_trade_ids = {CurrencyTradeIdMother.get_valid() for _ in range(10)}

        repository.add_bulk_currency_trade_ids(currency_trade_ids)

        for currency_trade_id in currency_trade_ids:
            self.assert_id_in_database(currency_trade_id)

    def test_error_raised_when_duplicated_currency_trade_ids_are_added_in_bulk(self):
        repository = MySqlCurrencyTradeIdRepository(connection_configuration=self.connection_configuration)
        currency_trade_id_1 = CurrencyTradeIdMother.get_valid()
        currency_trade_id_2 = CurrencyTradeIdMother.get_valid()
        currency_trade_id_3 = CurrencyTradeIdMother.get_valid()

        repository.add_bulk_currency_trade_ids({currency_trade_id_1, currency_trade_id_2, currency_trade_id_3})

        with pytest.raises(exceptions.MultipleCurrencyTradeInsertionError) as exception:
            repository.add_bulk_currency_trade_ids({currency_trade_id_1, currency_trade_id_2})

        assert currency_trade_id_1 in exception.value.already_saved_currency_trade_ids
        assert currency_trade_id_2 in exception.value.already_saved_currency_trade_ids
