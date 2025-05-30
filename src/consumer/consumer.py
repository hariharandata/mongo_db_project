import json
import os
import sys
import time

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from utils.logger import setup_logger
from utils.rabbitmq import wait_for_rabbitmq

logger = setup_logger(__name__)


# Atlas connection string
atlas_cluster = os.getenv("MONGO_ATLAS_URI")
mongodb_name = os.getenv("MONGO_DB_NAME", "message_queue_db")
collection_name = os.getenv("MONGO_COLLECTION_NAME", "messages")

# Assunimg that MongoDB is running on the same Docker network as RabbitMQ
local_mongo_url = os.getenv("MONGO_URL", "mongodb://admin:adminpassword@mongodb:27017/")

# Check if Atlas details are available
if atlas_cluster:
    client = MongoClient(atlas_cluster, server_api=ServerApi("1"))
    logger.info("Connecting successful to MongoDB Atlas...")
else:
    uri = local_mongo_url
    logger.info("Connecting to Local MongoDB...")
    client = MongoClient(uri)
# Confirm connection
try:
    client.admin.command("ping")
    logger.info("✅ Connected to MongoDB Atlas")
except Exception as e:
    logger.error(f"❌ Connection failed: {e}")

# Use your desired DB and collection
db = client["message_queue_db"]
collection = db["messages"]


def callback(ch, method, properties, body):
    try:
        logger.info(f"Received {body}")
        message = json.loads(body.decode())
        time.sleep(5)  # Simulate some processing time
        collection.insert_one(message)
        logger.info(f"[✔] Message saved to MongoDB: {message}")
        # Acknowledge the message even though receiver crash it wil retain the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Failed to insert a message to MongoDB: {e}")
        # Below line tells RabbitMQ not to retry it — discard it.”
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main():
    connection = wait_for_rabbitmq()
    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue="data_queue", durable=True)
    logger.info(" [*] Waiting for messages. To exit press CTRL+C")
    # It tells RabbitMQ:“Don’t send more than one message at a time
    # to a worker/consumer until it acknowledges the previous one.”
    channel.basic_qos(prefetch_count=1)  # Fair dispatch
    channel.basic_consume(queue="data_queue", on_message_callback=callback)  # Fair dispatch
    channel.start_consuming()


if __name__ == "__main__":
    try:
        logger.info("Starting RabbitMQ consumer...")
        main()
    except KeyboardInterrupt:
        logger.error("Interrupted by user %s", os.getlogin())
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
