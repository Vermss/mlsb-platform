'''
@author: Dallas Fraser
@author: 2015-09-29
@organization: MLSB API
@summary: The views for player stats
'''
from sqlalchemy.sql.expression import or_
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Team, Player, roster, Bat, Game
parser = reqparse.RequestParser()
parser.add_argument('email', type=str)
parser.add_argument('player_name', type=str)

class PlayerLookupAPI(Resource):
    def post(self):
        """
            POST request to lookup Player
            Route: Route['player_lookup']
            Parameters:
                email: the league id (str)
                player_name: the player id (str)
            Returns:
                status: 200 
                mimetype: application/json
                data: list of possible Players
        """
        player_name = None
        data = []
        response = {'success': True,
                  'message': '',
                  'failures': [],
                  'data': {}}
        args = parser.parse_args()
        players = None
        if args['email']:
            # guaranteed to find player
            players = Player.query.filter(Player.email==args['email']).all()
        elif args['player_name']:
            # maybe overlap
            players = Player.query.filter(Player.name.contains(args['player_name'])).all()
        if players is not None:
            for player in players:
                data.append(player.json())
        response['data'] = data
        return Response(dumps(response), status=200, mimetype="application/json")
