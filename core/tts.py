
import pyttsx3

_engine = pyttsx3.init()


def speak(text: str) -> None:
    print(f"Assistant: {text}")
    _engine.say(text)
    _engine.runAndWait()



from gtts import gTTS 
import os 

def speak_gtts(text: str) -> None :

    print(f"AI: {text}")
    tts = gTTS( text=text, lang="en" )

    tts.save( "output.mp3" )

    # Linux
    os.system( "mpg321 -q output.mp3"  )
