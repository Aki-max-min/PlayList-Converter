import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")

# Spotify credentials

SPOTIFY_REDIRECT_URI = "http://127.0.0.1:9999/callback"

# YouTube scopes
YOUTUBE_SCOPES = ["playlist-read-private playlist-read-collaborative user-library-read"]

def get_youtube_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=8080)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

# Spotify setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-read-private playlist-read-collaborative"
))

# Get playlists
print("Fetching your Spotify playlists...\n")
playlists = sp.current_user_playlists(limit=50)

print("Your playlists:")
for idx, playlist in enumerate(playlists['items']):
    print(f"{idx + 1}. {playlist['name']} ({playlist['tracks']['total']} tracks)")

# Select playlist
playlist_num = int(input("\nEnter playlist number: "))
selected_playlist = playlists['items'][playlist_num - 1]

print(f"\nFetching tracks from '{selected_playlist['name']}'...")

# Get tracks
tracks = []
results = sp.playlist_tracks(selected_playlist['id'])
tracks.extend(results['items'])

while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

print(f"Found {len(tracks)} tracks\n")

# Authenticate with YouTube
print("Authenticating with YouTube...")
youtube = get_youtube_service()
print("✓ YouTube authenticated!\n")

# Create YouTube playlist
playlist_title = selected_playlist['name'] + " (from Spotify)"
request = youtube.playlists().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": playlist_title,
            "description": f"Converted from Spotify playlist: {selected_playlist['name']}"
        },
        "status": {
            "privacyStatus": "private"
        }
    }
)
new_playlist = request.execute()
playlist_id = new_playlist['id']

print(f"✓ Created YouTube playlist: {playlist_title}\n")

# Search and add tracks
added = 0
failed = []

for item in tracks:
    track = item['track']
    if not track:
        continue
    
    query = f"{track['name']} {track['artists'][0]['name']}"
    print(f"Searching: {query}")
    
    try:
        search_response = youtube.search().list(
            q=query,
            part='id',
            maxResults=1,
            type='video'
        ).execute()
        
        if search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()
            
            added += 1
            print(f"  ✓ Added\n")
        else:
            failed.append(query)
            print(f"  ✗ Not found\n")
    
    except Exception as e:
        failed.append(query)
        print(f"  ✗ Error: {e}\n")

print(f"\n{'='*50}")
print(f"DONE!")
print(f"Added: {added}/{len(tracks)}")
if failed:
    print(f"\nCouldn't find {len(failed)} songs:")
    for song in failed[:5]:
        print(f"  - {song}")
print(f"{'='*50}")