from ..lazy_list import LazyList, NotCallableException
from typing import *

class CallsManager:
    def __init__(self) -> None:
        self.__calls = []
    
    def call(self, index: int):
        self.__calls.append(index)

    def get_calles(self) -> List[int]:
        return self.__calls
    
def test_argument_not_callable():
    try:
        LazyList.from_callable(None)
    except NotCallableException:
        return
    assert False, "An exception should have been thrown since 'None' is not callable"

def _get_square_lazy_list(up_limit=None):
    def callable(n):
        if up_limit is not None and n > up_limit:
            raise IndexError(n)
        return n ** 2

    lazy_list = LazyList.from_callable(callable)
    return lazy_list

def test_simple_index_access():
    lazy_list = _get_square_lazy_list()

    assert lazy_list[2] == 4
    assert lazy_list[-2] == 4
    assert lazy_list[0] == 0

def test_range():
    lazy_list = _get_square_lazy_list()

    assert lazy_list[1:1] == []
    assert lazy_list[2:3] == [4]
    assert lazy_list[5:9] == [n ** 2 for n in [5,6,7,8]]
    assert lazy_list[0:8:2] == [n ** 2 for n in [0, 2, 4, 6]] 

def test_iter():
    lazy_list_until_10 = _get_square_lazy_list(up_limit=10)

    # when itereting on lazy list, the iterator will start from 0 until get StopIteration Exception
    assert [n for n in lazy_list_until_10] == [n ** 2 for n in range(11)]

def test_len():
    lazy_list_until_10 = _get_square_lazy_list(up_limit=10)

    assert len(lazy_list_until_10) == 11 # including 0

def test_in():
    lazy_list_until_10 = _get_square_lazy_list(up_limit=10)

    assert 81 in lazy_list_until_10 # 9 ** 2 = 81
    assert 100 in lazy_list_until_10 # 10 ** 2 = 1000
    assert 121 not in lazy_list_until_10 # the limit is 10
    assert 7 not in lazy_list_until_10

def test_index():
    lazy_list_until_10 = _get_square_lazy_list(up_limit=10)

    
    assert lazy_list_until_10.index(0) == 0
    assert lazy_list_until_10.index(49) == 7
    assert lazy_list_until_10.index(47) == None
    assert lazy_list_until_10.index(25, start=6) == None
    assert lazy_list_until_10.index(25, stop=5) == None
    assert lazy_list_until_10.index(25, start=5, stop=6) == 5

def test_only_require_index_and_only_once():
    called_indexes = []

    def call(index):
        called_indexes.append(index)

    lazy_list = LazyList.from_callable(call)


    lazy_list[1]
    lazy_list[1]
    lazy_list[2]
    lazy_list[3]
    lazy_list[5]
    lazy_list[8]
    lazy_list[13]
    lazy_list[8]
    lazy_list[5]
    lazy_list[3]
    lazy_list[2]
    lazy_list[1]
    lazy_list[1]

    assert called_indexes == [1, 2, 3, 5, 8, 13]



    
        
