import sounddevice as sd 
import numpy as np 
import scipy.io.wavfile as wav 

from groq import Groq 
from config import GROQ_API_KEY, INPUT_MODE

client = Groq(api_key=GROQ_API_KEY)

def record_audio(seconds: int = 6, rate: int = 44100) -> str:


    recording = sd.rect(int(seconds * rate), samplerate=rate, channels=1, dtype=np.int16)
    sd.wait()

    print("Done recording!")

    wav.write("input.wav", rate, recording )

    with open("input.wav", "rb" ) as f:
        result = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=f
        )

    return result.text


def text_input() -> str:
    return input("You: ")

def get_user_input() -> str:
    if INPUT_MODE == "text":
        return text_input()
    return record_audio()