from pathlib import Path

import sounddevice as sd
from audio_system import EchoCancellationManager

from audio import AudioQueue
from commands import CommandRouter
from config import (
    SAMPLE_RATE,
    CHANNELS,
    DTYPE,
    WAKE_CHUNK_SIZE,
    VOSK_MODEL_PATH,
    COMMAND_SECONDS,
)
from speech import Speaker, VoskCommandRecognizer
from wake import WakeWordDetector


class JarvisAssistant:
    def __init__(self):
        self.echo_manager = EchoCancellationManager()
        self.echo_manager.setup()

        if not Path(VOSK_MODEL_PATH).exists():
            raise FileNotFoundError(
                f"Vosk model folder not found: {VOSK_MODEL_PATH}"
            )

        self.audio = AudioQueue()
        self.speaker = Speaker()
        self.wake_detector = WakeWordDetector(wake_word_name="hey_jarvis")
        self.command_recognizer = VoskCommandRecognizer()
        self.command_router = CommandRouter()

    def run(self) -> None:
        print("\nAssistant running.")
        print('Wake word: "Hey Jarvis"')
        print("Commands:")
        print('  "play Spotify"')
        print('  "pause"')
        print('  "next song"')
        print('  "previous song"')
        print("Press Ctrl+C to stop.\n")

        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=WAKE_CHUNK_SIZE,
            dtype=DTYPE,
            channels=CHANNELS,
            callback=self.audio.callback,
        ):
            while True:
                data = self.audio.get()

                if not self.wake_detector.detect(data):
                    continue

                self.speaker.speak("Yes?")

                self.audio.clear()

                command_audio = self.audio.record_seconds(
                    COMMAND_SECONDS,
                    SAMPLE_RATE,
                    WAKE_CHUNK_SIZE,
                )

                command_text = self.command_recognizer.transcribe(command_audio)

                self.command_router.handle(command_text)

                self.audio.clear()
                self.wake_detector.reset()
                self.wake_detector.start_cooldown()

                print("\nBack to wake-word mode...\n")


if __name__ == "__main__":
    assistant = JarvisAssistant()
    assistant.run()