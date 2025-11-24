import os
import google.generativeai as genai

# API Key ထည့်တယ်
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# မြန်မာကနေ အခမဲ့ အလုပ်ဖြစ်တဲ့ တစ်ခုတည်းသော model (2025 အခုထိ)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

def safe_generate(prompt: str) -> str:
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1000
            )
        )
        # အဖြေ မရှိရင် လှပစွာ ပြန်ပေးမယ်
        if not response.text or not response.text.strip():
            return "အခုချိန်လေးမှာ နည်းနည်းရှုပ်နေတယ် 😅\nနောက်တစ်ခါ ထပ်မေးကြည့်ပါနော်၊ ချက်ချင်း ကူညီပေးပါမယ်!"
        return response.text.strip()
    except Exception as e:
        # ဘယ်လို error ပဲ ဖြစ်ဖြစ် ဒီစာသားပဲ ပေါမယ်
        return "အိုး... ခဏနေပြီး ထပ်မေးကြည့်ပါနော် 🥺\nကျွန်တော် ချက်ချင်း ပြန်လာခဲ့မယ်!"

def get_translation(text: str) -> str:
    prompt = f"""
    အောက်ပါ စာသားကို တရုတ် ↔ မြန်မာ အပြန်အလှန် ဘာသာပြန်ပေးပါ။
    ဘာသာစကား အလိုအလျောက် သိပြီး ဆန့်ကျင်ဘက်ဘာသာနဲ့ ဖြေပါ။
    အောက်ပါ format အတိုင်း လှပစွာ ရေးပါ။ emoji သုံးပြီး နွေးထွေးအောင် လုပ်ပါ။

    Translation: ...
    Pronunciation: ...
    Meaning: ...
    Example: ...

    စာသား: "{text}"
    """
    return safe_generate(prompt)

def get_explanation(text: str) -> str:
    prompt = f"""
    အောက်ပါ စကားလုံး/စာကြောင်းကို အသေးစိတ် ရှင်းပြပါ။
    တရုတ်စာဆိုရင် မြန်မာလို၊ မြန်မာစာဆိုရင် တရုတ်လို ဖြေပါ။
    အောက်ပါအချက်များ ထည့်ပေးပါ။

    • အဓိပ္ပာယ် အသေးစိတ်
    • အသံထွက် (Pinyin သို့မဟုတ် မြန်မာ အတိုင်း)
    • သဒ္ဒါပိုင်း (Grammar)
    • တကယ့်ဘဝမှာ သုံးပုံ ၂-၃ ခု
    • ဆင်တူစကားလုံး ၃-၅ ခု

    စာသား: "{text}"
    """
    return safe_generate(prompt)
