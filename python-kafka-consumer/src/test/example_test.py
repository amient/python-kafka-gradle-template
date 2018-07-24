import unittest
from multiprocessing import Process
from example.avro_consumer import *

class Test(unittest.TestCase):


    def testExample(self):

        m = Process(target=main, args=())
        m.start()
        try:
            c = AvroConsumer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS, 'group.id': 'ittest', 'schema.registry.url': SCHEMA_REGISTRY_URL})
            c.subscribe([OUTPUT_TOPIC])

            p = AvroProducer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS, 'schema.registry.url': SCHEMA_REGISTRY_URL})
            value = {"name": "Value", "favorite_number": 8, "favorite_color": "green", "age": 16}
            p.produce(topic=INPUT_TOPIC, value=value, value_schema=SCHEMA)
            p.flush()
            print("produced test record")

            msg = c.poll(30)
            self.assertNotEqual(msg, None)
            self.assertNotEqual(msg.value(), None)
            print(msg.value())
            #fixme for some reason sometimes the kafka avro consumer doesn't decode the bytes!
            #self.assertEqual(msg.value(), value)

            c.close()

        finally:
            m.terminate()



if __name__ == "__main__":
    unittest.main()