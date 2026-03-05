import serial
import threading
import time
from collections import deque


class SerialStream:

    def __init__(self, port, baudrate=9600, timeout=0.5, buffer_size=100):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

        self.buffer = deque(maxlen=buffer_size)
        self.latest = None

        self.running = True
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()


    def update(self):
        while self.running:

            line = self.ser.readline()
            if not line:
                continue

            self.latest = line.decode('utf-8', errors='ignore').strip()
            self.buffer.append({time.time_ns(): self.latest})


    def write(self, message):
        self.ser.write(f'[PY] {message}\n'.encode('ascii'))

    def read(self, n_latest=None):
        if n_latest is None:
            return self.latest

        n_latest = min(n_latest, len(self.buffer))
        return list(self.buffer)[-n_latest:]

    def stop(self):
        self.running = False
        self.thread.join()
        self.ser.close()


if __name__ == "__main__":

    ser = SerialStream(port='/dev/ttyUSB0', baudrate=9600, timeout=0.5, buffer_size=100)

    try:
        while True:
            latest = ser.read()
            print(f"Latest: {latest}")

            latest_5 = ser.read(n_latest=5)
            print(f"Latest 5: {latest_5}")
            
            ser.write("Hello from Python!")

            time.sleep(1)
            
    finally:
        ser.stop()