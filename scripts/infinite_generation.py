import sys

import config
from src.currency_trade_id_repository import MySqlCurrencyTradeIdRepository
from src.generation import CurrencyTradeIdGenerator

repository = MySqlCurrencyTradeIdRepository(connection_configuration=config.MySqlConfig.to_dict())
generator = CurrencyTradeIdGenerator(repository)


while True:
    for id in generator.generate_bulk(10):
        sys.stdout.write('%s\n' % id)
