import os
import tempfile
import asyncio
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ContextTypes

# Gemini ကို သုံးမယ်
from src.services.gemini import get_translation, get_explanation

# gTTS အသံထုတ်ဖို့
from src.utils.tts import text_to_speech, cleanup_file

# အခြေအနေ စစ်ဖို့
from src.utils.state import is_bot_active
from src.config import ADMIN_IDS


# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "မင်္ဂလာပါ ချစ်သောကျောင်းသားများ\n\n"
        "ကျွန်တော်က တရုတ်-မြန်မာ အပြန်အလှန် အဘိဓာန် Bot ပါ။\n"
        "စာရိုက်ရုံပဲ — အလိုအလျောက် ဘာသာပြန် + အသံထွက် ထွက်လာပါမယ်\n\n"
        "တရုတ်စာရိုက်ရင် → မြန်မာလို ပြန်ပေးမယ်\n"
        "မြန်မာစာရိုက်ရင် → တရုတ်လို ပြန်ပေးမယ်\n"
        "အသံထွက်ကို အင်္ဂလိပ်စာလုံးနဲ့ ရေးပြပြီး အသံဖိုင်ပါ ထွက်လာမယ်နော်\n\n"
        "စမ်းကြည့်လိုက်ပါ! ဥပမာ → 你好 / မင်္ဂလာပါ\n\n"
        "Developed by @MyanmarTecharea"
    )
    await update.message.reply_text(welcome_text, parse_mode=constants.ParseMode.HTML)


# Core function — အဓိက လုပ်ဆောင်ချက်
async def _process_and_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, user_input: str, is_audio=False):
    MAX_RETRIES = 2
    RETRY_DELAY = 8

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)

    for attempt in range(MAX_RETRIES + 1):
        try:
            
            response_text = get_translation(user_input)

            # Save for "Explain More"
            context.user_data['last_query'] = user_input
            context.user_data['last_sender'] = update.effective_user.id

           
            keyboard = [[InlineKeyboardButton("More Explanation", callback_data="explain")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            
            sent_msg = await update.message.reply_text(
                response_text,
                reply_markup=reply_markup,
                parse_mode=constants.ParseMode.MARKDOWN
            )

            
            pron_match = re.search(r"(?:Pronunciation|Pinyin|အသံထွက်)[\s:]*([^\n\r]+)", response_text, re.IGNORECASE)
            if pron_match:
                pronunciation = pron_match.group(1).strip()

                # တရုတ်စာပါရင် zh-CN၊ မပါရင် en (romanization)
                lang = "zh-CN" if any('\u4e00' <= c <= '\u9fff' for c in pronunciation) else "en"
                audio_path = text_to_speech(pronunciation, lang=lang)

                if audio_path and os.path.exists(audio_path):
                    await context.bot.send_voice(
                        chat_id=update.effective_chat.id,
                        voice=open(audio_path, 'rb'),
                        caption="Pronunciation",
                        reply_to_message_id=sent_msg.message_id
                    )
                    
                    cleanup_file(audio_path)

            return

        except Exception as e:
            if attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY)
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
            else:
                await update.message.reply_text("ယာယီချို့ယွင်းနေပါသည်။ ခဏနောက် ထပ်ကြိုးစားပါ။")


# Text message handler
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_bot_active() and update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Bot ကို ပြုပြင်နေပါသည်။ ခဏစောင့်ပါ။")
        return

    user_text = update.message.text.strip()
    if not user_text:
        return

    await _process_and_reply(update, context, user_text, is_audio=False)


# Voice message handler (ယာယီ ပိတ်ထား — နောက်မှ ထည့်မယ်)
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_bot_active() and update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Bot ကို ပြုပြင်နေပါသည်။ ခဏစောင့်ပါ။")
        return

    await update.message.reply_text(
        "အသံဘာသာပြန်ခြင်း ယာယီရပ်ထားပါသည်။\n"
        "စာသားရိုက်ပို့ပြီး သုံးပေးပါနော်"
    )


# "More Explanation" callback
async def user_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data != "explain":
        return

    last_text = context.user_data.get('last_query')
    last_sender = context.user_data.get('last_sender')

    if not last_text or last_sender != query.from_user.id:
        await query.message.reply_text("ယခင်မေးခွန်းကို ရှာမတွေ့ပါ။")
        return

    await query.message.reply_text("အသေးစိတ် ရှင်းပြပေးနေပါသည်...")
    explanation = await asyncio.to_thread(get_explanation, last_text)
    await query.message.reply_text(
        f"အသေးစိတ်ရှင်းလင်းချက်:\n\n{explanation}",
        parse_mode=constants.ParseMode.MARKDOWN
    )
