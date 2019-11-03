import grpc
import mensajeria_pb2
import mensajeria_pb2_grpc

from datetime import datetime

channel = grpc.insecure_channel('localhost:5000')

stub = mensajeria_pb2_grpc.SendStub(channel)

mesg = mensajeria_pb2.Mensaje(msg = "hola server", id = 1, id_dest = 1, timestamp = str(datetime.now()) )

response = stub.Send(mesg)
