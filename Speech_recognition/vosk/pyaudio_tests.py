import psutil
import os
import time
import random
import subprocess
import datetime

def activate_vosk():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=48000,
                    input=True,
                    frames_per_buffer=30000) # 30000
    stream.start_stream()
    return stream

stream = activate_pyaudio()
while True:
    data = stream.read(1024,exception_on_overflow = False)
    time.sleep(5)
