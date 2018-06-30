# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, jsonify
from .logic.worldcup import WorldCupLogic
from .logic.tech import TechLogic
from libs.kit import *

worldcup = Blueprint('worldcup', __name__, template_folder='pages')

logic = WorldCupLogic()
logic.reset()

tech = TechLogic()

@worldcup.route('/api/getGroupTeams')
def api_get_group_teams():
    return jsonify(logic._teams)

@worldcup.route('/api/getGroupMatches')
def api_get_group_matches():
    return jsonify(logic._matches)

@worldcup.route('/api/getLotteryData')
def api_get_lottery_data():
    logic._lottery.fetch_info()
    return jsonify(logic._lottery._data)

@worldcup.route('/api/getTechs')
def api_get_techs():
    return jsonify(tech.get_data())

@worldcup.route('/api/getTech/<team>')
def api_get_team_tech(team):
    return jsonify(tech.get_team_data(team))

@worldcup.route('/api/reset')
def api_reset():
    logic.reset()
    tech.fetch_info()
    return jsonify({'errno': 0})

@worldcup.route('/')
def get_index():
    return render_template('worldcup/index.html', groups=logic._teams, matches=logic._matches)

@worldcup.route('/refresh')
def get_refresh():
    logic.reset()
    return render_template('worldcup/index.html', groups=logic._teams, matches=logic._matches)

@worldcup.route('/forecast',methods=['GET','POST'])
def forecast():
    if request.method =='POST':
        for mid, result in request.form.items():
            if result == '':
                continue
            result = result.split(',')
            logic.set_match(mid[0], int(mid[1]), [int(result[0]), int(result[1])], True)
    else:
        pass
    return render_template('worldcup/index.html', groups=logic._teams, matches=logic._matches)   

@worldcup.route('/lottery')
def get_lottery():
    return render_template('worldcup/lottery.html')