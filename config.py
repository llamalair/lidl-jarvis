SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "int16"

WAKE_CHUNK_SIZE = 1280
VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"

COMMAND_SECONDS = 3

WAKE_THRESHOLD = 0.30
WAKE_COOLDOWN_SECONDS = 3.0

SPOTIFY_COMMAND = ["spotify"]

# If Spotify is Flatpak:
# SPOTIFY_COMMAND = ["flatpak", "run", "com.spotify.Client"]