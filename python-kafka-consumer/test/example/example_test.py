import unittest
#from sklearn import datasets


class Test(unittest.TestCase):

    def testExample(self):

        self.assertEqual(2 * 2 , 4, "2x2 sholud be 4")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testIrisDataset']
    unittest.main()