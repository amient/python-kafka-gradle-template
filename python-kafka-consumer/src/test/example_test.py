import unittest
import threading
from example.mirror import *
from confluent_kafka.admin import AdminClient, NewTopic

class Test(unittest.TestCase):


    def testExample(self):

        # # create topics needed for the test
        # a = AdminClient({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})
        # topics = [INPUT_TOPIC, OUTPUT_TOPIC]
        # new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics]
        # fs = a.create_topics(new_topics)
        # for topic, f in fs.items():
        #     try:
        #         f.result()  # The result itself is None
        #         print("Topic {} created".format(topic))
        #     except Exception as e:
        #         print("Failed to create topic {}: {}".format(topic, e))

        programInTest = Mirror()
        t = threading.Thread(target=programInTest.main)
        t.start()
        try:
            c = AvroConsumer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
                              'group.id': 'ittest',
                              'schema.registry.url': SCHEMA_REGISTRY_URL,
                              'default.topic.config': { 'auto.offset.reset': 'smallest'},
                              'enable.partition.eof': 'false'})
            try:
                c.subscribe([OUTPUT_TOPIC])

                p = AvroProducer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS, 'schema.registry.url': SCHEMA_REGISTRY_URL})
                value = {"name": "Value", "favorite_number": 8, "favorite_color": "green", "age": 16}
                p.produce(topic=INPUT_TOPIC, value=value, value_schema=SCHEMA)
                p.flush()
                print("produced test record")

                msg = c.poll(10)
                self.assertNotEqual(msg, None)
                self.assertNotEqual(msg.value(), None)
                self.assertEqual(msg.value()["favorite_number"], 8)
                self.assertEqual(msg.value()["favorite_color"], "green")
                self.assertEqual(msg.value()["age"], 16)
            finally:
                c.close()

        finally:
            programInTest.stop(0, None)



if __name__ == "__main__":
    unittest.main()