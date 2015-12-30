import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class Channel(object):

	def __init__(self, name, identifier):
		self.name = name
		self.identifier = identifier

	def __repr__(self):
		return '{} ({})'.format(self.name, self.identifier)

class Song(object):

	def __init__(self, title, artist, album):
		self.title = title
		self.artist = artist
		self.album = album

	def __repr__(self):
		return '{} by {} ({})'.format(self.title, self.artist, self.album)

class NotAvailable(Exception):
	pass

def get_channel_list():
	r = requests.get('https://www.siriusxm.com/channellineup/')
	soup = BeautifulSoup(r.text, 'html.parser')
	rows = soup.find_all('td', {'class': 'channelname'})
	items = []
	for row in rows:
		link = row.find('a')
		name = link.get('title')
		raw_href = link.get('href')
		href = raw_href.replace('/', '')
		items.append(Channel(name, href))
	if items:
		return items
	raise NotAvailable()

def get_raw_id(channel_id):
	r = requests.get('https://www.siriusxm.com/{}'.format(channel_id))
	soup = BeautifulSoup(r.text, 'html.parser')
	for script in soup.find_all('script'):
		matches = re.search('ChannelContentID = "([^"]*)"', script.text)
		if matches:
			return matches.group(1)
	raise NotAvailable()

def get_currently_playing(channel_id):
	raw_id = get_raw_id(channel_id)
	raw_time = datetime.utcnow()
	time = raw_time.strftime('%m-%d-%H:%M:00')
	api_url = 'http://www.siriusxm.com/metadata/pdt/en-us/json/channels/{}/timestamp/{}'.format(raw_id, time)
	r = requests.get(api_url)
	json = r.json()
	current = json['channelMetadataResponse']['metaData']['currentEvent']
	artist_id = current['artists']['id']
	if not artist_id:
		raise NotAvailable()
	artist = current['artists']['name']
	name = current['song']['name']
	album = current['song']['album']['name']
	if album == 'CD Single':
		album = None
	return Song(name, artist, album)

if __name__ == '__main__':
	print(get_currently_playing('siriusxmu'))