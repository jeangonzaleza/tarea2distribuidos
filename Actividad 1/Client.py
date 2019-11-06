import grpc
import threading

import mensajeria_pb2
import mensajeria_pb2_grpc

from datetime import datetime

class Client:
    mensajes = []

    def __init__(self):
        mensajes = []
        self.channel = grpc.insecure_channel('172.18.18.2:5000')
        self.stub = mensajeria_pb2_grpc.SendStub(self.channel)
        self.idc = None
        threading.Thread(target=self.waitMsg, daemon=True).start()
    
    def HandShake(self):
        
        stub = mensajeria_pb2_grpc.HandShakeStub(self.channel)
        idReq = mensajeria_pb2.Empty()
        self.idc = stub.HandShake(idReq).id

    def waitMsg(self):
        
        while True:
            stub = mensajeria_pb2_grpc.ReceiveStub(self.channel)
            mesg = mensajeria_pb2.Requester(id_requester = self.idc)
            response = stub.Receive(mesg)
            if response.id != 0 :
                print(response)

    def SendMessage(self):
        destino = input("Ingrese destino: ")
        message = input("Ingrese Mensaje: ")
        if message is not '':
            mesg = mensajeria_pb2.Mensaje(msg = message, id = self.idc, id_dest = int(destino), timestamp = str(datetime.now()) )
            self.stub.Send(mesg)
    
def Main():
    client = Client()
    client.HandShake()
    print(client.idc)
    while(True):
        client.SendMessage()

if __name__=='__main__':
    Main()