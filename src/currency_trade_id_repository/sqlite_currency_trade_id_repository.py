import sqlite3
from sqlite3 import IntegrityError

from src.currency_trade_id import CurrencyTradeId

from .currency_trade_id_repository import CurrencyTradeIdRepository
from .exceptions import AlreadySavedCurrencyTradeIdError



class SqliteCurrencyTradeIdRepository(CurrencyTradeIdRepository):

    _currency_trade_id_table = "currency_trade_ids"
    _id_column = "id"

    def __init__(self, db_connection: sqlite3.Connection):
        self.db_connection = db_connection

        self._initialize_table()

    def _initialize_table(self) -> None:
        cursor = self.db_connection.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self._currency_trade_id_table} (
                {self._id_column} TEXT PRIMARY KEY
            )
        """)
        self.db_connection.commit()

    def add_currency_trade_id(self, currency_trade_id: CurrencyTradeId) -> None:
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(f"INSERT INTO {self._currency_trade_id_table} ({self._id_column}) VALUES (?)",
                           (str(currency_trade_id),))
            self.db_connection.commit()
        except IntegrityError:
            raise AlreadySavedCurrencyTradeIdError(currency_trade_id=currency_trade_id)
