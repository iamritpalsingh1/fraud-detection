import time
import random
import json
from kafka import KafkaProducer
from faker import Faker

# Initialize the generator and producer
fake = Faker()
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("💳 Transaction Generator Started...")
print("Press Ctrl+C to stop.")

# ID of the user we will use for the fraud attack
FRAUD_USER_ID = 42 

try:
    while True:
        # 1. Randomly decide if we simulate a generic transaction or a fraud attack
        # 15% chance of fraud attack
        if random.random() < 0.15:
            print(f"\n⚠️  SIMULATING VELOCITY ATTACK (User {FRAUD_USER_ID})")
            
            # Generate 6 transactions in rapid succession (Velocity Attack)
            for _ in range(6):
                transaction = {
                    "transaction_id": fake.uuid4(),
                    "user_id": FRAUD_USER_ID, 
                    "card_id": f"card_{FRAUD_USER_ID}",
                    "amount": round(random.uniform(5.00, 1000.00), 2),
                    "timestamp": time.time(), # Current time
                    "merchant": fake.company(),
                    "location": fake.city()
                }
                producer.send('financial_transactions', transaction)
                print(f"   -> Sent Fraud Txn: ${transaction['amount']}")
                time.sleep(0.1) # Very fast (100ms gap)

        else:
            # 2. Normal "Good" Transaction
            user_id = random.randint(1, 100)
            transaction = {
                "transaction_id": fake.uuid4(),
                "user_id": user_id,
                "card_id": f"card_{user_id}",
                "amount": round(random.uniform(5.00, 100.00), 2),
                "timestamp": time.time(),
                "merchant": fake.company(),
                "location": fake.city()
            }
            producer.send('financial_transactions', transaction)
            print(f"✅ Sent Normal Txn: ${transaction['amount']}")

        # Wait a bit before the next loop to keep it readable
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\nStopping generator...")