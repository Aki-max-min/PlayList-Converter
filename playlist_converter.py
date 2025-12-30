import os
import pickle
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# SPOTIFY CONFIG
# --------------------------------------------------
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    raise RuntimeError("Spotify credentials not found in environment variables")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-read-private playlist-read-collaborative",
        cache_path=".cache",
    )
)

# --------------------------------------------------
# YOUTUBE CONFIG
# --------------------------------------------------
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube"]
YOUTUBE_CLIENT_SECRET_FILE = "client_secret.json"


def get_youtube_service():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                YOUTUBE_CLIENT_SECRET_FILE,
                YOUTUBE_SCOPES,
            )
            creds = flow.run_local_server(port=8080)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)


# --------------------------------------------------
# CORE CONVERSION FUNCTION
# --------------------------------------------------
def convert_playlist(spotify_playlist_url: str) -> str:
    """
    Convert a Spotify playlist URL into a YouTube playlist.
    Returns the YouTube playlist URL.
    """

    # Extract Spotify playlist ID
    playlist_id = spotify_playlist_url.split("/")[-1].split("?")[0]

    # Fetch playlist details
    playlist = sp.playlist(playlist_id)
    playlist_name = playlist["name"]

    # Fetch tracks
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results["items"])

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    # Authenticate YouTube
    youtube = get_youtube_service()

    # ---------------- CREATE YOUTUBE PLAYLIST ----------------
    try:
        yt_playlist = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": f"{playlist_name} (from Spotify)",
                    "description": f"Converted from Spotify playlist: {playlist_name}",
                },
                "status": {"privacyStatus": "private"},
            },
        ).execute()

    except HttpError as e:
        if e.resp.status == 403:
            raise RuntimeError(
                "YouTube API quota exceeded. Please try again tomorrow."
            )
        else:
            raise

    yt_playlist_id = yt_playlist["id"]

    # ---------------- ADD TRACKS ----------------
    for item in tracks:
        track = item["track"]
        if not track:
            continue

        query = f"{track['name']} {track['artists'][0]['name']}"

        try:
            search = youtube.search().list(
                q=query,
                part="id",
                maxResults=1,
                type="video",
            ).execute()

            if search["items"]:
                video_id = search["items"][0]["id"]["videoId"]
                youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": yt_playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id,
                            },
                        }
                    },
                ).execute()

        except HttpError as e:
            if e.resp.status == 403:
                raise RuntimeError(
                    "YouTube API quota exceeded during song addition."
                )
            else:
                continue

    return f"https://www.youtube.com/playlist?list={yt_playlist_id}"
