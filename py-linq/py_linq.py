class Enumerable:
    def __init__(self, data):
        self._data = data

    def __iter__(self):
        return self

    def __next__(self):
        for x in self._data:
            yield x
        raise StopIteration

    def Where(self, predicate):
        return Enumerable.WhereEnumerableIterator(self._data, predicate)

    class WhereEnumerableIterator:
        def __init__(self, data, predicate):
            self._data = data
            self._predicate = predicate

        def __iter__(self):
            for x in self._data:
                if self._predicate(x):
                    yield x

        def Select(self,selector):
            return Enumerable.WhereSelectEnumerableIterator(self._data, self._predicate, selector)

        def Where(self, predicate):
            return Enumerable.WhereEnumerableIterator(self, Enumerable.combine_predicates(self._predicate,predicate))

    class WhereSelectEnumerableIterator:
        def __init__(self, data, predicate, selector):
            self._data = data
            self._predicate = predicate
            self._selector = selector

        def __iter__(self):
            for x in self._data:
                if self._predicate(x):
                    yield self._selector(x)

        def Select(self,selector):
            return Enumerable.WhereSelectEnumerableIterator(self._data,self._predicate, Enumerable.combine_selectors(self._selector,selector))

        def Where(self, predicate):
            return Enumerable.WhereEnumerableIterator(self, predicate)

    @staticmethod
    def combine_predicates(predicate1, predicate2):
        return lambda x : predicate1(x) and predicate2(x)

    @staticmethod
    def combine_selectors(selector1,selector2):
        return lambda x : selector2(selector1(x))

a = Enumerable([1,2,3,4,5,6,7,8,9,10])
b = a.Where(lambda x : x > 5).Where(lambda x : x % 2 == 0).Select(lambda x : x * x).Select(lambda x : -x).Where(lambda x : x < -50)
print([i for i in b])