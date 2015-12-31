import requests

from canis.song import Song

class NotFound(Exception):
	
	def __init__(self, song):
		self.song = song

def id_for_song(song):
	album_subq = '%20album:{}'.format(song.album) if song.album else ''
	query = 'q=track:{}%20artist:{}{}&type=track'.format(song.title, song.artist, album_subq)
	r = requests.get('https://api.spotify.com/v1/search?{}'.format(query))
	json = r.json()
	try:
		track = json['tracks']['items'][0]
	except Exception:
		raise NotFound(song)
	return track['uri']

def playlist_id_for_name(name):
	pass

def create_playlist(name):
	pass

def add_song_to_playlist(song_id, playlist_id):
	pass
