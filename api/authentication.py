'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Holds the authentication functions
'''
from functools import wraps
from flask import request, Response
from flask import session
import os
from api.model import Team, Player

ADMIN = os.environ['ADMIN']
PASSWORD = os.environ['PASSWORD']
KIK = os.environ['KIK']
KIKPW = os.environ['KIKPW']

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == ADMIN and password == PASSWORD


def check_kik(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == KIK and password == KIKPW


def check_captain(player, password):
    '''
    check a if a player is the captain of a team
    '''
    players = Player.query.filter_by(name=player).all()
    player = None
    for p in players:
        if p.check_password(password):  # correct password
            player = p
    if player is None:
        return authenticate()
    session['captain'] = player.id
    return True


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        elif 'admin' in session and 'password' in session:
            # check if user signed in already
            logged = check_auth(session['admin'], session['password'])
            if not logged:
                return authenticate()
        return f(*args, **kwargs)
    return decorated


def requires_kik(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_kik(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def requires_captain(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_captain(auth.name, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
