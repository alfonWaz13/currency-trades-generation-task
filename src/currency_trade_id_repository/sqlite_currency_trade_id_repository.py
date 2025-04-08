import sqlite3
import threading
from pathlib import Path
from sqlite3 import IntegrityError

from src.currency_trade_id import CurrencyTradeId

from .currency_trade_id_repository import CurrencyTradeIdRepository
from .exceptions import AlreadySavedCurrencyTradeIdError, MultipleCurrencyTradeInsertionError


class SqliteCurrencyTradeIdRepository(CurrencyTradeIdRepository):

    _currency_trade_id_table = "currency_trade_ids"
    _id_column = "id"

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._threading_lock = threading.Lock()

        self._initialize_table()

    def _initialize_table(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._currency_trade_id_table} (
                    {self._id_column} TEXT PRIMARY KEY
                )
            """)
            connection.commit()

    def add_currency_trade_id(self, currency_trade_id: CurrencyTradeId) -> None:
        try:
            with self._threading_lock, sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO {self._currency_trade_id_table} ({self._id_column}) VALUES (?)",
                               (str(currency_trade_id),))
                connection.commit()
        except IntegrityError:
            raise AlreadySavedCurrencyTradeIdError(currency_trade_id=currency_trade_id)

    def add_bulk_currency_trade_ids(self, currency_trade_ids: set[CurrencyTradeId]) -> None:
        with self._threading_lock, sqlite3.connect(self.db_path) as connection:
            try:
                cursor = connection.cursor()
                cursor.executemany(
                    f"INSERT INTO {self._currency_trade_id_table} ({self._id_column}) VALUES (?)",
                    [(str(currency_trade_id),) for currency_trade_id in currency_trade_ids]
                )
                connection.commit()
            except IntegrityError:
                duplicated_ids = self._get_duplicated_currency_trade_ids(connection, currency_trade_ids)
                raise MultipleCurrencyTradeInsertionError(duplicated_ids)

    def _get_duplicated_currency_trade_ids(self, connection: sqlite3.Connection,
                                           currency_trade_ids: set[CurrencyTradeId]) -> set[CurrencyTradeId]:
        cursor = connection.cursor()
        placeholders = ",".join("?" for _ in currency_trade_ids)
        query = f"""
                    SELECT {self._id_column}
                    FROM {self._currency_trade_id_table}
                    WHERE {self._id_column} IN ({placeholders})
                """
        cursor.execute(query, [str(c) for c in currency_trade_ids])
        rows = cursor.fetchall()
        duplicated_ids = {CurrencyTradeId(row[0]) for row in rows}
        return duplicated_ids