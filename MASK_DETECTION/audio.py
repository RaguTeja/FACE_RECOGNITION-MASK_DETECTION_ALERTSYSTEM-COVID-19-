import pyttsx3

engine=pyttsx3.init()                       # INITIALIZE THE ENGINE
voices=engine.getProperty('voices')         # GET THE VOICE
engine.setProperty('voice',voices[0].id)    # SET THE VOICE YOU WANT
engine.setProperty('rate',150)              # VOICE RATE

def speak(str):
    engine.say(str)                         # TEXT TO SPEECH
    engine.runAndWait()

# speak('HII, This is raghu')