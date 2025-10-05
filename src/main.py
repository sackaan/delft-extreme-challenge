import whisper_timestamped as whisper
import torch
import argparse
import os
from pathlib import Path
from hate_speech_detector import HateSpeechDetector
import nltk
from nltk.tokenize import sent_tokenize


nltk.download('punkt')
nltk.download('punkt_tab')


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
    audio_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac', '.wma']

    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f"File not found: {file_path}")

    file_ext = Path(file_path).suffix.lower()
    if file_ext not in audio_extensions:
        raise argparse.ArgumentTypeError(f"Invalid audio format: {file_ext}")

    return file_path


def process_audio(file_path):
    transcribed_text = whisper.transcribe(model, file_path)
    detector = HateSpeechDetector()

    print("Transcription:", transcribed_text['text'])

    full_result = detector.predict(transcribed_text['text'])
    print(f"\nOverall Speech Analysis: {full_result['label'].upper()} (confidence: {full_result['confidence']:.2%})")

    print("\nWord-level timestamps with hate speech detection:")

    for segment in transcribed_text['segments']:
        # Split segment into sentences
        sentences = sent_tokenize(segment['text'].strip())

        # Calculate approximate timing for each sentence
        segment_duration = segment['end'] - segment['start']
        total_chars = len(segment['text'])

        current_time = segment['start']

        for sentence in sentences:
            if not sentence.strip():
                continue

            # Estimate sentence duration based on character count
            sentence_duration = (len(sentence) / total_chars) * segment_duration
            sentence_end = current_time + sentence_duration

            # Predict hate speech for this sentence
            result = detector.predict(sentence)

            print(f"\n[{current_time:.2f}s - {sentence_end:.2f}s]")
            print(f"Text: {sentence}")
            print(f"Classification: {result['label']} ({result['confidence']:.2%})")

            current_time = sentence_end


def process_text_file(file_path):
    detector = HateSpeechDetector()

    with open(file_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    print("Text:", full_text)

    full_result = detector.predict(full_text)
    print(f"\nOverall Text Analysis: {full_result['label'].upper()} (confidence: {full_result['confidence']:.2%})")

    print("\nSentence-level detection:")

    # Split into sentences
    sentences = sent_tokenize(full_text.strip())

    for idx, sentence in enumerate(sentences, 1):
        if not sentence.strip():
            continue

        result = detector.predict(sentence)

        print(f"\n[Sentence {idx}]")
        print(f"Text: {sentence}")
        print(f"Classification: {result['label']} ({result['confidence']:.2%})")


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for processing audio files"
    )

    parser.add_argument(
        'audio_file',
        nargs='?',
        type=validate_audio_file,
        help='Path to the audio file'
    )

    parser.add_argument(
        '-t', '--text-file',
        type=str,
        help='Path to a text file to analyze directly (skips audio transcription)'
    )

    args = parser.parse_args()

    if args.text_file:
        if not os.path.exists(args.text_file):
            print(f"Error: Text file not found: {args.text_file}")
            return
        process_text_file(args.text_file)
    elif args.audio_file:
        load_model("turbo")
        process_audio(args.audio_file)
    else:
        parser.error("Either provide an audio file or use -t/--text-file option")

if __name__ == "__main__":
    main()
