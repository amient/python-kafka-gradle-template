import unittest
import os

class Test(unittest.TestCase):

    def testExample(self):

        self.assertGreater(os.environ['KAFKA_PORT'], "")
        self.assertGreater(os.environ['SCHEMA_REGISTRY_PORT'], "")
        self.assertEqual(2 * 2 , 4, "2x2 sholud be 4")


if __name__ == "__main__":
    unittest.main()