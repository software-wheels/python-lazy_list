from ..lazy_list import LazyList

def test_simple_transformer():
    original_list = [1, 2, 3, 4]
    lazy_list = LazyList.from_transformer(original_list, transformer=lambda n: n ** 2)

    assert lazy_list[0] == 1
    assert lazy_list[1] == 4   
    assert lazy_list[2] == 9 

def test_only_once_and_require_indexes():
    called_objects = []
    original_list = ["a", "b", "c", "d"]
    def track_calls(c: str):
        called_objects.append(c)

    lazy_list = LazyList.from_transformer(original_list, transformer=track_calls)

    lazy_list[0]
    lazy_list[2]
    lazy_list[2]
    lazy_list[3]
    lazy_list[0]

    assert called_objects == ["a", "c", "d"]

def test_complex_access():
    original_list = range(10)
    lazy_list = LazyList.from_transformer(original_list, transformer=lambda n: n ** 2)

    assert lazy_list[2:6] == [n ** 2 for n in [2, 3, 4, 5]]
