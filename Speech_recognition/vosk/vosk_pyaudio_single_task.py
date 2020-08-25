from vosk import Model, KaldiRecognizer
import psutil
import os
import time
import random
import subprocess
import datetime
if not os.path.exists("model-ru"):
    print ("Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model' in the current folder.")
    print ("Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model-ru' in the current folder.")
    exit (1)

import pyaudio
import pyttsx3
from multiprocessing import Process

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
    if ozu > 70.0:
        engine.say("I have problem with memory")
        engine.runAndWait()
        print('OZU problem')
    if cpu > 50.0:
        engine.say("I have problem with processor")
        engine.runAndWait()
        print('CPU problem')

def vosk_main():
    engine = pyttsx3.init()
    rate = 110
    engine.setProperty('rate', rate) 
    hello_list = ['I am listening','Yes','I am here']
    model = Model("model-ru")
    rec = KaldiRecognizer(model, 48000) # 16000
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=48000,
                    input=True,
                    frames_per_buffer=30000) # 30000
    stream.start_stream()
    kws = False
    time_start = int(time.time())
    checking_time = time_start
    s = {}
    while True:
        if int(time.time()) > checking_time + 5:
            params_checking()
            checking_time = int(time.time())
        data = stream.read(5000,exception_on_overflow = False) # было 5000
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            first_res = rec.Result()
            if len(first_res) > 17:
                print(datetime.datetime.now().strftime("%H:%M:%S"))
                params_checking()
                print(first_res)
                if "компьютер" in first_res:
                    print("FOUND KW")
                    time_start = int(time.time())
                    kws = True
                time_now = int(time.time())
                if kws == True and time_now - time_start < 10:
                    if "свет" in first_res:
                        if "включ" in first_res:
                            turn_on_light()
                            engine.say("Turning on the light")
                            engine.runAndWait()
                            kws = False
                        elif "выключ" in first_res:
                            turn_off_light()
                            engine.say("Turning off the light")
                            engine.runAndWait()
                            kws = False
                    elif "увеличить скорость речи" in first_res:
                        engine.say("Speed up")
                        engine.runAndWait()
                    elif "уменьшить скорость речи" in first_res:
                        engine.say("Speed down")
                        engine.runAndWait()
                    elif "врем" in first_res:
                        now_time = datetime.datetime.now() + datetime.timedelta(hours=2)
                        engine.say(f"the time is {now_time.strftime('%H %M')}")
                        engine.runAndWait()
                    else:
                        engine.say(random.choice(hello_list))
                        engine.runAndWait()
                        time_start = int(time.time())
                if time_now - time_start > 15:
                    kws = False
    print(rec.FinalResult())


if __name__ == '__main__':
    vosk = Process(target = vosk_main)
    vosk.start()
    while True:
        cpu = psutil.cpu_percent()
        ozu = psutil.virtual_memory().percent
        if ozu > 80.5: #70.0:
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")}')
            print('OZU problem')
            vosk.terminate()
            time.sleep(1)
            vosk = Process(target = vosk_main)
            vosk.start()
            # print(f'CPU = {cpu}%, OZU = {ozu}%')
        if cpu > 50.0:
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")}')
            print('CPU problem')
        time.sleep(1)

