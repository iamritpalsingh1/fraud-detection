# Fraud-detection


# 🛡️ Real-Time Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Apache Spark](https://img.shields.io/badge/Apache%20Spark-Streaming-orange) ![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-Event%20Streaming-black) ![Docker](https://img.shields.io/badge/Docker-Containerized-blue) ![Grafana](https://img.shields.io/badge/Grafana-Visualization-orange)

A scalable, event-driven data pipeline designed to detect **"Velocity Attacks"** (high-frequency transaction fraud) in real-time. This system processes financial transaction streams using **Apache Kafka** and **Spark Structured Streaming**, identifies fraudulent patterns using stateful aggregations, and visualizes alerts on a live **Grafana** dashboard.

## 🏗️ Architecture

The project follows the **Kappa Architecture** pattern for real-time stream processing:

1.  **Ingestion:** Python-based Transaction Generator simulates 1000s of transactions/sec and pushes them to **Kafka**.
2.  **Processing:** **Apache Spark** reads the stream, applies 10-minute windowed aggregations, and flags users exceeding transaction limits (e.g., >5 swipes in 10 mins).
3.  **Storage:** Fraud alerts are written to **PostgreSQL** for persistent storage.
4.  **Visualization:** **Grafana** queries the database to display real-time spikes in fraud activity.



---

## 🛠️ Technologies Used

* **Language:** Python 3.x (PySpark)
* **Message Broker:** Apache Kafka & Zookeeper
* **Stream Processing:** Apache Spark Structured Streaming
* **Database:** PostgreSQL
* **Visualization:** Grafana
* **Infrastructure:** Docker & Docker Compose

---

## 🚀 How It Works

### 1. The Scenario
In a normal scenario, a user swipes their card 1-2 times an hour. In a **Velocity Attack**, a thief swipes a stolen card rapidly (e.g., 10 times in 1 minute) before the card is blocked.

### 2. The Solution
* The system defines a **Time Window** (e.g., 10 minutes).
* It groups incoming data by `user_id`.
* It maintains a running count of transactions in memory (**Stateful Processing**).
* If `count > 5` within the window, an alert is triggered immediately.

---

## ⚡ Getting Started

### Prerequisites
* Docker Desktop installed and running.
* Python 3.x installed locally (for running generator scripts).

### Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/fraud-detection-project.git](https://github.com/yourusername/fraud-detection-project.git)
    cd fraud-detection-project
    ```

2.  **Start the Infrastructure**
    Spin up Kafka, Zookeeper, Postgres, and Grafana using Docker Compose.
    ```bash
    docker-compose up -d
    ```

3.  **Install Python Dependencies**
    ```bash
    pip install pyspark kafka-python psycopg2-binary
    ```

### Usage

**Step 1: Start the Fraud Detector (Spark Engine)**
This acts as the consumer, waiting for data patterns.
```bash
python fraud_detector.py
```

**Step 2: Start the Transaction Generator This script generates synthetic traffic, injecting random "Velocity Attacks" every ~20 seconds.**
```bash
python transaction_generator.py
```

**Step 3: Monitor Dashboard**
* Open Grafana at `http://localhost:3000` (Default login: `admin`/`admin`).
* Connect to the PostgreSQL data source.
* Watch the live dashboard update as fraud attacks are simulated in the terminal.

---

## 📊 Visuals

### Real-Time Dashboard (Grafana)
![Grafana Dashboard](https://github.com/yourusername/fraud-detection-project/blob/main/images/grafana_dashboard.png?raw=true)

### Terminal Output
![Terminal Output](https://github.com/yourusername/fraud-detection-project/blob/main/images/terminal_output.png?raw=true)

---

## 🔮 Future Improvements

* **Machine Learning Integration:** Replace rule-based logic with an Isolation Forest model to detect unknown fraud patterns.
* **Notification System:** Integrate AWS SNS or Slack Webhooks to send instant alerts to security teams.
* **Cloud Deployment:** Migrate the local Docker infrastructure to AWS using EMR (Spark) and MSK (Managed Kafka).
* **CI/CD Pipeline:** Implement GitHub Actions for automated testing and deployment.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### 👤 Author

**Amrit** * [LinkedIn](https://www.linkedin.com/in/yourprofile)  
* [GitHub](https://github.com/yourusername)


