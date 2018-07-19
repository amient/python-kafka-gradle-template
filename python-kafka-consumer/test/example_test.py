import unittest
import os
from multiprocessing import Process
from example.avro_consumer import main

class Test(unittest.TestCase):

    def testExample(self):

        self.assertGreater(os.environ['KAFKA_PORT'], "")
        self.assertGreater(os.environ['SCHEMA_REGISTRY_PORT'], "")

        p = Process(target=main, args=())
        p.start()

        self.assertEqual(2 * 2 , 4, "2x2 sholud be 4")

        p.terminate()


if __name__ == "__main__":
    unittest.main()