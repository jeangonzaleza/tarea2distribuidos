import pika
import threading
import time
import sys

id_actual = 1
users = []
log = "log.txt"

class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.producer = Producer()
        self.producer.start()

    def run(self):
        self.connected = 0
        while(self.connected == 0):
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit_server')) #Connect to rabbitmq
                self.connected = 1
            except pika.exceptions.AMQPConnectionError:
                self.connected = 0
                print("Ups, el servidor de rabbitMQ no responde, reintentando en:")
                for i in range(5):
                    print("..", (5-i))
                    time.sleep(1)
                print("...")
        
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
            #users.append(str(id_actual))
            id_actual += 1
            print ("siguiente id: ",id_actual)
        elif (header['to'] != 0 and header['from'] != None):
            file = open(log, "a")
            file.write(msg+"\n")
            self.producer.send(msg, header)
        ##    
        ## PROCESAMIENTO MENSAJES DEL MENU
        elif (header['to'] == 0 and header['from'] != None):
            if msg == "lista mensajes":
                msg = ""
                file = open(log, "r")
                for line in file:
                    if "from:"+str(header['from'])+";" in line:
                        msg = msg + line
                header['to'] = header['from']
                header['from'] = 0
                self.producer.send(msg, header)
                file.close()

            if msg == "lista usuarios":
                msg = ""
                users = []
                for i in range(id_actual):
                    users.append(i+1)
                for usuario in users:
                    heart = {}
                    heart['to'] = usuario
                    heart['from'] = 0
                    beat = 'beat'
                    self.producer.send(beat, heart)
                time.sleep(1)
                for usuario in users:
                    check = self.channel.queue_declare(queue=str(usuario), passive=True)
                    if check.method.message_count != 0:
                        users.remove(usuario)
                for usuario in users:
                    msg = msg + str(usuario)+ "\n"
                header['to'] = header['from']
                header['from'] = 0
                self.producer.send(msg, header)

    def receive(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.basic_consume(queue='GlobalQueue', auto_ack=True, on_message_callback=self.callback) #Recibe mensajes de la cola
        self.channel.start_consuming()

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit_server'))
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