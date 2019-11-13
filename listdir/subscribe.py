# consumer
import pika
import configparser
import os


def connect(hostname, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
    channel = connection.channel()
    # channel.queue_declare(queue=queue_name)
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    return channel


def callback(ch, method, properties, body):
    print("[x] Received %r" % body)


def consume(channel, queue_name):
    result = channel.queue_declare(queue='', exclusive=True)
    res_queue = result.method.queue

    channel.queue_bind(exchange='logs', queue=res_queue)
    print('[*] Waiting for logs. To exit, press CTRL+C')

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print('[*] Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    o = os.path.dirname(__file__)
    config.read(o+'config.ini')
    hname = config['db']['hostname']
    qname = config['db']['queue_name']
    consume(connect(hname, qname), qname)
