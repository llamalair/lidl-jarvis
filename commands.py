from services.spotify import SpotifyService


class CommandRouter:
    def __init__(self):
        self.services = [
            SpotifyService(),
        ]

    def clean_command(self, command_text: str) -> str:
        return (
            command_text
            .lower()
            .replace("hey jarvis", "")
            .replace("jarvis", "")
            .strip()
        )

    def handle(self, command_text: str) -> None:
        command_text = self.clean_command(command_text)

        print(f"Detected command: {command_text}")

        if not command_text:
            print("No command detected.")
            return

        for service in self.services:
            if not service.can_handle(command_text):
                continue

            handled = service.handle(command_text)

            if handled:
                return

        print("Unknown command.")