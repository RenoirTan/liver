from typing import Iterator, TypeVar, Callable


T = TypeVar("T")


def find_first(iterator: Iterator[T], predicate: Callable[[T], bool]) -> T:
    return next(x for x in iterator if predicate(x))


def index_first(iterator: Iterator[T], predicate: Callable[[T], bool]) -> int:
    try:
        i, x = find_first(enumerate(iterator), lambda ix: predicate(ix[1]))
        return i
    except StopIteration:
        return -1
