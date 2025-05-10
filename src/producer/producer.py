import json

import pika
from fastapi import FastAPI, HTTPException

from utils.logger import setup_logger
from utils.model import DataModel
from utils.rabbitmq import wait_for_rabbitmq

logger = setup_logger(__name__)

# ──────────────
# FastAPI App
# ──────────────
app = FastAPI()


# Connect to RabbitMQ
connection = wait_for_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue="data_queue", durable=True)


@app.get("/")
def read_root():
    logger.info("Health check called at /")
    return {"message": "FastAPI producer is running."}


@app.post("/send")
async def send_data(data: DataModel):
    try:
        message = json.dumps(data.model_dump())
        channel.basic_publish(
            exchange="",
            routing_key="data_queue",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent,
            ),
        )
        logger.info(f"[x] Sent message: {message}")
        return {"message": "Data sent successfully"}
    except Exception as e:
        logger.error(f"Failed to send data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send data: {str(e)}")
