from confluent_kafka import KafkaError
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.serializer import SerializerError
import os

KAFKA_BROKERS = 'localhost:' + os.environ['KAFKA_PORT']
SCHEMA_REGITRY = 'http://localhost:' + os.environ['SCHEMA_REGISTRY_PORT']

SCHEMA=avro.load(os.path.join(os.path.dirname(__file__), '../resources/value_schema.avsc'))
INPUT_TOPIC='test-input'
OUTPUT_TOPIC='test-output'

value = {"name": "Value", "favorite_number": 10, "favorite_color": "green", "age": 25}

def main():


    print("Starting Avro Producer 2")
    p = AvroProducer({'bootstrap.servers': KAFKA_BROKERS, 'schema.registry.url': SCHEMA_REGITRY})
    p.produce(topic=INPUT_TOPIC, value=value, value_schema=SCHEMA)
    p.flush()

main()