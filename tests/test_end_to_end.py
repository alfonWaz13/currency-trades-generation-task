import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from unittest import mock

import mysql.connector
import pytest

import config
from src.currency_trade_id_repository import MySqlCurrencyTradeIdRepository
from src.generation import CurrencyTradeIdGenerator


class TestEndToEnd:

    @classmethod
    def setup_class(cls):
        cls.connection_configuration = config.MySqlConfig.to_dict()
        cls.repository = MySqlCurrencyTradeIdRepository(connection_configuration=cls.connection_configuration)
        cls.currency_trade_id_generator = CurrencyTradeIdGenerator(repository=cls.repository)

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

    @pytest.mark.timeout(6000)
    def test_generate_bulk_performance(self):

        with mock.patch('src.currency_trade_id.currency_trade_id.ID_CHARACTERS', '0ABCDEFG'), \
                mock.patch('src.generation.ID_CHARACTERS', '0ABCDEFG'):
            self.currency_trade_id_generator.generate_bulk(2097100)
