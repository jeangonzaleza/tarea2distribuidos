import grpc
from concurrent import futures
import time

import mensajeria_pb2
import mensajeria_pb2_grpc

ids = 1

class SendServicer(mensajeria_pb2_grpc.SendServicer):

    def __init__(self):
        self.messages = {}
        self.log = "log.txt"
        self.users = []

    def HandShake(self, request, context):
        global ids
        response = mensajeria_pb2.IdRequest()
        response.id = ids
        self.messages[ids] = list()
        ids += 1
        return response

    def Send(self, request, context):
        print(request)
        file = open(self.log,"a")
        file.write("id:%d;id_dest:%d;msg:%s;timestamp:%s \n" % (request.id, request.id_dest, request.msg, request.timestamp))
        file.close()
        self.messages[request.id_dest].append(request)
        response = mensajeria_pb2.Empty()
        return response
    
    def Receive(self, request, context):
        if str(request.id_requester) not in self.users:
            self.users.append(str(request.id_requester))
        if (len(self.messages[request.id_requester])>0):
            for mensaje in self.messages[request.id_requester]:
                if (mensaje.id_dest == request.id_requester):
                    mensaje_recibido = mensaje
                    response = mensajeria_pb2.Mensaje(msg=mensaje_recibido.msg, id = mensaje_recibido.id, id_dest = mensaje_recibido.id_dest, timestamp = mensaje_recibido.timestamp)
                    self.messages[request.id_requester].remove(mensaje)
                    break
                else:
                    response = mensajeria_pb2.Mensaje(msg="", id = 0, id_dest = request.id_requester, timestamp = "")
        else:
            response = mensajeria_pb2.Mensaje(msg="", id = 0, id_dest = request.id_requester, timestamp = "")
        #mensaje_recibido = self.messages[-1]
        
        return response

    def Menu(self, request, context):
        if request.msg == "1":
            response = mensajeria_pb2.Listado(lista= " ".join(self.users))
            
        elif request.msg == "2":
            mensajes = ""
            file = open(self.log, "r")
            for line in file:
                if "id:"+str(request.id)+";" in line:
                    mensajes = mensajes + line
            response = mensajeria_pb2.Listado(lista = mensajes)
            file.close()
              
        else:
            response = mensajeria_pb2.Listado(lista = "Proceda a enviar mensajes\n")
            
        return response
    
    
def Main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    send_servicer = SendServicer()

    mensajeria_pb2_grpc.add_MenuServicer_to_server(send_servicer,server)
    mensajeria_pb2_grpc.add_SendServicer_to_server(send_servicer,server)
    mensajeria_pb2_grpc.add_ReceiveServicer_to_server(send_servicer,server)
    mensajeria_pb2_grpc.add_HandShakeServicer_to_server(send_servicer,server)

    print("server listening in 5000")

    server.add_insecure_port('[::]:5000')
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("cerrando server")
        server.stop(0)

if __name__ == '__main__':
    Main()