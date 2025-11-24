import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from src.config import TELEGRAM_TOKEN
# 🌟 /start command handler ကို မှန်ကန်စွာ ထည့်သွင်း import လုပ်ခြင်း
from src.handlers.messages import start, handle_text, handle_voice, user_callback
from src.handlers.admin import admin_panel, admin_callback

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_TOKEN is missing in .env file")
        exit(1)

    print("🚀 Bot is starting...")
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # 🌟 /start command ကို မှတ်ပုံတင်ပါ
    application.add_handler(CommandHandler('start', start))
    
    # Admin Handlers
    application.add_handler(CommandHandler('admin', admin_panel))
    application.add_handler(CallbackQueryHandler(admin_callback, pattern="^admin_"))
    
    # User Handlers
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(CallbackQueryHandler(user_callback, pattern="^explain"))
    
    application.run_polling()
