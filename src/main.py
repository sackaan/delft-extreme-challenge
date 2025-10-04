import whisper
import torch

import argparse
import os
from pathlib import Path

model = None

def load_model(model_name):
    global model

    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model(model_name, device=device)
    print(f"Model loaded on {device}")


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
    print(f"Processing audio file: {file_path}")
    # Add your audio processing logic here
    transcribed_text = model.transcribe(file_path)
    print("Transcription:")
    print(transcribed_text['text'])
    file_size = os.path.getsize(file_path)
    print(f"File size: {file_size / 1024:.2f} KB")


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for processing audio files"
    )

    parser.add_argument(
        'audio_file',
        type=validate_audio_file,
        help='Path to the audio file'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    if args.verbose:
        print(f"Verbose mode enabled")
    load_model("turbo")
    process_audio(args.audio_file)
    print("Processing complete!")


if __name__ == "__main__":
    main()
