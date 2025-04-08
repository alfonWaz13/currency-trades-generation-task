import re
from src.generation import generate, ID_CHARACTERS


def test_id_is_the_correct_length():
    assert len(generate()) == 7


def test_id_uses_correct_characters():
    generated_id = str(generate())
    check = re.compile('^[' + ID_CHARACTERS + ']+$')
    assert check.match(generated_id) is not None


def test_ids_are_unique():
    ids = set()
    for i in range(0, 10):
        ids.add(generate())

    assert len(ids) == 10
