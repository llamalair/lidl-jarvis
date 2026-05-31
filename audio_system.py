import subprocess


class EchoCancellationManager:
    SOURCE_NAME = "echoCancel_source"
    SINK_NAME = "echoCancel_sink"

    def __init__(self):
        self.loaded_module_id = None
        self.previous_source = None
        self.previous_sink = None

    def setup(self) -> None:
        """
        Turn echo cancellation on for this app session.
        Also remember the user's previous default mic/speaker.
        """
        if not self._command_exists("pactl"):
            print("Warning: pactl not found. Echo cancellation not enabled.")
            return

        self.previous_source = self._get_default_source()
        self.previous_sink = self._get_default_sink()

        if not self.is_loaded():
            self.load_module()
        else:
            print("Echo cancellation already loaded.")

        self.set_echo_defaults()

    def cleanup(self) -> None:
        """
        Restore previous defaults when Jarvis exits.
        Unload echo cancellation only if this app loaded it.
        """
        print("Restoring previous audio defaults...")

        if self.previous_source:
            subprocess.run(
                ["pactl", "set-default-source", self.previous_source],
                check=False,
            )

        if self.previous_sink:
            subprocess.run(
                ["pactl", "set-default-sink", self.previous_sink],
                check=False,
            )

        if self.loaded_module_id:
            print("Unloading echo cancellation...")
            subprocess.run(
                ["pactl", "unload-module", self.loaded_module_id],
                check=False,
            )

    def is_loaded(self) -> bool:
        sources = self._run(["pactl", "list", "short", "sources"])
        sinks = self._run(["pactl", "list", "short", "sinks"])

        return self.SOURCE_NAME in sources and self.SINK_NAME in sinks

    def load_module(self) -> None:
        print("Loading echo cancellation...")

        command = [
            "pactl",
            "load-module",
            "module-echo-cancel",
            f"source_name={self.SOURCE_NAME}",
            f"sink_name={self.SINK_NAME}",
            "aec_method=webrtc",
            "source_properties=device.description=Echo Cancel Microphone",
            "sink_properties=device.description=Echo Cancel Speakers",
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            print("Warning: Could not load echo cancellation.")
            print(result.stderr.strip())
            return

        module_id = result.stdout.strip()

        if module_id:
            self.loaded_module_id = module_id
            print(f"Echo cancellation loaded. Module ID: {module_id}")

    def set_echo_defaults(self) -> None:
        print("Using echo-cancelled mic/speaker for Jarvis session...")

        subprocess.run(
            ["pactl", "set-default-source", self.SOURCE_NAME],
            check=False,
        )

        subprocess.run(
            ["pactl", "set-default-sink", self.SINK_NAME],
            check=False,
        )

    def _get_default_source(self) -> str | None:
        output = self._run(["pactl", "info"])

        for line in output.splitlines():
            if line.startswith("Default Source:"):
                return line.split(":", 1)[1].strip()

        return None

    def _get_default_sink(self) -> str | None:
        output = self._run(["pactl", "info"])

        for line in output.splitlines():
            if line.startswith("Default Sink:"):
                return line.split(":", 1)[1].strip()

        return None

    def _run(self, command: list[str]) -> str:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout

    def _command_exists(self, command: str) -> bool:
        result = subprocess.run(
            ["which", command],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0