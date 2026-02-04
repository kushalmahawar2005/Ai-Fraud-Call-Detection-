import os
import whisper
import warnings
import librosa
import numpy as np

# Suppress warnings to keep the output clean
warnings.filterwarnings("ignore")

class Transcriber:
    def __init__(self, model_size="base"):
        """
        Initialize the Whisper model.
        Options for model_size: 'tiny', 'base', 'small', 'medium', 'large'
        'base' is a good trade-off for speed vs accuracy for a hackathon.
        """
        print(f"Loading Whisper model: {model_size}...")
        try:
            self.model = whisper.load_model(model_size)
            print("Whisper model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def transcribe(self, audio_path):
        """
        Transcribes the audio file using librosa for loading to avoid FFmpeg dependency.
        Returns the transcribed text string.
        """
        if self.model is None:
            return "Error: Model not loaded."

        # Check if file exists
        if not os.path.exists(audio_path):
            return f"Error: File not found at {audio_path}"

        try:
            # 1. Load and resample audio using librosa
            # This uses soundfile/audioread internally and returns a numpy array
            # We enforce 16kHz mono (required by Whisper)
            audio_array, _ = librosa.load(audio_path, sr=16000, mono=True)

            # 2. Pass the numpy array directly to Whisper
            # Passing the array bypasses Whisper's internal 'ffmpeg -i' command usage
            # fp16=False is recommended for CPU usage
            result = self.model.transcribe(audio_array, fp16=False)
            return result["text"]
            
        except Exception as e:
            return f"Error during transcription: {str(e)}"
