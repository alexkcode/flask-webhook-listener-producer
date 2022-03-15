import json, ssl
import pika
from flask import Flask, request, redirect, Response, logging
from flask_talisman import Talisman
from flask_basicauth import BasicAuth

app = Flask(__name__)

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

@app.route('/')
def index():
    return 'OK'
    # return(ssl.OPENSSL_VERSION)

@app.route('/webhook/<queue>', methods=['POST'])
def webhook_endpoint(queue):
    """
    Endpoint for a webhook that immediately places message in MQ.
    """

    if request.method == 'POST':
        app.logger.info('Webhook Received')
        app.logger.info(request.get_data())

    # request_json = request.get_data()
    request_json = request.get_json(force=True)
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

    # return " [x] Data put in queue: %s" % data
    # app.logger.info(" [x] Data put in queue: %s" % data)
    return Response(response='OK', status=200)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')