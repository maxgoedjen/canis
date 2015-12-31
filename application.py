from time import sleep
from datetime import datetime
import traceback

from canis import siriusxm, spotify, oauth

def main():
    channel_names = ['Sirius XMU', 'Alt Nation']
    channels = siriusxm.channels_from_names(channel_names)
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
            except spotify.NotFound, e:
                print('Unable to find {} on Spotify'.format(e.song))
            except siriusxm.NotAvailable, e:
                print('Unable load data for {}'.format(channel))
            except Exception, e:
                print('Error {} {}'.format(e, traceback.format_exc()))
        sleep(60)

if __name__ == "__main__":
    oauth.app.run()
    main()