import grpc
import threading
from datetime import datetime

import chat_pb2
import chat_pb2_grpc

class Client:
    mensajes = []
    def __init__(self):
        mensajes = []
        channel = grpc.insecure_channel('localhost:9000')
        self.connect = chat_pb2_grpc.ServerChatStub(channel)
        threading.Thread(target=self.waitMsg, daemon=True).start()

    def waitMsg(self):
        for msg in self.connect.ChatStream(chat_pb2.Nada()):
            mensaje = "[" + str(msg.timestamp) + "] " + str(msg.contenido)
            print(mensaje)
            self.mensajes.append(mensaje)

    def SendMessage(self):
        message = input("Ingrese Mensaje: ")
        if message is not '':
            msg = chat_pb2.Mensaje()
            msg.timestamp = str(datetime.now())
            msg.contenido = message
            self.connect.SendMessage(msg)
    
def Main():
    client = Client()
    while(True):
        client.SendMessage()

if __name__=='__main__':
    Main()