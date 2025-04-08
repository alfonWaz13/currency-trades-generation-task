from mysql.connector import pooling, IntegrityError
from mysql.connector.pooling import PooledMySQLConnection

from src.currency_trade_id import CurrencyTradeId

from .exceptions import (AlreadySavedCurrencyTradeIdError, MultipleCurrencyTradeInsertionError,
                         EmptyCurrencyTradeIdException)
from .currency_trade_id_repository import CurrencyTradeIdRepository


class MySqlCurrencyTradeIdRepository(CurrencyTradeIdRepository):

    _currency_trade_id_table = "currency_trades"
    _id_column = "id"

    def __init__(self, connection_configuration: dict):
        self.pool = pooling.MySQLConnectionPool(
            pool_size=10,
            pool_reset_session=True,
            **connection_configuration
        )
        self._initialize_table()

    def _initialize_table(self) -> None:
        with self.pool.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._currency_trade_id_table} (
                    {self._id_column} VARCHAR(10) PRIMARY KEY
                )
            """)
            connection.commit()

    def add_currency_trade_id(self, currency_trade_id: CurrencyTradeId) -> None:
        try:
            with self.pool.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    f"INSERT INTO {self._currency_trade_id_table} ({self._id_column}) VALUES (%s)",
                    (str(currency_trade_id),)
                )
                connection.commit()
        except IntegrityError:
            raise AlreadySavedCurrencyTradeIdError(currency_trade_id=currency_trade_id)

    def add_bulk_currency_trade_ids(self, currency_trade_ids: set[CurrencyTradeId]) -> None:

        values = [(str(currency_trade_id),) for currency_trade_id in currency_trade_ids]
        query = f"INSERT INTO {self._currency_trade_id_table} ({self._id_column}) VALUES (%s)"
        with self.pool.get_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.executemany(query, values)
                connection.commit()
            except IntegrityError:
                duplicated_ids = self._get_duplicated_currency_trade_ids(connection, currency_trade_ids)
                raise MultipleCurrencyTradeInsertionError(currency_trade_ids=duplicated_ids)

    def _get_duplicated_currency_trade_ids(self,
                                           connection: PooledMySQLConnection,
                                           currency_trade_ids: set[CurrencyTradeId]
                                           ) -> set[CurrencyTradeId]:

        placeholders = ",".join(["%s"] * len(currency_trade_ids))
        query = f"""
                    SELECT {self._id_column}
                    FROM {self._currency_trade_id_table}
                    WHERE {self._id_column} IN ({placeholders})
                """

        cursor = connection.cursor()
        cursor.execute(query, [str(t) for t in currency_trade_ids])

        return {CurrencyTradeId(row[0]) for row in cursor.fetchall()}

    def get_last_currency_trade_id(self) -> CurrencyTradeId:
        with self.pool.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT {self._id_column} FROM {self._currency_trade_id_table} ORDER BY {self._id_column} DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                return CurrencyTradeId(row[0])
            raise EmptyCurrencyTradeIdException()
