from vosk import Model, KaldiRecognizer

import os
print("hello")
if not os.path.exists("model-ru"):
    print ("Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model' in the current folder.")
    print ("Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model-en' in the current folder.")
    exit (1)

import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()
model = Model("model-ru")
rec = KaldiRecognizer(model, 16000)
s = {}
while True:
    data = stream.read(5000) # было 2000
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        first_res = rec.Result()
        
        if "" in first_res:
            print("first_res")
            print(first_res)
            if "компьютер" in first_res:
                print("FOUND KW")
print(rec.FinalResult())