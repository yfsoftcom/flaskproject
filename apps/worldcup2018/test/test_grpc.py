# -*- coding: utf-8 -*-
import unittest
import service.service_pb2_grpc as service_pb2_grpc
import service.service_pb2 as service_pb2
import grpc

class TestGrpc(unittest.TestCase):

  def test_get_teams(self):

    with grpc.insecure_channel('localhost:50051') as channel:
      stub = service_pb2_grpc.WorldCupStub(channel)
      response = stub.GetGroupTeams(service_pb2.Data(text='you'))
      print("client received: " + response.text)
      self.assertEqual('aa', response.text)