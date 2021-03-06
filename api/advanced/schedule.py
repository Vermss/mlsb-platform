'''
@author: Dallas Fraser
@date: 2019-03-11
@organization: MLSB API
@summary: The views for game schedule
'''
from sqlalchemy.sql.expression import and_

from flask_restful import Resource
from api.model import Game, League
from datetime import datetime, date, time
from api.errors import LeagueDoesNotExist
from api.routes import Routes
from flask import request
from api import cache
from api.variables import PAGE_SIZE, CACHE_TIMEOUT
from api.helper import pagination_response_items


class ScheduleAPI(Resource):
    @cache.memoize(timeout=CACHE_TIMEOUT)
    def get(self, year, league_id):
        """
            Get request for schedule data
            Route: Route['vschedule']/<int:year>/<int:team_id>
            Parameters:
                year: the year to get the schedule for
                league_id: the id of the league
            Returns:
                status: 200
                mimetype: application/json
                data: [
                        {
                            "away_team_id": int,
                            "away_team": str,
                            "date": str,
                            "field": str,
                            "home_team_id": int,
                            "home_team": str,
                            "league_id": int,
                            "score": str(home team - away team),
                            "status": str,
                            "time": str
                        }
                    ]
        """
        page = request.args.get('page', 1, type=int)
        g = (Game.query.filter)
        league = League.query.get(league_id)
        start = datetime.combine(date(year, 1, 1), time(0, 0))
        end = datetime.combine(date(year, 12, 30), time(0, 0))
        if league is None:
            raise LeagueDoesNotExist(payload={'details': league_id})
        games = (Game.query.filter(and_(Game.league_id == league.id,
                                        Game.date.between(start, end)))
                 ).order_by("date").paginate(page, PAGE_SIZE, False)
        data = []
        for game in games.items:
            result = game.json()
            if game.date < datetime.today():
                scores = game.summary()
                result['score'] = (str(scores['home_score']) + '-' +
                                   str(scores['away_score']))
            else:
                result['score'] = ""
            data.append(result)
        url_route = Routes['vschedule'] + "/" + str(year) + "/" + str(league_id)
        return pagination_response_items(games, url_route, data)
