from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time
import config

# topic name: test-bus-data

client = KafkaClient(hosts="localhost:9092")
topic = client.topics[config.TOPIC_NAME]
producer = topic.get_sync_producer()

# Read coordinates from JSON file
input_json_file = open('./data/bus_1.json')
json_array = json.load(input_json_file)
coordinates = json_array['features'][0]['geometry']['coordinates']

# Generate UUID
def generate_uuid():
    return uuid.uuid4()

data = {}
data['bus_line'] = '00001'

# Construct a message & send it to Kafka
def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['bus_line'] +  '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        message_as_bytes = str.encode(message)
        producer.produce(message_as_bytes)
        time.sleep(1)

        if i == len(coordinates) - 1:
            i = 0
        else:
            i += 1

generate_checkpoint(coordinates)

