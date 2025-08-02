import os
from pathlib import Path
import imageio_ffmpeg
import ffmpeg

# Get full path to ffmpeg binary
ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

def extract_audio(video_path: str, output_dir: str = "output/audio") -> str:
    input_path = Path(video_path)
    output_path = Path(output_dir) / (input_path.stem + ".wav")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        (
            ffmpeg
            .input(str(input_path))
            .output(str(output_path), acodec="pcm_s16le", ac=1, ar="16000", vn=None)
            .run(cmd=ffmpeg_bin, overwrite_output=True)
        )
        print(f"✅ Audio extracted: {output_path}")
        return str(output_path)
    except ffmpeg.Error as e:
        print(f"❌ ffmpeg-python error: {e.stderr.decode()}")
        return ""

# Example
if __name__ == "__main__":
    test_video = "marcus_av_pipeline/sample_data/mrrogersep1521conflict.mp4"
    extract_audio(test_video)
