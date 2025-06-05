# consumer.py
from kafka import KafkaConsumer, KafkaProducer
import json

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Create Kafka consumer to read transactions
consumer = KafkaConsumer('transactions', bootstrap_servers=bootstrap_servers, value_deserializer=lambda m: json.loads(m.decode('utf-8')))

# Create Kafka producer to send alerts
producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Consumer script
def main():
    for message in consumer:
        transaction = message.value
        customer_id = transaction['customer_id']
        customer_age = transaction['customer_age']
        money = transaction['money']
        
        print(f"Consumer Receiving transaction: {transaction}")

        # Check if transaction meets the fraud criteria
        if money > 4000 and customer_age > 40:
            # Flag as potential fraud and send to 'alerts' topic
            fraud_alert = {'customer_id': customer_id, 'message': 'Fraud'}
            producer.send('alerts', value=fraud_alert)
            print(f"Fraud alert sent: {fraud_alert}")

if __name__ == '__main__':
    main()