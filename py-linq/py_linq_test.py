import unittest
from py_linq import *

class Test_py_linq_test(unittest.TestCase):
    def test_iterating_the_enumerable(self):
        it = Enumerable([1,2,3])
        source = [i for i in it]
        self.assertCountEqual(source,[1,2,3])

    def test_simple_where(self):
        it = Enumerable([1,2,3,4,5,6,7,8,9,10]).Where(lambda x : x >= 10)
        source = [i for i in it]
        self.assertCountEqual(source,[10])

    def test_concatenated_where(self):
        it = Enumerable([1,2,3,4,5,6,7,8,9,10]).Where(lambda x : x >= 5).Where(lambda x : x % 2 == 0)
        source = [i for i in it]
        self.assertCountEqual(source,[6,8,10])

if __name__ == '__main__':
    unittest.main()
