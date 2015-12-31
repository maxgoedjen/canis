import requests

from canis import oauth
from canis.song import Song
from canis.memoize import memoize

class NotFound(Exception):
	
	def __init__(self, song):
		self.song = song

def id_for_song(song):
	album_subq = '%20album:{}'.format(song.album) if song.album else ''
	query = 'q=track:{}%20artist:{}{}&type=track'.format(song.title, song.artist, album_subq)
	r = requests.get('https://api.spotify.com/v1/search?{}'.format(query), headers=headers())
	json = r.json()
	try:
		track = json['tracks']['items'][0]
	except Exception:
		# Sometimes album is incorrect, try again without album
		if song.album:
			stripped = Song(song.title, song.artist, None)
			return id_for_song(stripped)
		raise NotFound(song)
	return track['uri']

@memoize
def playlist_id_for_name(name):
	url = 'https://api.spotify.com/v1/users/{}/playlists?limit=50'.format(oauth.user_id)
	r = requests.get(url, headers=headers())
	resp = r.json()
	for playlist in resp['items']:
		if playlist['name'] == name:
			return playlist['id']
	return create_playlist(name)

def create_playlist(name):
	url = 'https://api.spotify.com/v1/users/{}/playlists'.format(oauth.user_id)
	r = requests.post(url, json={'name': name, 'public': 'false'}, headers=headers())
	resp = r.json()
	return resp['id']

def add_song_to_playlist(song_id, playlist_id):
	url = 'https://api.spotify.com/v1/users/{}/playlists/{}/tracks'.format(oauth.user_id, playlist_id)
	r = requests.post(url, json={'uris': [song_id]}, headers=headers())

def headers():
	return {'Authorization': 'Bearer {}'.format(oauth.access_token)}