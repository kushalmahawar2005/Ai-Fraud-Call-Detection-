import os
import shutil
import whisper
import warnings

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
        Transcribes the audio file at audio_path.
        Returns the transcribed text string.
        """
        if self.model is None:
            return "Error: Model not loaded."

        # 0. Add local bin to PATH (for portable FFmpeg)
        import os
        bin_path = os.path.join(os.getcwd(), "bin")
        if os.path.exists(bin_path):
            os.environ["PATH"] += os.pathsep + bin_path

        # 1. Check if FFmpeg is installed
        if not shutil.which("ffmpeg"):
            return (
                "Error: FFmpeg is not installed or not in PATH.\n\n"
                "Please download FFmpeg from https://ffmpeg.org/download.html, "
                "extract it, and add the 'bin' folder to your System PATH."
            )

        # 2. Check if file exists
        if not os.path.exists(audio_path):
            return f"Error: File not found at {audio_path}"

        try:
            # Make path absolute to avoid WinError 2
            abs_path = os.path.abspath(audio_path)

            # The transcribe function automatically detects language (English/Hindi)
            # fp16=False is recommended for CPU usage to avoid warnings
            result = self.model.transcribe(abs_path, fp16=False)
            return result["text"]
        except Exception as e:
            return f"Error during transcription: {str(e)}"
