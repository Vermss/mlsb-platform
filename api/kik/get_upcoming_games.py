'''
@author: Dallas Fraser
@author: 2015-09-29
@organization: MLSB API
@summary: The route for authenticating a captain
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Player, Team, Game, Bat
from api.errors import PNS
from api.authentication import requires_kik
from flask import session
from api.errors import InvalidField 
from api.variables import UNASSIGNED
from datetime import datetime, timedelta, date
from sqlalchemy import or_
parser = reqparse.RequestParser()
parser.add_argument('kik', type=str, required=True)


class UpcomingGamesAPI(Resource):
    @requires_kik
    def post(self):
        """
            POST request for authenticating a player is a captain of a team
            Route: Route['authenticate_captain']
            Parameters:
                kik: the captain's kik user name (str)
            Returns:
                status: 200 
                mimetype: application/json
                data: id: the captain's team id
        """
        args = parser.parse_args()
        kik = args['kik']
        player = DB.session.query(Player).filter(Player.kik==kik).first()
        if player is None:
            return Response(dumps("{} not registered".format(kik)), status=PNS, mimetype="application/json")
        teams = []

        today = date.today()
        this_week = today + timedelta(days=4)
        for team in player.teams:
            teams.append(team.id)
        games  = DB.session.query(Game).filter(or_(Game.away_team_id.in_(teams),
                                                  (Game.home_team_id.in_(teams))))
        games = games.filter(Game.date.between(today,this_week ))
        print(str(games))
        result = []
        for game in games:
            result.append(game.json())
        return Response(dumps(result), status=200, mimetype="application/json")
