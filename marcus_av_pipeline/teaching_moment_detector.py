import json
from pathlib import Path

KEYWORDS = [
    "love", "kindness", "feelings", "empathy", "help", "respect",
    "neighbor", "forgive", "yourself", "understand", "special"
]

def is_teaching_moment(text: str) -> bool:
    """Detects whether a chunk contains a moral/educational teaching."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in KEYWORDS)

def annotate_teaching_moments(transcript_path: str) -> str:
    """Annotate a transcript file with teaching moment flags."""
    input_path = Path(transcript_path)
    with input_path.open("r") as f:
        data = json.load(f)

    for chunk in data:
        chunk["teaching_moment"] = is_teaching_moment(chunk["text"])

    output_path = input_path.parent / (input_path.stem + "_labeled.json")
    with output_path.open("w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Teaching moments annotated: {output_path}")
    return str(output_path)

# Example usage
if __name__ == "__main__":
    transcript_file = "output/transcripts/MrRogersspeech_transcript.json"
    annotate_teaching_moments(transcript_file)
