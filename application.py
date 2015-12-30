from canis import siriusxm, spotify

def main():
	try:
		current = siriusxm.get_currently_playing('siriusxmu')
		spotify_id = spotify.id_for_song(current)
		print(current, spotify_id)
	except Exception, e:
		print "Error {}".format(e)

if __name__ == '__main__':
	main()