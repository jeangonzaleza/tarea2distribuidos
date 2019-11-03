import grpc
import mensajeria_pb2
import mensajeria_pb2_grpc

from datetime import datetime

channel = grpc.insecure_channel('localhost:5000')

stub = mensajeria_pb2_grpc.ReceiveStub(channel)

mesg = mensajeria_pb2.Empty()

response = stub.Receive(mesg)

print(response)