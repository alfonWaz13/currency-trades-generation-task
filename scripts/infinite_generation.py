import sys

from src.currency_trade_id_repository import MemoryCurrencyTradeIdRepository
from src.generation import CurrencyTradeIdGenerator

repository = MemoryCurrencyTradeIdRepository()
generator = CurrencyTradeIdGenerator(repository)


while True:
    for id in generator.generate_bulk(10):
        sys.stdout.write('%s\n' % id)
