

# 📦 Project Description
## MongoDB-RabbitMQ-FastAPI Messaging System

This project demonstrates a simple distributed system using FastAPI, RabbitMQ, and MongoDB (MongoDB Atlas or local MongoDB) within a Docker Compose setup.

It implements a producer-consumer architecture:

- FastAPI (Producer) accepts HTTP POST requests, serializes the data, and pushes messages into a RabbitMQ queue.
- Python Consumer listens to the RabbitMQ queue, processes incoming messages, and saves them into a MongoDB database.

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
             [MongoDB Dashboard reads MongoDB data in MongoDB Atlas]
```

## 🚀 Components
| Component| Role |
| ------------- | ------------- |
| FastAPI Producer | Receives data via REST API and publishes it to RabbitMQ. |
| RabbitMQ  | Message broker that queues messages between producer and consumer. |
| MongoDB (Atlas or Local)  | Database where consumer stores processed messages. |
| RabbitMQ  | Listens to the queue, processes the data, and inserts it into MongoDB. |

## Why this project?
I work as a Data Engineer at Volvo Cars. We have an event-driven messaging service built using MongoDB and RabbitMQ. This system captures messages in specific queues, and it was designed before I joined the team. Later, my teammates and I developed a new data pipeline to capture and automatically process newly ingested vehicle sensor data—such as radar, LiDAR, and ultrasonic data.

However, we lacked proper observability of the data being ingested and processed through this pipeline. To address this, I proposed a proof of concept (PoC) to my team lead: connecting our MongoDB application hosted on OpenShift to MongoDB Atlas for enhanced observability and visualization.

This solution would help our team monitor the volume of data served per sensor and enable us to retrigger the data pipeline by collecting and filtering data based on specific criteria. My team lead has accepted the idea, and we are currently planning to deploy it.



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
Open - http://localhost:8000/docs and fill the information in the post request. (Discussed in the Quick Start section)



## 🐇 RabbitMQ

- RabbitMQ is used to buffer and deliver messages reliably between the producer and consumer.
- Durable queues and persistent messages ensure no data is lost if the server restarts.

## 🗄️ MongoDB
- Incoming messages from RabbitMQ are inserted into a MongoDB collection called messages inside the message_queue_db database.
- Default connection is set to MongoDB Atlas. (Update the URI if using local MongoDB.)

## Architecture diagram

### 📊 System Architecture
The application is built using a microservices approach. The flow is:
1. FastAPI Producer receives HTTP requests and publishes messages to RabbitMQ.
2. RabbitMQ acts as a broker to queue and deliver messages.
3. Consumer Worker listens to the queue, processes the messages, and stores them into MongoDB.
![System Architecture](docs/architecture/system_architecture.png)

### 📜 Sequence Diagram for /send Endpoint

When a client sends a API request to the /send endpoint:
![Sequence Diagram](docs/architecture/sequence_send.png)


## 🛠️ Environment Setup
1. Create a .env file at the root of the project by copying the provided .env.example (or manually create one).
2.	Update the following environment variables:
- RabbitMQ username and password.
- MongoDB username and password.
3.	MongoDB Atlas Setup (Optional):
- Create a free account on MongoDB Atlas.
👉 Get Started with MongoDB Atlas - https://www.w3schools.com/mongodb/mongodb_get_started.php
- Create a new user inside the Atlas project with appropriate roles.
- Update the following variables inside your .env file:
- MONGO_ATLAS_USERNAME
- MONGO_ATLAS_PASSWORD
- MONGO_ATLAS_CLUSTER
- The application will automatically prefer MongoDB Atlas if the credentials are available.
Otherwise, it will fallback to local MongoDB.
4.	Important:
- Make sure your .env is properly configured before starting the Docker containers or running the app locally.


## 🐳 Docker Compose

- rabbitmq
- mongodb
- fastapi_app (producer)
- consumer_worker (consumer)

All services communicate over a shared custom Docker network.


## 🏁 Quick Start
1.	Clone the repository
2.	Update MongoDB URI if needed
3.	Build and run Docker containers:

```bash
docker-compose up --build
```
4.	Test FastAPI API at http://localhost:8000/docs
5. After sending the API request or the data to be updated to the mongoDB, open the MongoDB Atlas with your login credentials. Click the database name and the collection name you mentioned in the .env file. Further, In the mongo DB atlas, visualiztion can be made.

##  Additional information
### Docker Compose Networks - Summary

This project uses a custom Docker network (app_network) to allow different services (RabbitMQ, MongoDB, FastAPI producer, and Consumer) to communicate securely and efficiently.

- Service discovery: Containers communicate using service names instead of IP addresses (e.g., rabbitmq:5672, mongodb:27017).
- Isolation: Only services on the same network can talk to each other, improving security.
- Scalability: The network setup makes it easy to add or replace services without breaking connections.

## 🧹 Future Improvements
- Add authentication/security for FastAPI.
- Set up retry mechanisms or dead-letter queues for failed messages.
- Health checks and monitoring dashboards (e.g., Grafana + Prometheus).
