from vosk import Model, KaldiRecognizer

import os
import time
print("hello")
if not os.path.exists("model-ru"):
    print ("Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model' in the current folder.")
    print ("Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model-ru' in the current folder.")
    exit (1)

import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=30000)
stream.start_stream()
model = Model("model-ru")
print('############################################')
print(p.get_device_info_by_index(0)['defaultSampleRate'])
rec = KaldiRecognizer(model, 16000) # 16000
# time.sleep(3)
s = {}
while True:
    data = stream.read(30000,exception_on_overflow = False) # было 2000
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        first_res = rec.Result()
        if len(first_res) > 1:
            print(int(time.time()))
            print(first_res)
            if "компьютер" in first_res:
                print("FOUND KW")
print(rec.FinalResult())
