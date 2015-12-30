import requests

from canis.song import Song

def id_for_song(song):
	album_subq = '%20album:{}'.format(song.album) if song.album else ''
	query = 'q=track:{}%20artist:{}{}&type=track'.format(song.title, song.artist, album_subq)
	print 'https://api.spotify.com/v1/search?{}'.format(query)
	r = requests.get('https://api.spotify.com/v1/search?{}'.format(query))
	json = r.json()
	track = json['tracks']['items'][0]
	return track['id']

def playlist_id_for_name(name):
	pass

def create_playlist(name):
	pass

def add_song_to_playlist(song_id, playlist_id):
	pass