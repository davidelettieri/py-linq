class Enumerable:
    def __init__(self, data):
        self._data = data

    def __iter__(self):
        return iter(self._data)

    def Where(self, predicate):
        return _WhereEnumerableIterable(self, predicate)

    def Select(self, selector):
        return _WhereSelectEnumerableIterable(self, _id, selector)

    def SelectMany(self, selector):
        return _SelectManyIterable(self, selector)

    def Take(self, count):
        return _TakeIterable(self, count)

    def Skip(self, count):
        return _SkipIterable(self, count)

    def TakeWhile(self, predicate):
        return _TakeWhileIterable(self, predicate)

    def SkipWhile(self, predicate):
        return _SkipWhileIterable(self, predicate)

    def GroupBy(self, key_selector):
        return _GroupByIterable(self, key_selector,lambda x:x, lambda x:x)

class _WhereEnumerableIterable(Enumerable):
    def __init__(self, data, predicate):
        self._data = data
        self._predicate = predicate

    def __iter__(self):
        for x in self._data:
            if self._predicate(x):
                yield x

    def Select(self,selector):
        return _WhereSelectEnumerableIterable(self._data, self._predicate, selector)

    def Where(self, predicate):
        return _WhereEnumerableIterable(self, _combine_predicates(self._predicate,predicate))

class _WhereSelectEnumerableIterable(Enumerable):
    def __init__(self, data, predicate, selector):
        self._data = data
        self._predicate = predicate
        self._selector = selector

    def __iter__(self):
        for x in self._data:
            if self._predicate(x):
                yield self._selector(x)

    def Select(self,selector):
        return _WhereSelectEnumerableIterable(self._data,self._predicate, _combine_selectors(self._selector,selector))

    def Where(self, predicate):
        return _WhereEnumerableIterable(self, predicate)

class _SelectManyIterable(Enumerable):
    def __init__(self, data, selector, resultSelector=None):
        self._data = data
        if resultSelector is None:
            self._resultSelector = _id
        else:
            self._resultSelector = resultSelector

        self._selector = selector

    def __iter__(self):
        for x in self._data:
            for y in self._selector(x):
                yield self._resultSelector(y)

class _TakeIterable(Enumerable):
    def __init__(self, data, count):
        self._data = data
        self._count = count

    def __iter__(self):
        if self._count == 0:
            return

        for x in self._data:
            yield x
            self._count -= 1
            if self._count == 0:
                return

class _TakeWhileIterable(Enumerable):
    def __init__(self, data, predicate):
        self._data = data
        self._predicate = predicate

    def __iter__(self):
        for x in self._data:
            if self._predicate(x):
                yield x
            else:
                return

class _SkipIterable(Enumerable):
    def __init__(self, data, count):
        self._data = data
        self._count = count

    def __iter__(self):
        for x in self._data:
            if(self._count > 0):
                self._count-=1
                continue
            yield x

class _SkipWhileIterable(Enumerable):
    def __init__(self, data, predicate):
        self._data = data
        self._predicate = predicate

    def __iter__(self):
        skip = True
        for x in self._data:
            if skip and self._predicate(x):
                continue
            else:
                skip = False
                yield x

class _GroupByIterable(Enumerable):
    def __iter__(self):
        lookup = _Lookup.Create(self._data, self._key_selector,self._element_selector, self._result_selector)

        for x in lookup:
            yield x
    def __init__(self, data, key_selector, element_selector, result_selector):
        self._data = data
        self._key_selector = key_selector
        self._element_selector = element_selector
        self._result_selector = result_selector




class _Lookup(Enumerable):
    def __init__(self):
        self.groupings = []
        self.lastGrouping = None
        self.count = 0

    @staticmethod
    def Create(source, key_selector, element_selector, comparer):
        lookup = _Lookup()

        for el in source:
            lookup.GetGrouping(key_selector(el),True).Add(element_selector(el))


    def GetGrouping(self, item,create):
        hash_code = hash(item)

        if self.groupings:
            g = self.groupings[hash_code % self.count]

            while g is not None:
                if g.hashCode == hash_code and g.key == item:
                    return g

                g = g.hashNext()

        if create:
            index = hash_code % len(self.groupings)
            g = _Grouping()
            g.key = item
            g.hashCode = hashCode
            g.hashNext = self.groupings[index]
            self.groupings[index] = g

            if self.lastGrouping is None:
                g.next = g
            else:
                g.next = self.lastGrouping.next
                self.lastGrouping.next = g

            self.lastGrouping = g
            return g

        return None

    def __iter__(self):
        g = self.lastGrouping

        if g is not None:
            g = g.next
            first = True
            while first or g != self.lastGrouping:
                first = False
                yield g

class _Grouping(Enumerable):
    def __init__(self):
        self.key = None
        self.hashCode = None
        self.elements = [None] * 7
        self.count = 7
        self.hashNext = None
        self.next = None


    def Add(self,element):
        self.elements.append(element)
        count += 1

    def __iter__(self):
        for i in self.elements:
            yield i

    def __getitem__(self, idx):
        return self._data[idx]


def _combine_predicates(predicate1, predicate2):
    return lambda x : predicate1(x) and predicate2(x)

def _combine_selectors(selector1,selector2):
    return lambda x : selector2(selector1(x))

def _id(x):
    return x