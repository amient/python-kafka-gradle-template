from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

# from kafka import KafkaConsumer

KAFKA_TOPIC = 'test'
KAFKA_BROKERS = 'localhost:19092'  # see step 1
SCHEMA_REGITRY = 'http://localhost:18081'


def main():

    c = AvroConsumer(
        {'bootstrap.servers': KAFKA_BROKERS, 'group.id': 'test',
            'schema.registry.url': SCHEMA_REGITRY})

    c.subscribe([KAFKA_TOPIC])

    running = True
    while running:
        msg = c.poll(10)
        try:
            if msg:
                if not msg.error():
                    print(msg.key())
                    print(msg.value())
                elif msg.error().code() != KafkaError._PARTITION_EOF:
                    print(msg.error())
                    running = False
        except SerializerError as e:
            print("Message deserialization failed for %s: %s" % (msg, e))
            running = False

    c.close()
