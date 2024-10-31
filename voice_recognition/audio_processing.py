# voice_recognition/audio_processing.py
from google.cloud import speech_v1 as speech
import io
import subprocess
import wave

def get_audio_properties(file_path):
    """Get audio properties like sample rate, channels, and format."""
    with wave.open(file_path, 'rb') as wf:
        sample_rate = wf.getframerate()
        num_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        return sample_rate, num_channels, sample_width

def convert_audio(input_path, output_path, sample_rate=16000):
    """Convert audio file to mono with specified sample rate using ffmpeg."""
    command = [
        'ffmpeg', '-i', input_path,
        '-ar', str(sample_rate), '-ac', '1',  # Convert to mono
        output_path
    ]
    subprocess.run(command, check=True)

def transcribe_audio(file_path, json_key_path):
    """Transcribe audio using Google Cloud Speech-to-Text API."""
    client = speech.SpeechClient.from_service_account_json(json_key_path)

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )

    try:
        response = client.recognize(config=config, audio=audio)
        return [result.alternatives[0].transcript for result in response.results]
    except Exception as e:
        raise RuntimeError(f"Error during transcription: {e}")
