# -*- coding: utf-8 -*-
import os, time, re, json
from libs.kit import *

URL = 'http://ziliaoku.sports.qq.com/cube/index?cubeId=32&dimId=61&params=t2:4&order=t1&from=sportsdatabase'

class TechLogic(object):
    def __init__(self):
        self.fetch_info()

    def fetch_info(self):
        body = download(URL)
        self._root = json.loads(body)
        data_list = self._root['data']['footballTeamCurSeasonStatByCid']
        self._datas = []
        for row in data_list:
            data = {}
            for key in ['teamId', 'teamCnName', 'goals', 'goalsConceded', 
                'totalScoringAtt', 'ontargetScoringAtt', 'ontargetScoringRate', 
                'wonCorners', 'fkFoulLost', 
                'totalPass', 'passSuccessRate', 
                'totalTackle', 'wonTackleRate',
                'totalOffside', 
                'totalYelCard', 'totalRedCard',
                'saves']:
                data[key] = row[key]
            self._datas.append(data)

    def get_data(self):
        return self._datas

    def get_team_data(self, name):
        for team in self._datas:
            if team['teamCnName'] == name:
                return team

    