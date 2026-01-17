from youtube_transcript_api import YouTubeTranscriptApi

def load_transcript(video_id: str) -> str:
    yt_api = YouTubeTranscriptApi()   # ✅ instantiate
    transcript = yt_api.fetch(video_id)

    # Each item is an object, not dict
    text = " ".join([t.text for t in transcript])
    return text
