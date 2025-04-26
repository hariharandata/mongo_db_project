from .logger import setup_logger
import pika
import time


logger = setup_logger(__name__)

def wait_for_rabbitmq(max_retries=10):
    for i in range(max_retries):
        try:
            logger.info(f"Trying to connect to RabbitMQ... Attempt {i+1}")
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            logger.info("Connected to RabbitMQ successfully")
            return connection
        except pika.exceptions.AMQPConnectionError:
            logger.warning(f"[{i+1}/{max_retries}] Waiting for RabbitMQ...")
            time.sleep(3)
    logger.error("Failed to connect to RabbitMQ after several retries")
    raise Exception("Failed to connect to RabbitMQ")
