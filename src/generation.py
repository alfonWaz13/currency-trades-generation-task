from src import currency_trade_id_repository
from src.currency_trade_id import CurrencyTradeId, ID_CHARACTERS, CURRENCY_TRADES_ID_LENGTH


class CurrencyTradeIdGenerator:
    def __init__(self, repository: currency_trade_id_repository.CurrencyTradeIdRepository):
        self.repository = repository

    def generate(self):
        currency_trade_id = None

        while not currency_trade_id:
            currency_trade_id = self._get_sorted_currency_trade_id()
            try:
                self.repository.add_currency_trade_id(currency_trade_id)
            except currency_trade_id_repository.AlreadySavedCurrencyTradeIdError:
                currency_trade_id = None

        return currency_trade_id

    def generate_bulk(self, number_of_ids: int) -> set[CurrencyTradeId]:
        new_currency_trade_ids = set()
        currency_trade_ids_to_insert = set()

        while len(new_currency_trade_ids) < number_of_ids:

            number_new_currency_trades_to_generate = number_of_ids - len(new_currency_trade_ids) - len(currency_trade_ids_to_insert)
            currency_trade_ids_to_insert.update(self._get_multiple_sorted_currency_trade_ids(number_new_currency_trades_to_generate))

            try:
                self.repository.add_bulk_currency_trade_ids(currency_trade_ids_to_insert)
                new_currency_trade_ids.update(currency_trade_ids_to_insert)
                currency_trade_ids_to_insert = set()
            except currency_trade_id_repository.MultipleCurrencyTradeInsertionError as exception:
                duplicated_ids = exception.already_saved_currency_trade_ids
                currency_trade_ids_to_insert.difference_update(duplicated_ids)

        return new_currency_trade_ids

    def _get_sorted_currency_trade_id(self) -> CurrencyTradeId:
        """It searches for the last stored currency trade id and generates the next one in a sorted sequence."""
        try:
            last_currency_trade_id_stored = self.repository.get_last_currency_trade_id()
        except currency_trade_id_repository.EmptyCurrencyTradeIdException:
            return CurrencyTradeId(ID_CHARACTERS[0] * CURRENCY_TRADES_ID_LENGTH)

        return self._get_next_currency_trade_id_in_sequence(last_currency_trade_id_stored)

    def _get_multiple_sorted_currency_trade_ids(self, number_of_ids: int) -> set[CurrencyTradeId]:
        sorted_currency_trade_ids = set()
        next_currency_trade_id = self._get_sorted_currency_trade_id()
        sorted_currency_trade_ids.add(next_currency_trade_id)

        while len(sorted_currency_trade_ids) < number_of_ids:
            next_currency_trade_id = self._get_next_currency_trade_id_in_sequence(next_currency_trade_id)
            sorted_currency_trade_ids.add(next_currency_trade_id)

        return sorted_currency_trade_ids

    @classmethod
    def _get_next_currency_trade_id_in_sequence(cls, previous_id: CurrencyTradeId) -> CurrencyTradeId:
        """Using the last stored currency trade id, it generates the next one in a sorted sequence according to the
        order of the characters in the ID_CHARACTERS patterns.
        I.e. For the next pattern: 'ABCDEFGH', and 7 as CURRENCY_TRADES_ID_LENGTH:
        - previous_id = 'AABDFFA' ==> new_id = 'AABDFFB', only last digit is updated
        - previous_id = 'AABDFFH' ==> new_id = 'AABDFGA', last two digits are updated
        - previous_id = 'AHHHHHH' ==> new_id = 'BAAAAAAA', all digits are updated
        """
        digits_to_update = 1
        new_id_termination = []

        while previous_id.get_final_digits(digits_to_update)[0] == ID_CHARACTERS[-1]:
            new_id_termination.insert(0, ID_CHARACTERS[0])
            digits_to_update += 1

        character_last_digit_to_update = previous_id.get_final_digits(digits_to_update)[0]
        index_last_digit_to_update = ID_CHARACTERS.index(character_last_digit_to_update)
        new_character = ID_CHARACTERS[index_last_digit_to_update + 1]
        new_id_termination.insert(0, new_character)

        new_id_beginning = previous_id.get_initial_digits(CURRENCY_TRADES_ID_LENGTH - len(new_id_termination))
        new_id = new_id_beginning + ''.join(new_id_termination)

        return CurrencyTradeId(new_id)
