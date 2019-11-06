import pika
import threading
import _thread

def callback(ch, method, properties, body):
    print("[*] Received %r" % body)

def sendMsg(channel):
    while(True):
        msg = input("[*] Ingrese mensaje: ")
        channel.basic_publish(exchange='', routing_key='chat', body=msg) #Envia msg a la cola

def receiveMsg(channel):
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(queue='chat', auto_ack=True, on_message_callback=callback) #Recibe mensajes de la cola
    channel.start_consuming()

def Main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit_server'))
        channel = connection.channel()
        channel.queue_declare(queue='chat') #Create a queue named chat
        _thread.start_new_thread(sendMsg, (channel,))
        _thread.start_new_thread(receiveMsg, (channel,))
        while(True):
            continue
    except KeyboardInterrupt:
        print("OK BYE")
        connection.close()

if __name__ == '__main__':
    Main()
    