from kafka import KafkaProducer, KafkaConsumer
import json
import time
import os
import sys
import traceback
import logging

# Configurer le logging pour capturer les erreurs même dans un thread daemon
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_kafka_producer():
    bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
    max_retries = 10
    retry_interval = 5

    for attempt in range(max_retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                retries=5,
                request_timeout_ms=10000,
                max_block_ms=10000
            )
            logger.info("Kafka producer initialized successfully")
            return producer
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{max_retries}: Failed to connect to Kafka (Producer) - {e}")
            traceback.print_exc(file=sys.stdout)
            time.sleep(retry_interval)
    raise Exception("Failed to connect to Kafka (Producer) after maximum retries")

def start_kafka_consumer():
    bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
    max_retries = 10
    retry_interval = 5

    logger.info(f"Attempting to connect to Kafka at {bootstrap_servers}...")
    consumer = None
    for attempt in range(max_retries):
        try:
            consumer = KafkaConsumer(
                'reservations_topic',
                bootstrap_servers=bootstrap_servers,
                auto_offset_reset='earliest',
                group_id='reservation-service-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                enable_auto_commit=True,
                session_timeout_ms=30000,
                max_poll_interval_ms=300000,
                request_timeout_ms=40000
            )
            logger.info("Kafka consumer started, listening to 'reservations_topic'...")
            break
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{max_retries}: Failed to connect to Kafka (Consumer) - {e}")
            traceback.print_exc(file=sys.stdout)
            logger.info(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    else:
        logger.error("Failed to connect to Kafka (Consumer) after maximum retries. Kafka consumer will not start.")
        return

    if consumer is None:
        logger.error("Consumer is None, cannot proceed with message consumption.")
        return

    try:
        logger.info("Starting to consume messages...")
        for message in consumer:
            event = message.value
            logger.info(f"Received event: {event}")
    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")
        traceback.print_exc(file=sys.stdout)
    finally:
        logger.info("Kafka consumer stopped.")