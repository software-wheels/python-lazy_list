from typing import *

class NotCallableException(Exception):
    def __init__(self, object: object) -> None:
        super().__init__(f"Got non-callable object: {repr(object)}, from type: {type(object)}")

class LazyList(Sequence):
    def __init__(self) -> None:


        raise NotImplementedError("Use the static methods below to create the object")
    
    @staticmethod
    def from_callable(o: Callable):
        if callable(o):
            return _LazyListFromCallable(callable=o)
        else:
            raise NotCallableException(object=o)

    @staticmethod
    def with_transformer(sequence: Sequence, transformer: Callable[[Any], Any]):
        if callable(transformer):
            return _LazyListWithTransformer(sequence=sequence, transformer=transformer)
        else:
            raise NotCallableException(object=transformer) 
        
class _LazyListFromCallable(LazyList):

    def __init__(self, callable: Callable) -> None:
        self.__iteration_index = 0
        self.__callable = callable
        self.__ind_map = {}

    def __getitem__(self, ind: Union[int, slice]):
        if isinstance(ind, slice):
            ifnone = self.__if_none
            return [self[i] for i in range(ifnone(ind.start, 0), ind.stop, ifnone(ind.step, 1))]
        try:
            return self.__ind_map[ind]
        except KeyError:
            self.__ind_map[ind] = self.__callable(ind)
        return self.__ind_map[ind]
    
    def __iter__(self):
        return self

    def __next__(self):
        # when itereting on a lazy list, the iterator will start from 0 until get StopIteration Exception
        item = None
        try:
            item = self[self.__iteration_index]
        except IndexError:
            raise StopIteration()
        self.__iteration_index += 1
        return item
    
    def evaluate_all(self):
        return [n for n in self]
    
    def __len__(self):
        # will evaluate all the list items
        return len(self.evaluate_all())
    
    def __contains__(self, value: object) -> bool:
        for item in self:
            try:
                if value == item:
                    return True
                continue
            except IndexError:
                return False
    
    def index(self, value: Any, start: int = 0, stop: int = None) -> int:
        ind = start
        while stop is None or ind < stop:
            try:
                if self[ind] == value:
                    return ind
            except IndexError:
                break
            ind += 1
        return None
            
    def __repr__(self):
        return repr(self.evaluate_all())
    
    @staticmethod
    def __if_none(a, b):
        return b if a is None else a
    
class _LazyListWithTransformer(_LazyListFromCallable):
    def __init__(self, sequence: Sequence, transformer: Callable[[Any], Any]) -> None:
        def callable(i: int):
            if i < len(sequence):
                return transformer(sequence[i]) 
            raise IndexError(i)
        
        super().__init__(callable)

    