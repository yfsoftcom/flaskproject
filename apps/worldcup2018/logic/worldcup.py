# -*- coding: utf-8 -*-
import os, time, re, json
from operator import itemgetter, attrgetter
from libs.kit import *
from .lottery import LotteryLogic


ASCII_A = 65
WIN_SCORE = 3
EQUAL_SCORE = 1
class WorldCupLogic(object):
    def __init__(self):
        self._lottery = LotteryLogic()
        # self._lottery.fetch_info()
        self._teams = []
        self._teams_16 = []
        self._teams_8 = []
        self._teams_4 = []
        self._teams_2 = []
        self._champion = None

        self._finished_matches = [
            [ [5,0], [0,1], [3,1], [1,0], [-1,-1], [-1,-1] ], # a
            [ [3,3], [0,1], [1,0], [0,1], [-1,-1], [-1,-1] ], # b
            [ [2,1], [0,1], [1,0], [1,1], [-1,-1], [-1,-1] ], # c
            [ [1,1], [2,0], [0,3], [-1,-1], [-1,-1], [-1,-1] ], # d
            [ [1,1], [0,1], [2,0], [-1,-1], [-1,-1], [-1,-1] ], # e
            [ [0,1], [1,0], [-1,-1], [-1,-1], [-1,-1], [-1,-1] ], # f
            [ [3,0], [1,2], [-1,-1], [-1,-1], [-1,-1], [-1,-1] ], # g
            [ [1,2], [1,2], [-1,-1], [-1,-1], [-1,-1], [-1,-1] ]  # h
        ]
    def get_teams_name(self):
        return [["俄罗斯", "沙特", "埃及", "乌拉圭"], ["葡萄牙", "西班牙", "摩洛哥", "伊朗"], ["法国", "澳大利亚", "秘鲁", "丹麦"], ["阿根廷", "冰岛", "克罗地亚", "尼日利亚"], ["巴西", "瑞士", "哥斯达黎加", "塞尔维亚"], ["德国", "墨西哥", "瑞典", "韩国"], ["比利时", "巴拿马", "突尼斯", "英格兰"], ["波兰", "塞内加尔", "哥伦比亚", "日本"]]

    def reset(self):
        teams = self.get_teams_name()
        self._teams = []
        # reset teams name, score, goals, ranking
        for i in range(0,8):
            group = []
            for j in range(0,4):
                group.append([teams[i][j], 0, 0, -1])
            self._teams.append(group) # name, score, goals, sort
        self._matches = self.get_void_matches()
        self.reset_finished_matches()

    # http://matchweb.sports.qq.com/matchUnion/list?startTime=2018-06-14&endTime=2018-07-20&columnId=4&index=0
    def fetch_group_match_sechdule(self):
        group_match_sechdule = []
        body = download('http://matchweb.sports.qq.com/matchUnion/list?startTime=2018-06-14&endTime=2018-07-20&columnId=4&index=0')
        data_dict = json.loads(body)['data']
        for date, matches in data_dict.items():
            for match in matches:
                result = [-1, -1]
                if match['matchPeriod'] != '0': # finished
                    result = [ int(match['leftGoal']), int(match['rightGoal'])]
                group_match_sechdule.append([ match['leftName'], match['rightName'], match['startTime'], result])
        return group_match_sechdule

    def reset_finished_matches(self):
        # get the finished matches
        A = ASCII_A
        for matches in self._finished_matches:
            i = 1
            for result in matches:
                if result[0] == -1:
                    continue
                self.set_match(chr(A), i, result)
                i = i + 1
            A = A + 1

    def output(self):
        print('################################## Matches ###################################\n')
        for g in self._matches:
            g_list = self._matches[g]
            for m in g_list:
                self.print_match(m)
            print('\n###################################################\n\n')

        print('\n################################## Matches ###################################')

    def print_match(self, m):
        print("{id}: {h}\t{h1}:{g1}\t{g}".format(id=m['id'], h=m['H'], g=m['G'], h1=m['a_result'][0], g1=m['a_result'][1]))

    def print_team(self, t):
        print("Name:[{name}] \tScore:[{score}] \tGoals:[{goals}] \tRanking:[{ranking}]".format(name=t[0],score=t[1],goals=t[2],ranking=t[3]))

    def get_match(self, g, mid):
        return self._matches[ord(g)][mid - 1]

    def set_match(self, g, mid, result, fake = False):
        match = self._matches[ord(g)][mid - 1]
        if match['state'] != 0:
            raise Exception('seted!')
        match['a_result'] = result
        if fake:
            match['state'] = 2
        else:
            match['state'] = 1
        self.change_score(match)
        return match

    def change_score(self, match):
        group_index = match['group']
        host_index = match['Hi']
        guest_index = match['Gi']
        result = match['a_result']
        if result[0] == -1:
            return
        self._teams[group_index][host_index][2] = self._teams[group_index][host_index][2] + result[0] - result[1]
        self._teams[group_index][guest_index][2] = self._teams[group_index][guest_index][2] + result[1] - result[0]
        if result[0] > result[1]: # host win
            self._teams[group_index][host_index][1] = self._teams[group_index][host_index][1] + WIN_SCORE 
        elif result[0] < result[1]: # guest win
            self._teams[group_index][guest_index][1] = self._teams[group_index][guest_index][1] + WIN_SCORE 
        else:
            self._teams[group_index][host_index][1] = self._teams[group_index][host_index][1] + EQUAL_SCORE 
            self._teams[group_index][guest_index][1] = self._teams[group_index][guest_index][1] + EQUAL_SCORE

        self.rank_group(group_index)

    def rank_group(self, g):
        # score-, goals-
        datas = []
        teams = self._teams[g]
        for i, team in enumerate(teams):
            datas.append([i, team[1], team[2]])
        datas = sorted(datas, key = itemgetter(1,2), reverse = True)
        for i, team in enumerate(datas):
            index = team[0]
            teams[index][3] = i + 1

    def progress_top16(self):
        self._teams_16 = []
        for group in self._teams:
            winers = [None, None]
            for team in group:
                ranking = team[3]
                if ranking == 1:
                    winers[0] = team
                elif ranking == 2:
                    winers[1] = team
            self._teams_16.append(winers)
                
    def get_top16_matches(self):
        groups_matches = {}
        A = ASCII_A
        for i in range(0,4):
            group_matches = []
            for j, item in enumerate( [ [(i * 2,0), (i * 2 + 1,1)], [ (i * 2,1), (i * 2 + 1,0)] ] ):
                (g1, t1) = item[0]
                (g2, t2) = item[1]
                h = self._teams_16[g1][t1] 
                g = self._teams_16[g2][t2] 
                group_matches.append({
                    'id': '1_8-' + chr(A) + str(j + 1),
                    'H': h[0],
                    'G': g[0],
                    'Hi': item[0],
                    'Gi': item[1],
                    'a_result': [-1,-1],
                    'forecast': [-1,-1],
                    'state': 0
                }) 
            groups_matches[i] = group_matches
            A = A + 1
        return groups_matches

    def progress_top8(self):
        pass
        

    def progress_top4(self):
        pass

    def progress_champion(self):
        pass

    def get_void_matches(self):
        sechdules = self.fetch_group_match_sechdule()
        groups_matches = {}
        A = ASCII_A
        for group in self._teams:
            group_matches = []
            i = 0
            for (x,y) in [ (0,1), (2,3), (0,2), (3,1), (1,2), (0,3)]:
                i = i + 1
                h = group[x][0]
                g = group[y][0]
                match = {
                    'id': chr(A) + str(i),
                    'group': A - ASCII_A,
                    'H': h,
                    'G': g,
                    'Hi': x,
                    'Gi': y,
                    'a_result': [-1,-1],
                    'forecast': [-1,-1],
                    'state': 0
                }
                found_flag = False
                # get sechdule
                for s in sechdules:
                    s_h = s[0]
                    s_g = s[1]
                    s_time = s[2]
                    s_r = s[3]
                    if str_include(s_h, h) and str_include(s_g, g):
                        self._finished_matches[A - ASCII_A][i-1] = s_r
                        match['starttime'] = s_time
                        found_flag = True
                        break
                    if str_include(s_h, g) and str_include(s_g, h):
                        s_r.reverse()
                        self._finished_matches[A - ASCII_A][i-1] = s_r
                        match['starttime'] = s_time
                        found_flag = True
                        break
                if not found_flag:
                    if match['id'] != 'D2':
                        raise Exception('No This Game: %s' % match)
                # match['lottery'] = self._lottery.get_point(match)
                group_matches.append(match)
            groups_matches[A] = group_matches
            A = A + 1
        return groups_matches





