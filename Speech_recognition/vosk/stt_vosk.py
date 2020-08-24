from vosk import Model, KaldiRecognizer
import parser
import psutil
import os
import time
import random
import subprocess
import datetime
print("hello")
if not os.path.exists("model-ru"):
    print ("Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model' in the current folder.")
    print ("Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model-ru' in the current folder.")
    exit (1)

import pyaudio
import pyttsx3

def turn_on_light():
    sub = subprocess.Popen(["./light_tuya_1.sh true"], shell=True)
    time.sleep(1)
    sub.kill()
    
def turn_off_light():
    sub = subprocess.Popen(["./light_tuya_1.sh false"], shell=True)
    time.sleep(1)
    sub.kill()
    
def params_checking():
    cpu = psutil.cpu_percent()
    ozu = psutil.virtual_memory().percent
    print(f'CPU = {cpu}%, OZU = {ozu}%')
    if ozu > 50.0: #70.0:
        engine.say("I have problem with memory")
        engine.runAndWait()
        print('OZU problem')
        return False
    if cpu > 50.0:
        engine.say("I have problem with processor")
        engine.runAndWait()
        print('CPU problem')
        return False
    return True

def activate_vosk():
    if params_checking() is False:
        quit()
    #model = Model("model-ru")
    #rec = KaldiRecognizer(model, 48000) # 16000
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=48000,
                    input=True,
                    frames_per_buffer=30000) # 30000
    stream.start_stream()
    
    return stream, p#, rec, p, model

#
engine = pyttsx3.init()
rate = 110
engine.setProperty('rate', rate)
hello_list = ['I am listening','Yes','I am here']
#


while True:
    kws = False
    time_start = int(time.time())
    checking_time = time_start
    s = {}
    #
    cycle_trigger = True
    stream, p = activate_vosk()
    time.sleep(3)
    data = stream.read(1024,exception_on_overflow = False)
    
    
    stream.close()
    p.terminate()
    print(stream)
    rec = None
    data = None
    model = None
    stream = None
    time.sleep(5)
    # KaldiRecognizer.CleanUp()
print(rec.FinalResult())