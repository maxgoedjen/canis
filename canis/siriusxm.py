import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import difflib

from canis.song import Song
from canis.memoize import fresh

class Channel(object):

	def __init__(self, name, href, identifier):
		self.name = name
		self.href = href
		self.identifier = identifier

	def __repr__(self):
		return '{} ({})'.format(self.name, self.identifier)

class NotAvailable(Exception):

	def __init__(self, json):
		self.json = json

def get_channel_list():
	r = requests.get('https://www.siriusxm.com/channellineup/')
	soup = BeautifulSoup(r.text, 'html.parser')
	rows = soup.find_all('td', {'class': 'channelname'})
	items = {}
	for row in rows:
		link = row.find('a')
		name = link.get('title')
		raw_href = link.get('href')
		href = raw_href.replace('/', '')
		items[name] = Channel(name, href, None)
	if items:
		return items
	raise NotAvailable(r.json())

def channels_from_names(names):
	selected = []
	all_channels = get_channel_list()
	all_names = all_channels.keys()
	for channel_name in names:
		matches = difflib.get_close_matches(channel_name, all_names, 1)
		if matches:
			unidentified = all_channels[matches[0]]
			identifier = get_raw_id(unidentified.href)
			selected.append(Channel(unidentified.name, unidentified.href, identifier))
	return selected


def get_raw_id(channel_id):
	r = requests.get('https://www.siriusxm.com/{}'.format(channel_id))
	soup = BeautifulSoup(r.text, 'html.parser')
	for script in soup.find_all('script'):
		matches = re.search('ChannelContentID = "([^"]*)"', script.text)
		if matches:
			return matches.group(1)
	raise NotAvailable(r.json())

@fresh
def get_currently_playing(channel_id):
	raw_time = datetime.utcnow()
	time = raw_time.strftime('%m-%d-%H:%M:00')
	api_url = 'http://www.siriusxm.com/metadata/pdt/en-us/json/channels/{}/timestamp/{}'.format(channel_id, time)
	r = requests.get(api_url)
	json = r.json()
	try:
		current = json['channelMetadataResponse']['metaData']['currentEvent']
		artist_id = current['artists']['id']
	except Exception, e:
		raise NotAvailable(json)
	if not artist_id:
		raise NotAvailable(json)
	artist = current['artists']['name']
	name = current['song']['name']
	album = current['song']['album']['name']
	if album.lower() == 'cd single':
		album = None
	return Song(name, artist, album)

if __name__ == '__main__':
	print(get_currently_playing('siriusxmu'))