from os import environ
from urllib import urlencode
from datetime import datetime, timedelta

from flask import Flask, request, redirect, url_for
import requests

app = Flask(__name__)

SPOTIFY_CLIENT_ID = environ['CANIS_SPOTIFY_API_CLIENT_ID']
SPOTIFY_SECRET = environ['CANIS_SPOTIFY_API_SECRET']
SPOTIFY_CALLBACK = environ.get('CANIS_SPOTIFY_API_CALLBACK', 'http://127.0.0.1:5000/callback/')

access_token = None
refresh_token = None
expiration = None
user_id = None

@app.route('/login')
def login():
    args = {
        'client_id': SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': SPOTIFY_CALLBACK,
        'scope': 'playlist-read-private playlist-modify-private playlist-modify-public',
    }
    arg_str = urlencode(args)
    url = 'https://accounts.spotify.com/authorize?{}'.format(arg_str)
    return redirect(url)

@app.route('/callback/')
def callback():
    args = {
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': SPOTIFY_CALLBACK,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_SECRET
    }
    r = requests.post('https://accounts.spotify.com/api/token', data=args)
    resp = r.json()
    store_token_response(resp)
    rm = requests.get('https://api.spotify.com/v1/me', headers={'Authorization': 'Bearer {}'.format(access_token)})
    me = rm.json()
    global user_id
    user_id = me['id']
    shutdown_server()
    return redirect(url_for('login'))

def refresh():
    args = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_SECRET
    }
    r = requests.post('https://accounts.spotify.com/api/token', data=args)
    resp = r.json()
    store_token_response(resp)

def store_token_response(resp):
    global access_token
    global refresh_token
    global expiration
    access_token = resp['access_token']
    if resp.get('refresh_token'):
        refresh_token = resp['refresh_token']
    expiration = datetime.utcnow() + timedelta(seconds=int(resp['expires_in']))

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
