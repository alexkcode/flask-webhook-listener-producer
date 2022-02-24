import json
import pika
from flask import Flask, request, abort, Response

app = Flask(__name__)

@app.route('/')
def index():
    return 'OK'

@app.route('/webhook', methods=['POST'])
def webhook_endpoint():
    """
    Endpoint for a webhook that immediately places message in MQ.
    """

    if request.method == 'POST':
        print('Webhook Received')

    # data = request.get_json()
    request_json = request.json
    data = json.dumps(request_json,indent=4)

    creds = pika.PlainCredentials(request.authorization.username, request.authorization.password)
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', creds))

    channel = connection.channel()
    channel.exchange_declare(exchange='webhook_exchange', durable=True)
    channel.queue_declare(queue='webhook_queue', durable=True)
    channel.queue_bind('webhook_queue', 'webhook_exchange', routing_key='webhook')
    channel.basic_publish(
        exchange='webhook_exchange',
        routing_key='webhook',
        body=data,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()

    # print(" [x] Data put in queue: %s" % data)
    # return " [x] Data put in queue: %s" % data
    return Response(status=200)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')