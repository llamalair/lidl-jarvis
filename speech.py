import json
import subprocess

from vosk import KaldiRecognizer, Model as VoskModel, SetLogLevel

from config import SAMPLE_RATE, VOSK_MODEL_PATH


SetLogLevel(-1)


class Speaker:
    def speak(self, text: str) -> None:
        subprocess.Popen(
            ["espeak-ng", text],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


class VoskCommandRecognizer:
    def __init__(self):
        print("Loading Vosk model...")
        self.model = VoskModel(VOSK_MODEL_PATH)

        self.grammar = json.dumps([
            "play spotify",
            "open spotify",
            "start spotify",
            "resume spotify",

            "pause spotify",
            "stop spotify",

            "next song",
            "next track",
            "skip song",

            "previous song",
            "previous track",
            "go back",

            "play",
            "pause",
            "stop",
            "next",
            "skip",
            "previous",
            "back",

            "play spotty",
            "play spotty fight",
            "open spotty",
            "open spotty fight",

            "[unk]",
        ])

    def transcribe(self, audio_bytes: bytes) -> str:
        recognizer = KaldiRecognizer(self.model, SAMPLE_RATE, self.grammar)
        recognizer.AcceptWaveform(audio_bytes)

        result = json.loads(recognizer.FinalResult())
        return result.get("text", "").lower().strip()