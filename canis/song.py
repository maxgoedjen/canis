class Song(object):

	def __init__(self, title, artist, album):
		self.title = title
		self.artist = artist
		self.album = album

	def __repr__(self):
		return '{} by {} ({})'.format(self.title, self.artist, self.album)
