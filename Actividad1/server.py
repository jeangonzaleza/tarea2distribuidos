import grpc
from concurrent import futures
import time

import chat_pb2
import chat_pb2_grpc


class ServerChat(chat_pb2_grpc.ServerChatServicer):
    mensajes = []
    def __init__(self):
        mensajes = [] #registro de mensajes

    def ChatStream(self, request_iterator, context):
        ultimoMsj = 0 #Posicion en la lista del ultimo mensaje
        while (True):
            while (len(self.mensajes) > ultimoMsj):
                msj = self.mensajes[ultimoMsj]
                ultimoMsj += 1
                yield msj #parecido al return, pero recuerda donde queda la funcion antes de retornar

    def SendMessage(self, request, context): #tambien me gustaria saber que estoy haciendo
        print("[" + request.timestamp + "] " + request.contenido)
        self.mensajes.append(request)
        return chat_pb2.Nada()

def Main():
    port = 9000
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000))
    chat_pb2_grpc.add_ServerChatServicer_to_server(ServerChat(), server)
    
    print("Servidor escuchando en el puerto: " + str(port))
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    
    while(True): #don't ask
        continue

if __name__ == '__main__':
    Main()