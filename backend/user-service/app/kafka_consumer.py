from threading import Thread
from kafka import KafkaConsumer
import json

def start_kafka_consumer():
    def run():
        consumer = KafkaConsumer(
            'user-events',
            bootstrap_servers='kafka:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='user-service-group'
        )
        for message in consumer:
            print(f"Received message from Kafka: {message.value}")

    thread = Thread(target=run)
    thread.daemon = True
    thread.start()