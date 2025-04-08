from src.generation import generate


def test_ids_are_unique():
    ids = set()
    for i in range(0, 10):
        ids.add(generate())

    assert len(ids) == 10
