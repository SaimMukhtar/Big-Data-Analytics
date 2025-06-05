# app.py
from flask import Flask, render_template, request
from kafka import KafkaProducer, KafkaConsumer
import json

app = Flask(__name__)

# Initialize Kafka producer and consumer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
consumer = KafkaConsumer('user_activity', bootstrap_servers=['localhost:9092'], group_id='recommendation_group')

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/playback', methods=['POST'])
def playback():
    # Capture user activity (e.g., track played)
    track_id = request.form['track_id']

    # Publish user activity to Kafka topic
    producer.send('user_activity', json.dumps({'track_id': track_id}).encode('utf-8'))

    return "Playback recorded successfully."

@app.route('/recommendation')
def recommendation():
    # Consume real-time recommendation from Kafka topic
    recommendation = []
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        recommendation.append(data['recommendation'])
        if len(recommendation) >= 5:
            break

    # Display recommendations to the user
    return render_template('recommendation.html', recommendation=recommendation)

if __name__ == '__main__':
    app.run(debug=True)
