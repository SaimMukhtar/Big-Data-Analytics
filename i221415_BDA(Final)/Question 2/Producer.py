# producer.py
from kafka import KafkaProducer, KafkaConsumer
import json
import random
import time

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Create Kafka consumer to read alerts
alert_consumer = KafkaConsumer('alerts', bootstrap_servers=bootstrap_servers, value_deserializer=lambda m: json.loads(m.decode('utf-8')))

# Generate synthetic transaction data
def generate_transaction():
    return {
        'transaction_id': random.randint(10000, 99999),
        'customer_id': random.randint(1000, 2000),
        'customer_age': random.randint(18, 70),
        'money': round(random.uniform(10.0, 5000.0), 2)
    }

# Producer script
def main():
    alerts = {}
    for message in alert_consumer:
        alert = message.value
        alerts[alert['customer_id']] = alert['message']

    while True:
        transaction = generate_transaction()
        customer_id = transaction['customer_id']
        
        # Check for fraud alerts
        if alerts.get(customer_id) == 'Fraud':
            print(f"Transaction ignored due to fraud alert: {transaction}")
        else:
            producer.send('transactions', value=transaction)
            print(f"Producer Sending the transaction: {transaction}")

        time.sleep(1)  # Simulate transactions every second

if __name__ == '__main__':
    main()