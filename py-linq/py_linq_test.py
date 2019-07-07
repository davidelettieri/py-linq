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

    def test_where_after_select(self):
        class Test:
            def __init__(self, data):
                self.Data = data
            def __eq__(self, other):
                return self.Data == other.Data

        it = Enumerable([1,2,3,4,5,6,7,8,9,10]).Select(lambda x : Test(x)).Where(lambda x : x.Data >= 10)
        source = [i for i in it]
        self.assertEqual(len(source),1)
        self.assertEqual(source[0], Test(10))

    def test_take_1(self):
        it = Enumerable([1,2,3,4,5,6,7,8,9,10]).Take(1)
        source = [i for i in it]
        self.assertEqual(len(source),1)
        self.assertEqual(source[0], 1)

    def test_take_2(self):
        it = Enumerable([1,2,3,4,5,6,7,8,9,10]).Take(2)
        source = [i for i in it]
        self.assertEqual(len(source),2)
        self.assertEqual(source[0], 1)
        self.assertEqual(source[1], 2)

    def test_skip_1(self):
        it = Enumerable([1,2,3,4,5,6,7,8,9,10]).Skip(1)
        source = [i for i in it]
        self.assertEqual(len(source),9)
        self.assertEqual(source[0], 2)

    def test_skip_1_take_2(self):
        it = Enumerable([1,2,3,4,5,6,7,8,9,10]).Skip(1).Take(2)
        source = [i for i in it]
        self.assertEqual(len(source),2)
        self.assertEqual(source[0], 2)
        self.assertEqual(source[1], 3)

    def test_take_while(self):
        it = Enumerable([1,2,3,4,5,6,7,8,9,10]).TakeWhile(lambda x: x < 5)
        source = [i for i in it]
        self.assertEqual(len(source),4)
        self.assertEqual(source[0], 1)
        self.assertEqual(source[1], 2)
        self.assertEqual(source[2], 3)
        self.assertEqual(source[3], 4)

    def test_skip_while(self):
        it = Enumerable([1,2,3,4,5,6,7,8,9,10]).SkipWhile(lambda x: x <= 5)
        source = [i for i in it]
        self.assertEqual(len(source),5)
        self.assertEqual(source[0], 6)
        self.assertEqual(source[1], 7)
        self.assertEqual(source[2], 8)
        self.assertEqual(source[3], 9)
        self.assertEqual(source[4], 10)

    def test_skipwhile_takewhile(self):
        it = Enumerable([1,2,3,4,5,6,7,8,9,10]).SkipWhile(lambda x: x <= 5).TakeWhile(lambda x: x < 9)
        source = [i for i in it]
        self.assertEqual(len(source),3)
        self.assertEqual(source[0], 6)
        self.assertEqual(source[1], 7)
        self.assertEqual(source[2], 8)

    def test_selectmany(self):
        it = Enumerable([1,2,3,4,5,6,7,8,9,10]).SelectMany(lambda x: range(x))
        source = [i for i in it]
        self.assertEqual(len(source),55)


    def test_where_doesnt_change_source(self):
        start = Enumerable([1,2,3,4,5,6,7,8,9,10])
        a = start.Where(lambda x: x > 5)
        b = start.Where(lambda x: x <= 5)

        start_source = [i for i in start]
        a_source = [i for i in a]
        b_source = [i for i in b]

        self.assertEqual(len(start_source),10)
        self.assertEqual(len(a_source),5)
        self.assertEqual(len(b_source),5)

    def test_group_by(self):
        start = Enumerable([1,2,3,4,5,6,7,8,9,10]).GroupBy(lambda x: x % 2)

        source = [i for i in start]

        self.assertEqual(len(source),2)

        self.assertEqual(len(a),2)


if __name__ == '__main__':
    unittest.main()
