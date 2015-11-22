'''
Name: Dallas Fraser
Date: 2014-08-22
Project: MLSB API
Purpose: To create an application to act as an api for the database
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Team
from datetime import date
from api.authentication import requires_admin
parser = reqparse.RequestParser()
parser.add_argument('sponsor_id', type=int)
parser.add_argument('color', type=str)
parser.add_argument('league_id', type=int)
parser.add_argument('year', type=int)
parser.add_argument('espys', type=int)

post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('sponsor_id', type=int, required=True)
post_parser.add_argument('color', type=str, required=True)
post_parser.add_argument('league_id', type=int, required=True)
post_parser.add_argument('year', type=int, required=True)
post_parser.add_argument('espys', type=int)

class TeamAPI(Resource):
    def get(self, team_id):
        """
            GET request for Team Object matching given team_id
            Route: Routes['team']/<team_id:int>
            Returns:
                if found
                    status: 200 
                    mimetype: application/json
                    data:  
                        {
                           'team_id':  int,
                           'team_name': string,
                           'color': string,
                           'sponsor_id': int,
                           'league_id': int,
                           'year': int,
                           'espys': int,
                           'captain': string
                        }
                otherwise
                    status: 404 
                    mimetype: application/json
                    data:  
                        None
        """
        # expose a single team
        entry  = Team.query.get(team_id)
        response = Response(dumps(None),
                            status=404, mimetype="application/json")
        if entry is not None:
            response = Response(dumps(entry.json()), status=200,
                                mimetype="application/json")
        return response

    @requires_admin
    def delete(self, team_id):
        """
            DELETE request for Team
            Route: Routes['team']/<team_id:int>
            Returns:
                if found
                    status: 200 
                    mimetype: application/json
                    data: None
                otherwise
                    status: 404 
                    mimetype: application/json
                    data: None
        """
        team = Team.query.get(team_id)
        response = Response(dumps(None), status=404, mimetype="application/json")
        if team is not None:
            # delete a single team
            DB.session.delete(team)
            DB.session.commit()
            response = Response(dumps(None), status=200,
                                mimetype="application/json")
        return response

    @requires_admin
    def put(self, team_id):
        """
            PUT request for team
            Route: Routes['team']/<team_id:int>
            Parameters :
                team_id: The team's id (int)
                team_name: The team's name (string)
                sponsor_id: The sponsor's id (int)
                league_id: The league's id (int)
                color: the color of the team (string)
                year: the year of the team (int)
                espys: the total espys points of the team (int)
            Returns:
                if found and updated successfully
                    status: 200 
                    mimetype: application/json
                    data: None
                otherwise possible errors are
                    status: 404, IFSC, LDNESC, PDNESC or SDNESC
                    mimetype: application/json
                    data: None
        """
        # update a single user
        team = Team.query.get(team_id)
        args = parser.parse_args()
        response = Response(dumps(None), status=404,
                            mimetype="application/json")
        color = None
        sponsor_id = None
        league_id = None
        espys = None
        year = None
        if team is not None:
            if args['color']:
                color = args['color']
            if args['sponsor_id']:
                sponsor_id = args['sponsor_id']
            if args['league_id']:
                league_id = args['league_id']
            if args['espys']:
                espys = args['espys']
            if args['year']:
                year = args['year']
            team.update(color=color,
                        sponsor_id=sponsor_id,
                        league_id=league_id,
                        year=year,
                        espys=espys
                        )
            DB.session.commit()
            response = Response(dumps(None), status=200,
                                mimetype="application/json")
        return response

    def option(self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }

class TeamListAPI(Resource):
    def get(self):
        """
            GET request for Teams List
            Route: Routes['team']
            Parameters :
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    teams: [  {
                                'team_id':  int,
                               'team_name': string,
                               'color': string,
                               'sponsor_id': int,
                               'league_id': int,
                               'year': int,
                               'espys': int,
                               'captain': string
                                }
                              ,{...}
                            ]
        """
        # return a list of teams
        teams = Team.query.all()
        result = []
        for i in range(0, len(teams)):
            result.append(teams[i].json())
        resp = Response(dumps(result), status=200, mimetype="application/json")
        return resp

    @requires_admin
    def post(self):
        """
            POST request for Teams List
            Route: Routes['team']
            Parameters :
                league_id: the league's id (int)
                sponsor_id: the sponsor's id (int)
                color: the color of the team (string)
                year: the year the team is playing in (int)
                espys: the team espys points (int)
            Returns:
                if successful
                    status: 200 
                    mimetype: application/json
                    data: the create team id (int)
                possible errors
                    status: 400, IFSC, LDNESC, PDNESC or SDNESC
                    mimetype: application/json
                    data: the create team id (int)
        """
        # create a new user
        args = post_parser.parse_args()
        color = None
        sponsor_id = None
        league_id = None
        year = date.today().year
        espys = 0
        if args['color']:
            color = args['color']
        if args['sponsor_id']:
            sponsor_id = args['sponsor_id']
        if args['league_id']:
            league_id = args['league_id']
        if args['espys']:
            espys = args['espys']
        if args['year']:
            year = args['year']
        t = Team(color=color,
                 sponsor_id=sponsor_id,
                 league_id=league_id,
                 year=year,
                 espys=espys)
        DB.session.add(t)
        DB.session.commit()
        result = t.id
        return Response(dumps(result), status=200, mimetype="application/json")

    def options (self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }
