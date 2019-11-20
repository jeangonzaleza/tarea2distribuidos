import pika
import threading
import time
import sys

id_client = None

class HandShake(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.connected = 0
        while(self.connected == 0):
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit_server'))
                self.connected = 1
            except pika.exceptions.AMQPConnectionError:
                self.connected = 0
                print("Ups, el servidor de rabbitMQ no responde, reintentando en:")
                for i in range(5):
                    print("..", (5-i))
                    time.sleep(1)
                print("...")

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
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit_server'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=str(id_client))
        self.receive()
    
    def callback(self, ch, method, properties, body):
        print("[*] Received %r" % body)

    def receive(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.basic_consume(queue=str(id_client), auto_ack=True, on_message_callback=self.callback) #Recibe mensajes de la cola
        self.channel.start_consuming()

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit_server'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='GlobalQueue') #Create a queue named GlobalQueue
        self.handshake()
        while(True):
            self.send()

    def send(self):
        opcion = input("Seleccione una de las siguiente opciones: \n \t 1-Lista usuarios \n \t 2-Lista mensajes enviados \n \t 3-Enviar mensaje \n")
        if opcion == "1":
            self.channel.basic_publish(exchange='', routing_key='GlobalQueue', 
                                    properties=pika.BasicProperties(headers={'to': 0, 'from': id_client}), 
                                    body="lista usuarios")
        elif opcion == "2":
            self.channel.basic_publish(exchange='', routing_key='GlobalQueue', 
                                    properties=pika.BasicProperties(headers={'to': 0, 'from': id_client}), 
                                    body="lista mensajes")
        elif opcion == "3":
            destino = input("[*] Ingrese destino:")
            msg = input("[*] Ingrese mensaje: ")
            self.channel.basic_publish(exchange='', routing_key='GlobalQueue', 
                                        properties=pika.BasicProperties(headers={'to': destino, 'from': id_client}), 
                                        body=msg) #Envia msg a la cola

    def handshake(self):
        self.channel.basic_publish(exchange='', routing_key='GlobalQueue', 
                                    properties=pika.BasicProperties(headers={'to': 0, 'from': id_client}), 
                                    body="peticion de id")

def Main():
    try:
        global id_client
        consumer = Consumer()
        producer = Producer()
        handshake = HandShake()

        producer.start()
        handshake.start()
        while(id_client == None):
            continue
        print("Su id es: ", id_client)
        handshake.join()
        print("handshake killed")

        consumer.start()


    except KeyboardInterrupt:
        print("Bye")

if __name__ == '__main__':
    Main()