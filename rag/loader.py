from youtube_transcript_api import YouTubeTranscriptApi

def load_transcript(video_id: str) -> str:
    yt_api = YouTubeTranscriptApi()
    transcript = yt_api.fetch(video_id)

    # FIX: use dot notation
    text = " ".join([t.text for t in transcript])

    return text
