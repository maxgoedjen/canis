from time import sleep
from datetime import datetime
from canis import siriusxm, spotify, oauth

def main():
    channels = ['siriusxmu', 'altnation']
    while True:
        if oauth.expiration > datetime.utcnow():
            oauth.refresh()
        for channel in channels:
            try:
                current = siriusxm.get_currently_playing(channel)
                spotify_id = spotify.id_for_song(current)
                print '{} - {}'.format(current, spotify_id)
            except Exception, e:
                print "Error {}".format(e)
        sleep(60)

if __name__ == "__main__":
    oauth.app.run()
    main()
