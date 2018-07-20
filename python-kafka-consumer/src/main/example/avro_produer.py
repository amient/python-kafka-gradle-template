from confluent_kafka import KafkaError
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.serializer import SerializerError
import os

KAFKA_TOPIC = 'test-input'
KAFKA_BROKERS = 'localhost:' + os.environ['KAFKA_PORT']
SCHEMA_REGITRY = 'http://localhost:' + os.environ['SCHEMA_REGISTRY_PORT']

value_schema = avro.load('ValueSchema.avsc')
value = {"name": "Value", "favorite_number": 10, "favorite_color": "green", "age": 25}

def main():


    print("Starting Avro Producer 2")
    p = AvroProducer({'bootstrap.servers': KAFKA_BROKERS, 'group.id': 'test', 'schema.registry.url': SCHEMA_REGITRY})
    p.produce(topic='test-input', value=value, value_schema=value_schema)
    p.flush()

main()