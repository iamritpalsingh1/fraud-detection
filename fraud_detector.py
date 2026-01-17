import os
import sys

# 1. Windows Setup for Spark (To avoid "WinUtils" errors)
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, count, current_timestamp
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType
from pyspark.sql.functions import col

print("🔥 Initializing Spark Session... (This may take a moment)")

# 2. Create the Spark Engine
spark = SparkSession.builder \
    .appName("FraudDetector") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .config("spark.jars", "postgresql-42.7.1.jar") \
    .config("spark.driver.extraClassPath", "postgresql-42.7.1.jar") \
    .config("spark.sql.shuffle.partitions", "2") \
    .config("spark.driver.extraJavaOptions", "-Duser.timezone=UTC") \
    .config("spark.executor.extraJavaOptions", "-Duser.timezone=UTC") \
    .config("spark.sql.session.timeZone", "UTC") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 3. Define the structure of the incoming data
schema = StructType() \
    .add("transaction_id", StringType()) \
    .add("user_id", StringType()) \
    .add("card_id", StringType()) \
    .add("amount", DoubleType()) \
    .add("timestamp", DoubleType()) # Timestamp comes as a number (epoch) from Python

# 4. Connect to Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "financial_transactions") \
    .option("startingOffsets", "latest") \
    .load()

# 5. Transform Data
# Convert Binary -> String -> JSON Objects -> Timestamp format
txn_df = df.select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("timestamp", col("timestamp").cast(TimestampType()))

# 6. The Core Engineering Logic (Window Aggregation)
# "Group data into 10-minute sliding windows"
window_counts = txn_df \
    .withWatermark("timestamp", "1 minute") \
    .groupBy(
        window(col("timestamp"), "10 minutes", "10 minutes"),
        col("user_id")
    ) \
    .agg(count("transaction_id").alias("txn_count"))

# 7. Filter: Only show users with > 5 transactions in that window
fraud_alerts = window_counts.filter(col("txn_count") > 5)

# 8. Define the Postgres Writing Function
def write_to_postgres(df, epoch_id):
    # 1. Convert the complex 'window' struct to a simple String
    # Postgres cannot save "Structs", so we turn it into text: "[2026-01-15 10:00, ...]"
    clean_df = df.withColumn("window", col("window").cast("string"))

    # 2. Write to DB (using the Timezone fix we added earlier)
    clean_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/fraud_db") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "fraud_alerts") \
        .option("user", "postgres") \
        .option("password", "secure_password") \
        .mode("append") \
        .save()

print("🚀 Streaming started! Writing alerts to Postgres...")

# 9. Start Streaming (Use foreachBatch to write to DB)
query = fraud_alerts.writeStream \
    .outputMode("update") \
    .foreachBatch(write_to_postgres) \
    .start()

query.awaitTermination()