
# Spotify to YouTube Playlist Converter (Backend)

This repository contains the backend service for converting a Spotify playlist into a YouTube playlist.
The backend is implemented using FastAPI and exposes a REST API that can be consumed by a frontend application.



## Why This Project?

Migrating playlists between music platforms is a common real-world problem.
This project demonstrates how to integrate multiple third-party APIs securely while designing a backend that is scalable, frontend-friendly, and safe for collaboration.

The project showcases:

* OAuth 2.0 authentication
* Spotify and YouTube API integration
* RESTful API design using FastAPI
* Secure handling of secrets and tokens
* Backend–frontend collaboration readiness



## Features

* Converts Spotify playlists to YouTube playlists
* Uses Spotify Web API and YouTube Data API v3
* Secure OAuth authentication flow
* FastAPI backend with interactive API documentation
* CORS enabled for frontend integration
* Environment-variable based secret management



## Tech Stack

* Python
* FastAPI
* Uvicorn
* Spotipy (Spotify Web API)
* Google API Client (YouTube Data API v3)
* OAuth 2.0
* RESTful API design



## Project Structure

```
.
├── main.py                 # FastAPI application and routes
├── playlist_converter.py   # Core playlist conversion logic
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignored secrets and cache files
├── .env.example            # Environment variable template
└── README.md               # Project documentation
```

---

## Quick Start

```bash
git clone <repository-url>
cd <repository-name>
pip install -r requirements.txt
uvicorn main:app --reload
```

Open the API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Environment Variables

Create a `.env` file locally. This file must not be committed to GitHub.

### `.env.example`

```env
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
YOUTUBE_CLIENT_SECRET=
```

### `.env` (local only)

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
```

---

## OAuth Setup

### Spotify OAuth

1. Go to the Spotify Developer Dashboard
2. Create a new app
3. Add the redirect URI:

   ```
   http://127.0.0.1:9999/callback
   ```

---

### YouTube OAuth

1. Create a Google Cloud project
2. Enable **YouTube Data API v3**
3. Create OAuth Client ID

   * Application type: Desktop app
4. Download the OAuth JSON file
5. Rename it to:

   ```
   client_secret.json
   ```
6. Place it in the project root directory

This file is ignored by Git and must never be committed.

---

## Running the Backend

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The server will be available at:

```
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI provides interactive documentation via Swagger UI.

Open:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoint

### Convert Playlist

**POST** `/convert`

#### Request Body

```json
{
  "spotify_playlist_url": "https://open.spotify.com/playlist/..."
}
```

#### Response

```json
{
  "status": "success",
  "youtube_playlist_url": "https://www.youtube.com/playlist?list=..."
}
```

---

## Frontend Integration

* Backend base URL: `http://localhost:8000`
* Endpoint: `POST /convert`
* Accepts and returns JSON
* CORS is enabled for development

Frontend developers do not require Spotify or YouTube credentials.

---

## Security Notes

* Secrets are stored using environment variables
* OAuth tokens are generated locally and ignored by Git
* `.env`, `client_secret.json`, and token files must never be committed
* Each developer must use their own API credentials

---

## First-Time Authentication Behavior

On the first request:

* Spotify OAuth login opens in the browser
* YouTube OAuth permission screen appears
* Tokens are generated and stored locally

This happens only once per environment.

---

## Known Limitations

* Some tracks may not be found on YouTube
* Conversion speed depends on YouTube search results
* API rate limits apply for both Spotify and YouTube

---

## Contributors

* **Backend**: Designed and implemented the FastAPI backend, OAuth authentication, Spotify and YouTube API integration, and API contract.
* **Frontend**: Implemented the user interface and API consumption.

---

## Project Status

Backend implementation is complete and ready for frontend integration.

---


