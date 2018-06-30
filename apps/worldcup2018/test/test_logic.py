# -*- coding: utf-8 -*-
import unittest
from logic.worldcup import WorldCupLogic
from libs.kit import *

logic = WorldCupLogic()
logic.reset()
logic.output()

class TestWorldCupLogic(unittest.TestCase):

    """Test WorldCupLogic"""

    def test_get_teams(self):
        # print(logic._teams)
        self.assertTrue(True)

    def test_get_match(self):
        logic.reset()
        match = logic.get_match('A', 1)
        logic.print_match(match)
        self.assertEqual(match['a_result'][0], 5)

    def test_forecast_1(self):
        ''' 葡萄牙0:0伊朗, 西班牙1:0摩洛哥'''
        logic.reset()
        logic.set_match('B', 6, [0,0])
        logic.set_match('B', 5, [1,0])
        print('\nGROUP: ##### B #######\n')
        for team in logic._teams[1]:
            logic.print_team(team)
        self.assertTrue(True)

    def test_forecast_2(self):
        ''' 葡萄牙0:0伊朗, 西班牙0:2摩洛哥'''
        logic.reset()
        logic.set_match('B', 6, [0,0])
        logic.set_match('B', 5, [0,2])
        # logic.output()
        print('\nGROUP: ##### B #######\n')
        for team in logic._teams[1]:
            logic.print_team(team)
        self.assertTrue(True)

    def test_rank_group(self):
        ''' D Group List rank_group'''
        logic.reset()
        logic.set_match('D', 4, [0,0])
        logic.set_match('D', 5, [0,0])
        logic.set_match('D', 6, [3,1])
        # logic.output()
        print('\nGROUP: ##### D #######\n')
        for team in logic._teams[3]:
            logic.print_team(team)
        self.assertTrue(True)

    def test_progress_top16(self):
        ''' D Group List progress_top16'''
        logic.reset()
        logic.set_match('D', 4, [0,0])
        logic.set_match('D', 5, [0,0])
        logic.set_match('D', 6, [3,1])
        logic.progress_top16()
        matches_1_8 = logic.get_top16_matches()
        print('\n', logic._teams_16)
        for key, match in matches_1_8.items():
            print('\n', match)
        self.assertTrue(True)

