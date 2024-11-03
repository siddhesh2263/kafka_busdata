from flask import Flask, render_template, Response
from pykafka import KafkaClient

app = Flask(__name__)

def get_kafka_client():
    return KafkaClient(hosts="localhost:9092")

def consume_events(client, topic_name):
    for i in client.topics[topic_name].get_simple_consumer():
        yield 'data:{0}\n\n'.format(i.value.decode())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topic/<topic_name>')
def get_messages(topic_name):
    client = get_kafka_client()
    return Response(consume_events(client, topic_name), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True, port=5002)

