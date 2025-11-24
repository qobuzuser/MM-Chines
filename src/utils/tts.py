# src/utils/tts.py
import os
import tempfile
from gtts import gTTS
import uuid

def text_to_speech(text: str, lang: str = "zh-CN") -> str:
    """
    စာသားကို အသံဖိုင်အဖြစ် ပြောင်းပြီး ယာယီလမ်းကြောင်းပြန်ပေးတယ်
    lang: "zh-CN" (Chinese), "my" (Myanmar - limited support), "en" (for pronunciation)
    """
    # မြန်မာစာကို gTTS က မကောင်းလို့ → အသံထွက်ကို English letters နဲ့ ပြောခိုင်းမယ်
    if lang == "my":
        lang = "en"  # မြန်မာစာကို English စာလုံးနဲ့ ဖတ်ခိုင်းမယ်

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts = gTTS(text=text, lang=lang, slow=False)
            fp_path = fp.name
            tts.save(fp_path)
            return fp_path
    except Exception as e:
        print(f"gTTS Error: {e}")
        return None

def cleanup_file(path: str):
    """အသံဖိုင်ကို ချက်ချင်း ဖျက်ပစ်မယ်"""
    try:
        if path and os.path.exists(path):
            os.unlink(path)
    except:
        pass
