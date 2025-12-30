from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from playlist_converter import convert_playlist
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConvertRequest(BaseModel):
    spotify_playlist_url: str

class ConvertResponse(BaseModel):
    status: str
    youtube_playlist_url: str

@app.post("/convert", response_model=ConvertResponse)
def convert(req: ConvertRequest):
    try:
        print("👉 Incoming request:", req.spotify_playlist_url)
        yt_url = convert_playlist(req.spotify_playlist_url)
        return {
            "status": "success",
            "youtube_playlist_url": yt_url
        }
    except Exception as e:
        print("\n🔥🔥🔥 REAL BACKEND ERROR 🔥🔥🔥")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
