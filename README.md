# canis
Build Spotify playlists off of Sirius XM

## Setup

Canis is best run on a separate server. Canis should run on Python 3.x and 2.7

### Environment Variables

`CANIS_SPOTIFY_API_CLIENT_ID` - `Client ID` from your Spotify application

`CANIS_SPOTIFY_API_SECRET` - `Client Secret` from your Spotify application

`CANIS_SPOTIFY_API_CALLBACK` - `Redirect URL` from your Spotify application

`CANIS_CHANNEL_NAMES` - comma separated list of channel names (example: `Sirius XMU, Alt Nation`)

### Step by Step

1. Go [here](https://developer.spotify.com/my-applications) and create a Spotify Application.
2. Set your callback URL as `http://YOUR_SERVER_URL/callback` (this will be `http://127.0.0.1:5000/callback` if you're running it locally). Note the `Client ID` and `Client Secret`
3. Make sure you set all the environment variables specified above with the values from your Spotify Application.
4. Run `application.py` and navigate to `http://YOUR_SERVER_URL:PORT/login`. Sign into your Spotify account.