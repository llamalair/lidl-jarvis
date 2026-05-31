import queue


class AudioQueue:
    def __init__(self):
        self._queue = queue.Queue()

    def callback(self, indata, frames, time_info, status):
        if status:
            print(status)

        self._queue.put(bytes(indata))

    def get(self):
        return self._queue.get()

    def clear(self):
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

    def record_seconds(self, seconds: int, sample_rate: int, chunk_size: int) -> bytes:
        print(f"Listening for command for {seconds} seconds...")

        frames = []
        total_chunks = int((sample_rate * seconds) / chunk_size)

        for _ in range(total_chunks):
            frames.append(self.get())

        return b"".join(frames)