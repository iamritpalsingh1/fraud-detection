# fraud-detection


🛡️ Real-Time Fraud Detection System
A scalable, event-driven data pipeline designed to detect "Velocity Attacks" (high-frequency transaction fraud) in real-time. This system processes financial transaction streams using Apache Kafka and Spark Structured Streaming, identifies fraudulent patterns using stateful aggregations, and visualizes alerts on a live Grafana dashboard.

🏗️ Architecture
The project follows the Kappa Architecture pattern for real-time stream processing:

Ingestion: Python-based Transaction Generator simulates 1000s of transactions/sec and pushes them to Kafka.

Processing: Apache Spark reads the stream, applies 10-minute windowed aggregations, and flags users exceeding transaction limits (e.g., >5 swipes in 10 mins).

Storage: Fraud alerts are written to PostgreSQL for persistent storage.

Visualization: Grafana queries the database to display real-time spikes in fraud activity.

🛠️ Technologies Used
Language: Python 3.x (PySpark)

Message Broker: Apache Kafka & Zookeeper

Stream Processing: Apache Spark Structured Streaming

Database: PostgreSQL

Visualization: Grafana

Infrastructure: Docker & Docker Compose

🚀 How It Works
1. The Scenario
In a normal scenario, a user swipes their card 1-2 times an hour. In a Velocity Attack, a thief swipes a stolen card rapidly (e.g., 10 times in 1 minute) before the card is blocked.

2. The Solution
The system defines a Time Window (e.g., 10 minutes).

It groups incoming data by user_id.

It maintains a running count of transactions in memory (Stateful Processing).

If count > 5 within the window, an alert is triggered immediately.

⚡ Getting Started
Prerequisites
Docker Desktop installed and running.

Python 3.x installed locally (for running generator scripts).

Installation
Clone the Repository

Bash

git clone https://github.com/yourusername/fraud-detection-project.git
cd fraud-detection-project
Start the Infrastructure Spin up Kafka, Zookeeper, Postgres, and Grafana using Docker Compose.

Bash

docker-compose up -d
Install Python Dependencies

Bash

pip install pyspark kafka-python psycopg2-binary
Usage
Step 1: Start the Fraud Detector (Spark Engine) This acts as the consumer, waiting for data patterns.

Bash

python fraud_detector.py
(Note: Ensure you have the PostgreSQL JDBC driver configured if running locally outside Docker)

Step 2: Start the Transaction Generator This script generates synthetic traffic, injecting random "Velocity Attacks" every ~20 seconds.

Bash

python transaction_generator.py
Step 3: Monitor Dashboard

Open Grafana at http://localhost:3000 (Default login: admin/admin).

Connect to the PostgreSQL data source.

Watch the live dashboard update as fraud attacks are simulated in the terminal.

📊 Visuals
Real-Time Dashboard (Grafana)
(Add your screenshot of the Grafana spike graph here)

Terminal Output
(Add your screenshot of the "SIMULATING VELOCITY ATTACK" yellow text here)

🔮 Future Improvements
Implement Machine Learning (Isolation Forest) for anomaly detection instead of rule-based logic.

Add email/Slack notifications when fraud is detected.

Deploy the pipeline to AWS using EMR (Spark) and MSK (Kafka).

📝 License
This project is licensed under the MIT License.
