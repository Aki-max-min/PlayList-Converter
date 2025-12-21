from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from playlist_converter import convert_playlist  # we'll create this function

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all during development
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
        yt_url = convert_playlist(req.spotify_playlist_url)
        return {
            "status": "success",
            "youtube_playlist_url": yt_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
