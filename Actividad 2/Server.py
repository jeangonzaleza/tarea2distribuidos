import pika
import threading
import time
import sys

id_actual = 1

class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.producer = Producer()
        self.producer.start()

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) #Connect to rabbitmq
        self.channel = self.connection.channel() #Create the channel
        self.channel.queue_declare(queue='GlobalQueue') #Create a queue named GlobalQueue
        self.channel.queue_declare(queue='HandShakeQueue') #Create a queue named HandShakeQueue
        self.receive()
    
    def callback(self, ch, method, properties, body):
        global id_actual
        msg = body.decode('utf-8')
        header = properties.headers
        print("[*] Received %r" % msg)
        if (header['to'] == 0 and header['from'] == None):
            self.channel.basic_publish(exchange='', routing_key='HandShakeQueue', body=str(id_actual))
            self.channel.queue_declare(queue=str(id_actual))
            id_actual += 1
            print ("siguiente id: ",id_actual)
        elif (header['to'] != 0 and header['from'] != None):
            self.producer.send(msg, header)

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
        self.channel.queue_declare(queue='GlobalQueue')

    def send(self, msg, header):
        self.channel.queue_declare(queue=str(header['to']))
        self.channel.basic_publish(exchange='', routing_key=str(header['to']), 
                                    properties=pika.BasicProperties(headers=header), 
                                    body=msg) #Envia msg a la cola

def Main():
    try:
        consumer = Consumer()
        #producer = Producer()
        consumer.start()
        #producer.start()
    except KeyboardInterrupt:
        print("Bye")

if __name__ == '__main__':
    Main()