# ingest_transcript_to_memory.py
import sys
from pathlib import Path

# Add root project directory to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
from pathlib import Path
from memory_system import MarcusMemorySystem, Concept

def ingest_labeled_transcript(transcript_path: str, episode_title: str):
    memory = MarcusMemorySystem()
    path = Path(transcript_path)

    if not path.exists():
        print(f"❌ File not found: {transcript_path}")
        return

    with open(path, 'r') as f:
        data = json.load(f)

    count = 0
    for chunk in data:
        if chunk.get("teaching_moment") is True:
            concept = Concept(
                id=f"{episode_title}_chunk{chunk['chunk']}",
                content=chunk["text"],
                subject="emotional_learning",
                grade_level="kindergarten",
                emotional_context=chunk.get("emotion", "neutral")
            )
            success = memory.learn_concept(concept)
            if success:
                count += 1

    print(f"✅ {count} teaching moments imported into Marcus's memory.")

# Example usage
if __name__ == "__main__":
    labeled_file = "output/transcripts/MrRogersspeech_transcript_labeled.json"
    ingest_labeled_transcript(labeled_file, episode_title="MrRogersspeech")
