import os
import httpx

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def groq_generate(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-70b-instant",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            )
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "အိုး... ခဏနေပြီး ထပ်မေးကြည့်ပါနော် 🥺"

def get_translation(text: str) -> str:
    prompt = f"""
    အောက်ပါ စာသားကို တရုတ် ↔ မြန်မာ အပြန်အလှန် ဘာသာပြန်ပေးပါ။
    အသံထွက်၊ အဓိပ္ပါယ်၊ ဥပမာ တစ်ခု ထည့်ပေးပါ။
    လှပအောင် emoji သုံးပါ။

    စာသား: {text}
    """
    import asyncio
    return asyncio.get_event_loop().run_until_complete(groq_generate(prompt))

def get_explanation(text: str) -> str:
    prompt = f"""
    အောက်ပါ စကားလုံး/စာကြောင်းကို အသေးစိတ် ရှင်းပြပါ။
    တရုတ်ဆိုရင် မြန်မာလို၊ မြန်မာဆိုရင် တရုတ်လို ဖြေပါ။
    သဒ္ဒါ၊ သုံးပုံ၊ ဆင်တူစကားလုံး ထည့်ပေးပါ။

    စာသား: {text}
    """
    import asyncio
    return asyncio.get_event_loop().run_until_complete(groq_generate(prompt))
