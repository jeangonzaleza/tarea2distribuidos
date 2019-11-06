import pika
import threading
import time
import sys

class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='chat') #Create a queue named chat
        self.receive()
    
    def callback(self, ch, method, properties, body):
        print("[*] Received %r" % body)

    def receive(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.basic_consume(queue='chat', auto_ack=True, on_message_callback=self.callback) #Recibe mensajes de la cola
        self.channel.start_consuming()

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='chat') #Create a queue named chat
        while(True):
            self.send()

    def send(self):
        msg = input("[*] Ingrese mensaje: ")
        self.channel.basic_publish(exchange='', routing_key='chat', body=msg) #Envia msg a la cola

def Main():
    try:
        consumer = Consumer()
        producer = Producer()
        consumer.start()
        producer.start()
    except KeyboardInterrupt:
        print("Bye")

if __name__ == '__main__':
    Main()