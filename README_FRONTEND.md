Prerequisites

- Python 3.8+
- Node.js 16+
- Spotify Developer Account (for Client ID & Secret)
- Google Cloud Project with YouTube Data API enabled

Get API Credentials

#### Spotify
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy **Client ID** and **Client Secret**
4. Add Redirect URI: `http://127.0.0.1:9999/callback`

#### YouTube
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create **Desktop App** OAuth credentials
5. Download `client_secret.json` and place it in the project root

Frontend Setup

cd frontend
npm install
npm run dev

Run Backend

uvicorn main:app --reload

Backend runs on `http://127.0.0.1:8000`  
Frontend runs on `http://localhost:5173`

## Usage

1. Open `http://localhost:5173` in your browser
2. Paste a Spotify playlist URL
3. Click **"Fetch Playlist!"**
4. Complete Spotify and YouTube OAuth flows (first time only)
5. Get your YouTube playlist link and share!

## API Endpoints

### POST `/convert`

Converts a Spotify playlist to YouTube.

## NOTE
RUN BOTH FRONTEND AND BACKEND IN DIFFERENT TERMINAL AT THE SAME TIME 

## Project Structure
PlayList-Converter/
├── main.py # FastAPI app entry point
├── playlist_converter.py # Core conversion logic
├── requirements.txt # Python dependencies
├── .env.example # Environment variables template
├── client_secret.json # Google OAuth credentials (add this)
├── .cache # Spotify token cache (auto-generated)
├── token.pickle # YouTube token cache (auto-generated)
├── frontend/ # React frontend
│ ├── src/
│ │ ├── App.jsx
│ │ ├── App.css
│ │ ├── components/
│ │ │ └── ConvertForm.jsx
│ │ ├── api.js
│ │ └── main.jsx
│ ├── package.json
│ └── README.md
└── README.md # This file