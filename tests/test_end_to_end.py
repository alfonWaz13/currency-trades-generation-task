from src.currency_trade_id_repository import MemoryCurrencyTradeIdRepository
from src.generation import CurrencyTradeIdGenerator


class TestEndToEnd:

    @classmethod
    def setup_class(cls):
        cls.repository = MemoryCurrencyTradeIdRepository()
        cls.currency_trade_id_generator = CurrencyTradeIdGenerator(repository=cls.repository)


    def test_ids_returned_by_generator_are_unique(self):
        ids = set()
        for _ in range(0, 10):
            ids.add(self.currency_trade_id_generator.generate())

        assert len(ids) == 10
