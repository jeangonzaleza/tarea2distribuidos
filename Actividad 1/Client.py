import grpc
import threading
import socket

import mensajeria_pb2
import mensajeria_pb2_grpc

from datetime import datetime

#channel = grpc.insecure_channel('localhost:5000')
#
#stub = mensajeria_pb2_grpc.SendStub(channel)
#
#mesg = mensajeria_pb2.Mensaje(msg = "hola server", id = 1, id_dest = 2, timestamp = str(datetime.now()) )
#
#response = stub.Send(mesg)

class Client:
    mensajes = []
    def __init__(self):
        mensajes = []
        self.channel = grpc.insecure_channel('172.18.18.2:5000')
        self.stub = mensajeria_pb2_grpc.SendStub(self.channel)
        threading.Thread(target=self.waitMsg, daemon=True).start()

    def waitMsg(self):

        while True:
            stub = mensajeria_pb2_grpc.ReceiveStub(self.channel)
            mesg = mensajeria_pb2.Requester(id_requester = 1)
            response = stub.Receive(mesg)
            if response.id != 0 :
                print(response)

        #for msg in self.stub:
        #    mensaje = "[" + str(msg.timestamp) + "] " + str(msg.contenido)
        #    print(mensaje)
        #    self.mensajes.append(mensaje)

    def SendMessage(self):
        message = input("Ingrese Mensaje: ")
        if message is not '':
            mesg = mensajeria_pb2.Mensaje(msg = message, id = 1, id_dest = 2, timestamp = str(datetime.now()) )
            self.stub.Send(mesg)
    
def Main():
    client = Client()
    while(True):
        client.SendMessage()

if __name__=='__main__':
    Main()