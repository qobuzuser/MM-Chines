from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.config import ADMIN_IDS
from src.utils.state import is_bot_active, set_bot_active

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        return # Ignore non-admins

    is_active = is_bot_active()
    status_text = "🟢 Online" if is_active else "🔴 Offline"
    
    keyboard = [
        [
            InlineKeyboardButton("🟢 Turn ON", callback_data="admin_on"),
            InlineKeyboardButton("🔴 Turn OFF", callback_data="admin_off")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🛡 **Admin Control Panel**\n\nCurrent Status: {status_text}",
        reply_markup=reply_markup
    )

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    if user_id not in ADMIN_IDS:
        await query.answer("Access Denied", show_alert=True)
        return

    await query.answer()
    
    if query.data == "admin_on":
        set_bot_active(True)
        await query.edit_message_text("✅ **Bot is now PUBLIC (ONLINE).**")
    elif query.data == "admin_off":
        set_bot_active(False)
        await query.edit_message_text("⛔️ **Bot is now MAINTENANCE (OFFLINE).**")
