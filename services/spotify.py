import subprocess
import time

from config import SPOTIFY_COMMAND


class SpotifyService:
    name = "spotify"

    patterns = [
        "spotify",
        "spotty",
        "play",
        "pause",
        "stop",
        "next",
        "skip",
        "previous",
        "back",
        "open",
        "start",
        "resume",
    ]

    def can_handle(self, command_text: str) -> bool:
        return any(pattern in command_text for pattern in self.patterns)

    def handle(self, command_text: str) -> bool:
        if "play" in command_text and self._mentions_spotify_or_play_only(command_text):
            self.play()
            return True

        if "open" in command_text and self._mentions_spotify(command_text):
            self.play()
            return True

        if "start" in command_text and self._mentions_spotify(command_text):
            self.play()
            return True

        if "resume" in command_text and self._mentions_spotify(command_text):
            self.play()
            return True

        if "pause" in command_text or "stop" in command_text:
            self.pause()
            return True

        if "next" in command_text or "skip" in command_text:
            self.next()
            return True

        if "previous" in command_text or "back" in command_text:
            self.previous()
            return True

        return False

    def _mentions_spotify(self, command_text: str) -> bool:
        return "spotify" in command_text or "spotty" in command_text

    def _mentions_spotify_or_play_only(self, command_text: str) -> bool:
        return self._mentions_spotify(command_text) or command_text == "play"

    def open_spotify(self) -> None:
        try:
            subprocess.Popen(
                SPOTIFY_COMMAND,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("Action: Opening Spotify")
            time.sleep(4)
        except FileNotFoundError:
            print("Error: Spotify command not found. Check SPOTIFY_COMMAND.")

    def play(self) -> None:
        self.open_spotify()
        subprocess.run(["playerctl", "-p", "spotify", "play"], check=False)
        print("Action: Spotify play")

    def pause(self) -> None:
        subprocess.run(["playerctl", "-p", "spotify", "pause"], check=False)
        print("Action: Spotify pause")

    def next(self) -> None:
        subprocess.run(["playerctl", "-p", "spotify", "next"], check=False)
        print("Action: Spotify next")

    def previous(self) -> None:
        subprocess.run(["playerctl", "-p", "spotify", "previous"], check=False)
        print("Action: Spotify previous")