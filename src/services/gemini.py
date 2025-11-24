import os
import google.generativeai as genai

# Configure
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Model
model = genai.GenerativeModel("gemini-2.5-flash")

def get_translation(text: str) -> str:
    prompt = f"""
    You are the best Chinese-Myanmar dictionary teacher.
    Input: "{text}"

    Auto-detect language (Chinese or Myanmar).
    Reply in the OPPOSITE language.
    Always include:
    • Translation
    • Pronunciation (Pinyin for Chinese, Romanization for Myanmar in English letters)
    • Short meaning
    • One real-life example sentence

    Format beautifully with emojis like:
    Translation: ...
    Pronunciation: ...
    Meaning: ...
    Example: ...

    Be warm and encouraging.
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.4,
                "max_output_tokens": 800,
            }
        )
        return response.text.strip()
    except Exception as e:
        return f"ယာယီချို့ယွင်းနေပါသည်: {str(e)}"


# ဒီ function ကို ထည့်ပေးလိုက်တယ်!
def get_explanation(text: str) -> str:
    prompt = f"""
    အောက်ပါ စကားလုံး/စကားစုကို အသေးစိတ် ရှင်းပြပါ: "{text}"

    ရှင်းပြရမယ့်အချက်များ:
    • အဓိပ္ပာယ် အသေးစိတ်
    • အသံထွက် (Pinyin သို့မဟုတ် Romanization)
    • သဒ္ဒါပိုင်း (Grammar)
    • တကယ့်ဘဝမှာ သုံးပုံများ (၂-၃ ခု)
    • ဆင်တူစကားလုံး ၃-၅ ခု
    • သတိထားရမယ့်အချက် (ရှိရင်)

    တရုတ်စာဆိုရင် မြန်မာလို ဖြေ
    မြန်မာစာဆိုရင် တရုတ်လို ဖြေ
    လှပအောင် emoji သုံးပြီး ကျောင်းသားတွေ နားလည်လွယ်အောင် ရေးပါ။
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.6,
                "max_output_tokens": 1000,
            }
        )
        return response.text.strip()
    except Exception as e:
        return "ယာယီ ရှင်းပြလို့ မရပါ။ နောက်မှ ထပ်ကြိုးစားပါ။"
