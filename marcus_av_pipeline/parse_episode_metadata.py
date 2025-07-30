import ffmpeg
import json
import os
from pathlib import Path
from datetime import datetime
import imageio_ffmpeg

# Ensure ffprobe is discoverable
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
ffprobe_path = ffmpeg_path.replace("ffmpeg", "ffprobe")
os.environ["PATH"] = str(Path(ffmpeg_path).parent) + os.pathsep + os.environ["PATH"]

def parse_episode_metadata(video_path: str, title: str = "Untitled") -> dict:
    input_path = Path(video_path)
    episode_id = input_path.stem

    try:
        # Probe the file using ffmpeg to get metadata
        probe = ffmpeg.probe(str(input_path))
        format_info = probe.get("format", {})
        duration = float(format_info.get("duration", 0))
        tags = format_info.get("tags", {})

        # Try to get creation time from tags
        creation_time = tags.get("creation_time", None)
        if creation_time:
            creation_time = creation_time.strip()
        else:
            creation_time = datetime.now().isoformat()

        metadata = {
            "episode_id": episode_id,
            "title": title,
            "duration_seconds": int(duration),
            "creation_date": creation_time,
            "file_path": str(input_path)
        }

        # Save to metadata file
        output_dir = Path("output/metadata")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{episode_id}_metadata.json"
        with open(output_file, "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"✅ Episode metadata saved: {output_file}")
        return metadata

    except ffmpeg.Error as e:
        print(f"❌ ffmpeg error: {e.stderr.decode()}")
        return {}

# Example usage
if __name__ == "__main__":
    test_video = "marcus_av_pipeline/sample_data/MrRogersspeech.mp4"
    parse_episode_metadata(test_video, title="Mr. Rogers on Loving Yourself")
