from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from pathlib import Path
import whisper_timestamped as whisper
import torch
from hate_speech_detector import HateSpeechDetector
import nltk
from nltk.tokenize import sent_tokenize

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max
app.config['ALLOWED_AUDIO_EXTENSIONS'] = {'.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac', '.wma'}
app.config['ALLOWED_TEXT_EXTENSIONS'] = {'.txt'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Global model
model = None
detector = HateSpeechDetector()


def load_whisper_model():
    global model
    if model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("large", device=device)
    return model


def allowed_file(filename, allowed_extensions):
    return Path(filename).suffix.lower() in allowed_extensions


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze/audio', methods=['POST'])
def analyze_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename, app.config['ALLOWED_AUDIO_EXTENSIONS']):
        return jsonify({'error': 'Invalid audio format'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Load model if needed
        whisper_model = load_whisper_model()

        # Transcribe
        transcribed_text = whisper.transcribe(whisper_model, filepath)

        # Overall analysis
        full_result = detector.predict(transcribed_text['text'])

        # Segment analysis
        segments = []
        for segment in transcribed_text['segments']:
            sentences = sent_tokenize(segment['text'].strip())
            segment_duration = segment['end'] - segment['start']
            total_chars = len(segment['text'])
            current_time = segment['start']

            for sentence in sentences:
                if not sentence.strip():
                    continue

                sentence_duration = (len(sentence) / total_chars) * segment_duration
                sentence_end = current_time + sentence_duration

                result = detector.predict(sentence)

                segments.append({
                    'start': round(current_time, 2),
                    'end': round(sentence_end, 2),
                    'text': sentence,
                    'label': result['label'],
                    'confidence': round(result['confidence'], 4)
                })

                current_time = sentence_end

        return jsonify({
            'transcription': transcribed_text['text'],
            'overall': {
                'label': full_result['label'],
                'confidence': round(full_result['confidence'], 4)
            },
            'segments': segments
        })

    finally:
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)


@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    if 'file' in request.files:
        file = request.files['file']

        if file.filename == '' or not allowed_file(file.filename, app.config['ALLOWED_TEXT_EXTENSIONS']):
            return jsonify({'error': 'Invalid text file'}), 400

        text = file.read().decode('utf-8')
    elif 'text' in request.json:
        text = request.json['text']
    else:
        return jsonify({'error': 'No text provided'}), 400

    # Overall analysis
    full_result = detector.predict(text)

    # Sentence analysis
    sentences = sent_tokenize(text.strip())
    sentence_results = []

    for idx, sentence in enumerate(sentences, 1):
        if not sentence.strip():
            continue

        result = detector.predict(sentence)
        sentence_results.append({
            'index': idx,
            'text': sentence,
            'label': result['label'],
            'confidence': round(result['confidence'], 4)
        })

    return jsonify({
        'text': text,
        'overall': {
            'label': full_result['label'],
            'confidence': round(full_result['confidence'], 4)
        },
        'sentences': sentence_results
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
