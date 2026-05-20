from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import shutil
import os
from app.services.replicate import separate_stems, generate_video, generate_song_from_text, assist_lyrics
from pydantic import BaseModel

router = APIRouter()

# Ensure uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class SongRequest(BaseModel):
    prompt: str
    lyrics: Optional[str] = ""

class LyricsRequest(BaseModel):
    topic: str
    style: str

@router.post("/process-audio")
async def process_audio(
    file: UploadFile = File(...),
    action: str = Form(...) # 'vocals_only' or 'stems' or 'remix'
):
    try:
        # Save file locally (in production, upload to S3/GCS first)
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
            
        # In a real scenario, this would be a public URL accessible by Replicate
        # For local dev without ngrok/s3, we just pass the file_location and Replicate mock will handle it
        
        if action in ["vocals_only", "stems"]:
            result = separate_stems(f"https://example.com/audio/{file.filename}")
            return {"status": "success", "result": result}
            
        return {"status": "error", "message": "Unknown action"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-video")
async def create_video(
    audio_url: str = Form(...),
    prompt: str = Form(...)
):
    try:
        result = generate_video(audio_url, prompt)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-song")
async def create_song(request: SongRequest):
    try:
        result = generate_song_from_text(request.prompt, request.lyrics)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assist-lyrics")
async def generate_lyrics(request: LyricsRequest):
    try:
        result = assist_lyrics(request.topic, request.style)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
