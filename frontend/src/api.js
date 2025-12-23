const BASE_URL = 'http://localhost:8000';

export async function convertPlaylist(spotifyUrl) {
  const res = await fetch(`${BASE_URL}/convert`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ spotify_playlist_url: spotifyUrl }),
  });

  if (!res.ok) {
    throw new Error(`Request failed with status ${res.status}`);
  }

  return res.json(); // { status, youtube_playlist_url }
}
