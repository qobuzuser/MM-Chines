import os
import google.generativeai as genai

# API Key ထည့်ပေးတယ်
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Safety settings ကို လျှော့ပြီး အမှားမထွက်အောင် လုပ်ထားတယ်
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    safety_settings=[
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    ]
)

def safe_generate(prompt: str) -> str:
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1000,
            }
        )
        # အဖြေ မရှိရင် ဒါမှမဟုတ် ပိတ်ထားရင် ဒီလို ပြန်ပေးမယ်
        if not response.candidates or len(response.candidates[0].content.parts) == 0:
            return "ယာယီ အဖြေ မထုတ်နိုင်ပါ။ စကားလုံးကို နည်းနည်း ပြန်ရေးကြည့်ပါနော် 😊"
        return response.text.strip()
    except Exception as e:
        return "ယာယီ ချို့ယွင်းနေပါသည်။ ခဏနေပြီး ထပ်ကြိုးစားပါ။"

# သာမန် ဘာသာပြန် + အသံထွက် + ဥပမာ
def get_translation(text: str) -> str:
    prompt = f"""
    အောက်ပါ စာသားကို တရုတ် ↔ မြန်မာ အပြန်အလှန် ဘာသာပြန်ပေးပါ။
    ဘာသာစကား အလိုအလျောက် သိပြီး ဆန့်ကျင်ဘက် ဘာသာနဲ့ ဖြေပါ။
    အောက်ပါ format အတိုင်း လှပစွာ ရေးပါ:

    🇨🇳 Translation: ...
    🔊 Pronunciation: ... (Pinyin သို့မဟုတ် မြန်မာ အသံထွက်)
    📖 Meaning: ...
    💡 Example: ...

    စာသား: "{text}"
    """
    return safe_generate(prompt)

# More Explanation ခလုတ်အတွက်
def get_explanation(text: str) -> str:
    prompt = f"""
    အောက်ပါ စကားလုံး/စကားစုကို အသေးစိတ် ရှင်းပြပါ။
    တရုတ်ဆိုရင် မြန်မာလို၊ မြန်မာဆိုရင် တရုတ်လို ဖြေပါ။

    ထည့်ပေးရမယ့်အချက်များ:
    • အဓိပ္ပာယ် အသေးစိတ်
    • အသံထွက် (Pinyin သို့မဟုတ် မြန်မာ အသံထွက်)
    • သဒ္ဒါပိုင်း
    • တကယ့်ဘဝမှာ သုံးပုံ ၂-၃ ခု
    • ဆင်တူစကားလုံး ၃-၅ ခု

    စာသား: "{text}"
    """
    return safe_generate(prompt)
