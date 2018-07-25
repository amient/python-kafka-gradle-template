from confluent_kafka import KafkaError
from confluent_kafka import avro
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.serializer import SerializerError
import os, signal

KAFKA_BOOTSTRAP_SERVERS = os.environ['KAFKA_BOOTSTRAP_SERVERS']
SCHEMA_REGISTRY_URL = os.environ['SCHEMA_REGISTRY_URL']

SCHEMA=avro.load(os.path.join(os.path.dirname(__file__), '../resources/value_schema.avsc'))
INPUT_TOPIC='test-input'
OUTPUT_TOPIC='test-output'

class Mirror():

    def __init__(self):
        self.running = True
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self, sig, frame):
        print("termination signal: " + str(sig))
        self.running = False

    def main(self):

        print("Creating Avro Consumer")
        c = AvroConsumer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
                          'group.id': 'example',
                          'default.topic.config': { 'auto.offset.reset': 'smallest'},
                          'schema.registry.url': SCHEMA_REGISTRY_URL,
                          'enable.partition.eof': 'false'})
        try:
            c.subscribe([INPUT_TOPIC], lambda consumer, partitions: print("subscribed to " + INPUT_TOPIC + " num. partitions=" + str(len(partitions))))

            print("Creating Avro Producer")
            p = AvroProducer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS, 'schema.registry.url': SCHEMA_REGISTRY_URL})

            print("Running Mirror Loop")
            while self.running:
                msg = c.poll(1)
                try:
                    if msg:
                        if not msg.error():
                            print(msg)
                            p.produce(topic=OUTPUT_TOPIC, key=None, value=msg.value(), key_schema=None, value_schema=SCHEMA)
                            p.flush()
                        else:
                            print(msg.error())
                            self.running = False
                except SerializerError as e:
                    print("Message deserialization failed for %s: %s" % (msg, e))
                    self.running = False
        finally:
            print("Closing consumer cleanly")
            c.close()


if __name__ == "__main__":
    prd=Mirror()
    prd.main()
