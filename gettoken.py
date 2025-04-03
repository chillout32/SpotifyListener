import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Authenticate using Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="2e8b7224885b428cb9aab93661e4a490",
                                               client_secret="e890f1aafc58483aa9afbcfbdc642b1e",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope=["user-library-read", "user-library-modify", "app-remote-control", "user-read-playback-state"]))

token_info = sp.auth_manager.get_access_token(sp.auth_manager.cache_handler.get_cached_token())
# Now you can make authenticated requests
if token_info:
    print(f"Access Token: {token_info['access_token']}")
else:
    print("Access token not found.")