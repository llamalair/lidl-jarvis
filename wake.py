import time

import numpy as np
from openwakeword.model import Model

from config import WAKE_THRESHOLD, WAKE_COOLDOWN_SECONDS


class WakeWordDetector:
    def __init__(self, wake_word_name: str = "hey_jarvis"):
        self.wake_word_name = wake_word_name
        self.last_wake_time = 0.0

        print("Loading openWakeWord model...")
        self.model = Model()

    def detect(self, audio_bytes: bytes) -> bool:
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
        prediction = self.model.predict(audio_array)
        now = time.time()

        for wakeword_name, score in prediction.items():
            if wakeword_name != self.wake_word_name:
                continue

            if score < WAKE_THRESHOLD:
                continue

            if now - self.last_wake_time < WAKE_COOLDOWN_SECONDS:
                continue

            print(f"\nDetected wake word: hey jarvis | score={score:.2f}")
            return True

        return False

    def reset(self) -> None:
        self.model = Model()

    def start_cooldown(self) -> None:
        self.last_wake_time = time.time()