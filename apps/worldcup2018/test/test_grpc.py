# -*- coding: utf-8 -*-
import unittest
from worldcup2018.service.service_pb2_grpc import WorldCupStub
from worldcup2018.service.service_pb2 import Data
import grpc

class TestGrpc(unittest.TestCase):

  def test_get_teams(self):

    with grpc.insecure_channel('localhost:50051') as channel:
      stub = WorldCupStub(channel)
      response = stub.GetGroupTeams(Data(text='you'))
      print("client received: " + response.text)
      self.assertEqual('aa you', response.text)