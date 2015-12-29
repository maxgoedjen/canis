import requests

class Channel(object):

	def __init__(self, name, identifier):
		self.name = name
		self.identifier = identifier

class Song(object):

	def __init__(self, title, artist):
		self.title = title
		self.artist = artist

def get_channel_list():
	r = requests.get('https://www.siriusxm.com/channellineup/')
	print r.text

def get_currently_playing(channel_identifier):
	pass

if __name__ == '__main__':
	print(get_channel_list())