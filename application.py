from time import sleep
from datetime import datetime
import traceback
from os import environ

from canis import siriusxm, spotify, oauth

CHANNEL_NAMES = environ['CANIS_CHANNEL_NAMES'].split(',')

def main():
    channels = siriusxm.channels_from_names(CHANNEL_NAMES)
    print('Monitoring channels: {}'.format(channels))
    while True:
        if oauth.expiration < datetime.utcnow():
            print('Refreshing Spotify token')
            oauth.refresh()
        for channel in channels:
            try:
                current, fresh = siriusxm.get_currently_playing(channel.identifier)
                if fresh:
                    spotify_id = spotify.id_for_song(current)
                    playlist_id = spotify.playlist_id_for_name(channel.name)
                    spotify.add_song_to_playlist(spotify_id, playlist_id)
                    print('Added {} - {} to {}'.format(current, spotify_id, channel.name))
            except spotify.NotFound as e:
                print('Unable to find {} on Spotify'.format(e.song))
            except siriusxm.NotAvailable as e:
                print('Unable load data for {} {}'.format(channel, e.json))
            except Exception as e:
                print('Error {} {}'.format(e, traceback.format_exc()))
        sleep(60)

if __name__ == "__main__":
    oauth.app.run(host='0.0.0.0')
    main()