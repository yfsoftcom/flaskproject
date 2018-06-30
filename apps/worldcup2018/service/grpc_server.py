"""The Python implementation of the GRPC worldcup.Greeter server."""

from concurrent import futures
import time

import grpc

import service_pb2
import service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class WorldCup(service_pb2_grpc.WorldCupServicer):

    def GetGroupTeams(self, request, context):
        # print('OK', request.text)
        return service_pb2.Data("aa")


def serve():
    print('ready to serve')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_WorldCupServicer_to_server(WorldCup(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('server started...')
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()