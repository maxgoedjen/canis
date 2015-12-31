class Song(object):

    def __init__(self, title, artist, album):
        self.title = title
        self.artist = artist
        self.album = album

    def __repr__(self):
        return '{} by {} ({})'.format(self.title, self.artist, self.album or 'No Album')

    def __eq__(self, other):
    	if not other:
    		return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
    	return not (self == other)