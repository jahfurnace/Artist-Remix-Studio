import replicate
from app.core.config import settings

def separate_stems(audio_file_url: str):
    """
    Uses Replicate to separate stems from an audio file.
    Model: hf-audio/demucs or similar audio separation model.
    """
    if not settings.REPLICATE_API_TOKEN:
        print("Warning: REPLICATE_API_TOKEN not set. Mocking response.")
        return {
            "vocals": "mock_vocals_url.mp3",
            "bass": "mock_bass_url.mp3",
            "drums": "mock_drums_url.mp3",
            "other": "mock_other_url.mp3",
        }
        
    try:
        output = replicate.run(
            "cjwbw/demucs:25a173108cff36ef9f80f854c162d01df9e6528be175794b80c2c626ce8f32ec",
            input={"audio": audio_file_url}
        )
        return output
    except Exception as e:
        print(f"Replicate API error: {e}")
        raise e

def generate_video(audio_file_url: str, prompt: str):
    """
    Generates an audio-reactive video using Replicate.
    """
    if not settings.REPLICATE_API_TOKEN:
        print("Warning: REPLICATE_API_TOKEN not set. Mocking response.")
        return {"video_url": "mock_video_url.mp4"}
        
    try:
        output = replicate.run(
            "deforum-art/deforum-stable-diffusion:e22e77495f2fb83c34d5fae2ad8ab63c0a87b6b573b6208e1535b0e0086c8f6e",
            input={"max_frames": 100, "audio_input": audio_file_url, "animation_prompts": prompt}
        )
        return output
    except Exception as e:
        print(f"Replicate API error: {e}")
        raise e

def generate_song_from_text(prompt: str, lyrics: str = ""):
    """
    Generates music/song from text and lyrics using models like MusicGen or Suno.
    """
    if not settings.REPLICATE_API_TOKEN:
        print("Warning: REPLICATE_API_TOKEN not set. Mocking song generation.")
        return {"song_url": "mock_generated_song_url.mp3", "status": "success"}
        
    try:
        # Example using Meta's MusicGen on Replicate
        output = replicate.run(
            "meta/musicgen:7a76a8258b23fae65c5a22debb8ceecf62e7462440c81d6d628d0f1ebbfddbc3",
            input={"prompt": f"{prompt} | Lyrics: {lyrics}", "model_version": "stereo-melody", "duration": 30}
        )
        return {"song_url": output}
    except Exception as e:
        print(f"Replicate API error: {e}")
        raise e

def assist_lyrics(topic: str, style: str):
    """
    Uses an LLM (like Llama 2/3 on Replicate) to write or rewrite lyrics.
    """
    if not settings.REPLICATE_API_TOKEN:
        print("Warning: REPLICATE_API_TOKEN not set. Mocking lyrics.")
        return {"lyrics": f"(Verse 1)\nWalking down the street feeling so {style}\nThinking about {topic} all the time...\n\n(Chorus)\nOh yeah, we're gonna make it right\nShining like a star in the night"}
        
    try:
        prompt = f"Write a {style} song about {topic}. Include Verse and Chorus."
        output = replicate.run(
            "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
            input={"prompt": prompt, "max_new_tokens": 500}
        )
        return {"lyrics": "".join(output)}
    except Exception as e:
        print(f"Replicate API error: {e}")
        raise e

