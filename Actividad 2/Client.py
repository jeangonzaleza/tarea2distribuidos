import pika
import threading
import time
import sys

id_client = None

class HandShake(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='HandShakeQueue')
        self.handshake()
        return

    def callback(self, ch, method, properties, body):
        global id_client
        id_client = int(body)
        print("[*] Received id %r" % id_client)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        self.channel.stop_consuming()
        self.connection.close()

    def handshake(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='HandShakeQueue', on_message_callback=self.callback)
        self.channel.start_consuming()

class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='GlobalQueue') #Create a queue named GlobalQueue
        self.receive()
    
    def callback(self, ch, method, properties, body):
        print("[*] Received %r" % body)

    def receive(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.basic_consume(queue='GlobalQueue', auto_ack=True, on_message_callback=self.callback) #Recibe mensajes de la cola
        self.channel.start_consuming()

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='GlobalQueue') #Create a queue named GlobalQueue
        self.handshake()
        print("Su id es: ",id_client)
        while(True):
            self.send()

    def send(self):
        msg = input("[*] Ingrese mensaje: ")
        self.channel.basic_publish(exchange='', routing_key='GlobalQueue', body=msg) #Envia msg a la cola

    def handshake(self):
        self.channel.basic_publish(exchange='', routing_key='GlobalQueue', body="peticion")

def Main():
    try:
        global id_client
        #consumer = Consumer()
        producer = Producer()
        handshake = HandShake()
        #consumer.start()
        producer.start()
        handshake.start()
        while(id_client == None):
            continue
        print("Su id es: ", id_client)
        handshake.join()
        print("handshake killed")


    except KeyboardInterrupt:
        print("Bye")

if __name__ == '__main__':
    Main()