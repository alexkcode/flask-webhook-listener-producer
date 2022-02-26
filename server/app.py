import json
import pika
from flask import Flask, request, abort, Response

app = Flask(__name__)

@app.route('/')
def index():
    return 'OK'

@app.route('/webhook/<queue>', methods=['POST'])
def webhook_endpoint(queue):
    """
    Endpoint for a webhook that immediately places message in MQ.
    """

    if request.method == 'POST':
        print('Webhook Received')

    request_json = request.get_json()
    request_json.update({'queue': queue})
    data = json.dumps(request_json)

    credentials = pika.PlainCredentials(request.authorization.username, request.authorization.password)
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))

    channel = connection.channel()
    channel.exchange_declare(exchange='webhook_exchange', durable=True)
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(queue, 'webhook_exchange', routing_key=queue+"_key")
    channel.basic_publish(
        exchange='webhook_exchange',
        routing_key=queue+"_key",
        body=data,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()

    return " [x] Data put in queue: %s" % data
    # return Response(response='OK', status=200)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')