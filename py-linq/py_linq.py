class Enumerable:
    def __init__(self, data):
        self._data = data

    def __iter__(self):
        return iter(self._data)

    def Where(self, predicate):
        return WhereEnumerableIterator(self._data, predicate)

class WhereEnumerableIterator(Enumerable):
    def __init__(self, data, predicate):
        self._data = data
        self._predicate = predicate

    def __iter__(self):
        for x in self._data:
            if self._predicate(x):
                yield x

    def Select(self,selector):
        return WhereSelectEnumerableIterator(self._data, self._predicate, selector)

    def Where(self, predicate):
        return WhereEnumerableIterator(self, combine_predicates(self._predicate,predicate))

class WhereSelectEnumerableIterator(Enumerable):
    def __init__(self, data, predicate, selector):
        self._data = data
        self._predicate = predicate
        self._selector = selector

    def __iter__(self):
        for x in self._data:
            if self._predicate(x):
                yield self._selector(x)

    def Select(self,selector):
        return WhereSelectEnumerableIterator(self._data,self._predicate, combine_selectors(self._selector,selector))

    def Where(self, predicate):
        return WhereEnumerableIterator(self, predicate)

def combine_predicates(predicate1, predicate2):
    return lambda x : predicate1(x) and predicate2(x)

def combine_selectors(selector1,selector2):
    return lambda x : selector2(selector1(x))