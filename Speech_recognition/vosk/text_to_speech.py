import pyttsx3

def speak(phrase):
    engine = pyttsx3.init()
    rate = 110
    engine.setProperty('rate', rate) 
