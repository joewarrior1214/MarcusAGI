import json
from pathlib import Path
from textblob import TextBlob
import re

TEACHING_KEYWORDS = [
    "you are special",
    "I like you just the way you are",
    "it's okay to feel",
    "when I was a boy",
    "make believe",
    "helping others",
    "being kind",
    "feelings",
    "being a good friend",
    "love",
    "safe",
    "talk about your feelings"
]

def detect_emotion(text: str) -> str:
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.4:
        return "joy"
    elif polarity < -0.2:
        return "sadness"
    elif 0.1 < polarity <= 0.4:
        return "calm"
    elif -0.2 <= polarity <= 0.1:
        return "neutral"
    else:
        return "conflicted"

def detect_teaching_moment(text: str) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in TEACHING_KEYWORDS)

def annotate_transcript(transcript_path: str, output_path: str):
    with open(transcript_path, "r") as f:
        chunks = json.load(f)

    for chunk in chunks:
        text = chunk["text"]
        chunk["emotion"] = detect_emotion(text)
        chunk["teaching_moment"] = detect_teaching_moment(text)

    with open(output_path, "w") as f:
        json.dump(chunks, f, indent=2)
    print(f"✅ Annotated transcript saved: {output_path}")

# Example usage
if __name__ == "__main__":
    transcript_file = "output/transcripts/MrRogersspeech_transcript.json"
    annotated_file = "output/analysis/MrRogersspeech_annotated.json"
    Path("output/analysis").mkdir(parents=True, exist_ok=True)
    annotate_transcript(transcript_file, annotated_file)
