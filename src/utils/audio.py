import os
from pydub import AudioSegment

def convert_ogg_to_mp3(ogg_path, mp3_path):
    try:
        audio = AudioSegment.from_ogg(ogg_path)
        audio.export(mp3_path, format="mp3")
        return True
    except Exception as e:
        print(f"Audio Conversion Error: {e}")
        return False
