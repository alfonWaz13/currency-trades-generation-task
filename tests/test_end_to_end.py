from concurrent.futures import ThreadPoolExecutor

from src.currency_trade_id_repository import MemoryCurrencyTradeIdRepository
from src.generation import CurrencyTradeIdGenerator


class TestEndToEnd:

    @classmethod
    def setup_class(cls):
        cls.repository = MemoryCurrencyTradeIdRepository()
        cls.currency_trade_id_generator = CurrencyTradeIdGenerator(repository=cls.repository)

    @classmethod
    def setup_method(cls):
        cls.repository._currency_trade_ids = set()


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

    def test_concurrent_bulk_generation(self):
        generated_ids = set()
        bulk_args = []
        for _ in range(0, 2000):
            bulk_args.append(2500)

        def consumer_function(ids):
            return list(ids)

        with ThreadPoolExecutor(max_workers=9) as pool:
            generators = list(pool.map(self.currency_trade_id_generator.generate_bulk, bulk_args))
            ids = list(pool.map(consumer_function, generators))

            for chunk in ids:
                generated_ids.update(chunk)

        assert len(generated_ids) == 5000000

