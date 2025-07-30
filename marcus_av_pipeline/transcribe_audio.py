# transcribe_audio.py
import speech_recognition as sr
from pathlib import Path
from pydub import AudioSegment
import math
import os
import json

def transcribe_audio(audio_path: str, output_path: str = "output/transcripts") -> str:
    recognizer = sr.Recognizer()
    audio_file = Path(audio_path)
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Split audio into 30-second chunks
    audio = AudioSegment.from_wav(audio_file)
    chunk_length_ms = 30 * 1000  # 30 sec
    num_chunks = math.ceil(len(audio) / chunk_length_ms)

    transcript_data = []
    
    print(f"🎧 Transcribing {num_chunks} audio chunks...")

    for i in range(num_chunks):
        start_ms = i * chunk_length_ms
        end_ms = min((i + 1) * chunk_length_ms, len(audio))
        chunk = audio[start_ms:end_ms]
        chunk_path = output_dir / f"chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")

        with sr.AudioFile(str(chunk_path)) as source:
            audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio_data)
                print(f"✅ Chunk {i}: {text[:60]}...")
            except sr.UnknownValueError:
                text = "[Unintelligible]"
                print(f"⚠️ Chunk {i}: Could not understand")
            except sr.RequestError as e:
                print(f"❌ Speech Recognition error: {e}")
                break

        transcript_data.append({
            "chunk": i,
            "start_time_sec": start_ms // 1000,
            "end_time_sec": end_ms // 1000,
            "text": text
        })

    # Save as JSON transcript
    transcript_path = output_dir / (audio_file.stem + "_transcript.json")
    with open(transcript_path, "w") as f:
        json.dump(transcript_data, f, indent=2)

    print(f"📄 Transcript saved: {transcript_path}")
    return str(transcript_path)

# Example
if __name__ == "__main__":
    wav_file = "output/audio/MrRogersspeech.wav"
    transcribe_audio(wav_file)
