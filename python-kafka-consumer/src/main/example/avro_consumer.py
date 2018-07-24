from confluent_kafka import KafkaError
from confluent_kafka import avro
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.serializer import SerializerError
import os

KAFKA_BOOTSTRAP_SERVERS = os.environ['KAFKA_BOOTSTRAP_SERVERS']
SCHEMA_REGISTRY_URL = os.environ['SCHEMA_REGISTRY_URL']

SCHEMA=avro.load(os.path.join(os.path.dirname(__file__), '../resources/value_schema.avsc'))
INPUT_TOPIC='test-input'
OUTPUT_TOPIC='test-output'

def main():

    print("Creating Avro Producer")
    p = AvroProducer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS, 'schema.registry.url': SCHEMA_REGISTRY_URL})

    print("Creating Avro Consumer")
    c = AvroConsumer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS, 'group.id': 'example', 'schema.registry.url': SCHEMA_REGISTRY_URL})
    c.subscribe([INPUT_TOPIC])

    running = True
    print("Running Mirror Loop")
    while running:
        msg = c.poll(1)
        try:
            if msg:
                if not msg.error():
                    p.produce(topic=OUTPUT_TOPIC, key=None, value=msg.value(), key_schema=None, value_schema=SCHEMA)

                elif msg.error().code() != KafkaError._PARTITION_EOF:
                    print(msg.error())
                    running = False
        except SerializerError as e:
            print("Message deserialization failed for %s: %s" % (msg, e))
            running = False

    c.close()

