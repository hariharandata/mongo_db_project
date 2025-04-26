```markdown
[Client/API] 
    ↓ 
  POST JSON → [Producer Service]
                  ↓
          Publishes to RabbitMQ
                  ↓
         [Consumer Service reads from RabbitMQ]
                  ↓
         Inserts into MongoDB → [MongoDB]
                  ↓
             [Grafana Dashboard reads MongoDB]
```

# 📦 Project Description
## MongoDB-RabbitMQ-FastAPI Messaging System

This project demonstrates a simple distributed system using FastAPI, RabbitMQ, and MongoDB (MongoDB Atlas or local MongoDB) within a Docker Compose setup.

It implements a producer-consumer architecture:

-	FastAPI (Producer) accepts HTTP POST requests, serializes the data, and pushes messages into a RabbitMQ queue.
- Python Consumer listens to the RabbitMQ queue, processes incoming messages, and saves them into a MongoDB database.



## 🚀 Components
| Component| Role |
| ------------- | ------------- |
| FastAPI Producer | Receives data via REST API and publishes it to RabbitMQ. |
| RabbitMQ  | Message broker that queues messages between producer and consumer. |
| MongoDB (Atlas or Local)  | Database where consumer stores processed messages. |
| RabbitMQ  | Listens to the queue, processes the data, and inserts it into MongoDB. |



## ⚙️ Features

- FastAPI based REST API at /send to post data into RabbitMQ.

- Reliable Message Delivery using durable queues and persistent messages in RabbitMQ.

- MongoDB Atlas Integration or optional local MongoDB.

- Structured Logging using a custom logger utility.

- Fair Dispatch with RabbitMQ basic_qos.

- Dockerized deployment using Docker Compose for full-stack orchestration.

## 📂 Project Structure

```markdown
mongo_db_project/
│
├── docker-compose.yml
├── Dockerfile.fastapi
├── Dockerfile.consumer
├── pyproject.toml
├── utils/
│   ├── logger.py
│   ├── model.py
│   └── rabbitmq.py
├── src/
│   ├── producer/
│   │   └── producer.py
│   └── consumer/
│       └── consumer.py
└── README.md
```

## 📡 FastAPI Producer API
- GET / → Health check endpoint

- POST /send → Accepts JSON data and pushes it to RabbitMQ

Example POST request:
Open - http://localhost:8000/docs and fill the information in the post request.



## 🐇 RabbitMQ

- RabbitMQ is used to buffer and deliver messages reliably between the producer and consumer.
- Durable queues and persistent messages ensure no data is lost if the server restarts.

## 🗄️ MongoDB
- Incoming messages from RabbitMQ are inserted into a MongoDB collection called messages inside the message_queue_db database.
- Default connection is set to MongoDB Atlas. (Update the URI if using local MongoDB.)

## 🐳 Docker Compose

- rabbitmq
- mongodb
- fastapi_app (producer)
- consumer_worker (consumer)

All services communicate over a shared custom Docker network.

## 🧹 Future Improvements
- Add authentication/security for FastAPI.
- Set up retry mechanisms or dead-letter queues for failed messages.
- Health checks and monitoring dashboards (e.g., Grafana + Prometheus).

## 🏁 Quick Start
1.	Clone the repository
2.	Update MongoDB URI if needed
3.	Build and run Docker containers:

```bash
docker-compose up --build
```
4.	Test FastAPI API at http://localhost:8000

##  Additional information
### Docker Compose Networks - Summary

This project uses a custom Docker network (app_network) to allow different services (RabbitMQ, MongoDB, FastAPI producer, and Consumer) to communicate securely and efficiently.

• Service discovery: Containers communicate using service names instead of IP addresses (e.g., rabbitmq:5672, mongodb:27017).
• Isolation: Only services on the same network can talk to each other, improving security.
• Scalability: The network setup makes it easy to add or replace services without breaking connections.




Connect to mongo DB

mongosh "mongodb+srv://cluster0.ucye7p6.mongodb.net/" --apiVersion 1 --username tharanihari2698
password - Hari1998