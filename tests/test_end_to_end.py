import os
import sqlite3
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.currency_trade_id_repository import SqliteCurrencyTradeIdRepository
from src.generation import CurrencyTradeIdGenerator


class TestEndToEnd:

    @classmethod
    def setup_class(cls):
        cls.database_path = Path("test.db")
        cls.repository = SqliteCurrencyTradeIdRepository(db_path=cls.database_path)
        cls.currency_trade_id_generator = CurrencyTradeIdGenerator(repository=cls.repository)

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


    def test_ids_returned_by_generator_are_unique(self):
        ids = set()
        for _ in range(0, 10):
            ids.add(self.currency_trade_id_generator.generate())

        assert len(ids) == 10

    def test_ids_are_unique_generated_in_bulk(self):
        generated_ids = set()
        generated_count = 0
        while generated_count < 100:
            generated_ids.update(self.currency_trade_id_generator.generate_bulk(1000))
            generated_count += 1
            assert len(generated_ids) == generated_count * 1000

    def test_concurrent_bulk_generation_generates_unique_ids_without_errors_with_concurrency(self):
        generated_ids = set()
        bulk_args = [2500] * 2000

        def consumer_function(ids):
            return list(ids)

        with ThreadPoolExecutor(max_workers=9) as pool:
            generators = pool.map(self.currency_trade_id_generator.generate_bulk, bulk_args)
            ids = pool.map(consumer_function, generators)

            for chunk in ids:
                generated_ids.update(chunk)

        assert len(generated_ids) == 5_000_000

    def test_restarting_process_does_not_duplicate_ids(self):
        ids = set()
        env = os.environ.copy()
        env['PYTHONPATH'] = os.getcwd() + ':' + env.get('PYTHONPATH', '')

        process = subprocess.Popen(
            ["/usr/bin/env", "python", "-u", "-m", "scripts.infinite_generation"],
            stdout=subprocess.PIPE,
            env=env)
        time.sleep(2)
        process.kill()
        for incoming_id in process.stdout.readlines():
            incoming_id = incoming_id.strip()
            ids.add(incoming_id)

        process = subprocess.Popen(
            ["/usr/bin/env", "python", "-u", "-m", "scripts.infinite_generation"],
            stdout=subprocess.PIPE,
            env=env)
        time.sleep(2)
        process.kill()
        for incoming_id in process.stdout.readlines():
            incoming_id = incoming_id.strip()
            # Here's our duplicate check. Restarting the process should
            # not duplicate the ids we get from it.
            assert incoming_id not in ids
            ids.add(incoming_id)
        # And we should have got at least 2
        assert len(ids) > 1
