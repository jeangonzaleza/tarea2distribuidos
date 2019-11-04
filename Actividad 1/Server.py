import grpc
from concurrent import futures
import time

import mensajeria_pb2
import mensajeria_pb2_grpc

class SendServicer(mensajeria_pb2_grpc.SendServicer):

    def __init__(self):
        self.messages = []
        self.log = "log.txt"

    def Send(self, request, context):
        print(request)
        self.messages.append(request)
        response = mensajeria_pb2.Empty()
        return response
    
    def Receive(self, request, context):
        if (len(self.messages)>0):
            for mensaje in self.messages:
                if (mensaje.id_dest == request.id_requester):
                    mensaje_recibido = mensaje
                    response = mensajeria_pb2.Mensaje(msg=mensaje_recibido.msg, id = mensaje_recibido.id, id_dest = mensaje_recibido.id_dest, timestamp = mensaje_recibido.timestamp)
                    self.messages.remove(mensaje)
                else:
                    response = mensajeria_pb2.Mensaje(msg="", id = 0, id_dest = 2, timestamp = "")
        else:
            response = mensajeria_pb2.Mensaje(msg="", id = 0, id_dest = 2, timestamp = "")
        #mensaje_recibido = self.messages[-1]
        
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

send_servicer = SendServicer()

mensajeria_pb2_grpc.add_SendServicer_to_server(send_servicer,server)
mensajeria_pb2_grpc.add_ReceiveServicer_to_server(send_servicer,server)

print("server listening in 5000")

server.add_insecure_port('[::]:5000')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop()