import { useState } from 'react';
import { convertPlaylist } from '../api';

export default function ConvertForm() {
  const [spotifyUrl, setSpotifyUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);

    if (!spotifyUrl.trim()) {
      setError('Please paste a Spotify playlist URL.');
      return;
    }

    try {
      setLoading(true);
      const data = await convertPlaylist(spotifyUrl);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Conversion failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="convert-form">
      <h1>Spotify → YouTube Playlist Converter</h1>
      <p>Paste a Spotify playlist link and get a YouTube playlist in one click.</p>

      <form onSubmit={handleSubmit}>
        <input
          type="url"
          placeholder="https://open.spotify.com/playlist/..."
          value={spotifyUrl}
          onChange={(e) => setSpotifyUrl(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Converting…' : 'Convert'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && result.youtube_playlist_url && (
        <div className="result">
          <p>Conversion status: {result.status}</p>
          <a
            href={result.youtube_playlist_url}
            target="_blank"
            rel="noreferrer"
          >
            Open YouTube Playlist
          </a>
        </div>
      )}
    </div>
  );
}
