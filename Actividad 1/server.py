import grpc
from concurrent import futures
import time

import mensajeria_pb2
import mensajeria_pb2_grpc

class SendServicer(mensajeria_pb2_grpc.SendServicer):

    def __init__(self):
        self.messages = []

    def Send(self, request, context):
        print(request)
        self.messages.append(request)
        response = mensajeria_pb2.Empty()
        return response
    
    def Receive(self, request, context):
        mensaje_recibido = self.messages[-1]
        response = mensajeria_pb2.Mensaje(msg=mensaje_recibido.msg, id = mensaje_recibido.id, id_dest = mensaje_recibido.id_dest, timestamp = mensaje_recibido.timestamp)
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