import whisper
import torch

import argparse
import os
from pathlib import Path

model = None

def load_model(model_name):
    global model

    device = "cuda" if torch.cuda.is_available() else "cpu"

    if device == "cuda":
        gpu_name = torch.cuda.get_device_name(0)
        print(f"Loading model '{model_name}' on device: {device} ({gpu_name})")
    else:
        print(f"Loading model '{model_name}' on device: {device}")

    model = whisper.load_model(model_name, device=device)
    print(f"Model '{model_name}' loaded successfully")


def validate_audio_file(file_path):
    """Validate if the file exists and has a valid audio extension."""
    audio_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac', '.wma']

    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f"File not found: {file_path}")

    file_ext = Path(file_path).suffix.lower()
    if file_ext not in audio_extensions:
        raise argparse.ArgumentTypeError(f"Invalid audio format: {file_ext}")

    return file_path


def process_audio(file_path):
    """Process the audio file."""
    transcribed_text = model.transcribe(file_path)
    print("Transcription:" + transcribed_text['text'])


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for processing audio files"
    )

    parser.add_argument(
        'audio_file',
        type=validate_audio_file,
        help='Path to the audio file'
    )

    args = parser.parse_args()

    load_model("turbo")
    process_audio(args.audio_file)

if __name__ == "__main__":
    main()
