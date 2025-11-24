from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from src.models.user import User
from src.database import engine
from src.config import ADMIN_IDS
from sqlalchemy import select, update
from datetime import datetime, timedelta
import asyncio

# Helper: Admin လား စစ်တယ်
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# ====================== USER COMMANDS ======================

async def request_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    async with engine.connect() as conn:
        result = await conn.execute(select(User).where(User.id == user.id))
        db_user = result.scalar_one_or_none()
        
        if db_user and db_user.is_active():
            await update.message.reply_text("သင်သည် အသုံးပြုခွင့် ရှိပြီးသားပါ။")
            return
            
        if db_user and db_user.status == "pending":
            await update.message.reply_text("သင်၏ တောင်းဆိုမှုကို စောင့်ဆိုင်းနေပါသည်။")
            return

        new_user = User(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            status="pending"
        )
        conn.add(new_user)
        await conn.commit()

    # Admin ဆီသို့ အသိပေး
    keyboard = [
        [InlineKeyboardButton("Approve", callback_data=f"approve_{user.id}_30"),
         InlineKeyboardButton("Reject", callback_data=f"reject_{user.id}")],
        [InlineKeyboardButton("1 လ", callback_data=f"approve_{user.id}_30"),
         InlineKeyboardButton("3 လ", callback_data=f"approve_{user.id}_90"),
         InlineKeyboardButton("1 နှစ်", callback_data=f"approve_{user.id}_365")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"အသုံးပြုချင်သူ အသစ်!\n\n"
                     f"ID: <code>{user.id}</code>\n"
                     f"Name: {user.full_name}\n"
                     f"Username: @{user.username or 'မရှိ'}",
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        except:
            pass
    
    await update.message.reply_text("သင်၏ တောင်းဆိုမှုကို Admin ထံ ပို့ပြီးပါပြီ။ ခဏစောင့်ပါနော်")

async def chat_with_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.args:
        await update.message.reply_text("သုံးနည်း: /chat <စာသား>")
        return
    message = " ".join(context.args)
    
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                admin_id,
                text=f"User က စာပို့လိုက်ပါတယ်:\n\n"
                     f"From: {user.full_name} (@{user.username or 'မရှိ'})\n"
                     f"ID: <code>{user.id}</code>\n\n"
                     f"{message}",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Reply", callback_data=f"replyto_{user.id}")
                ]])
            )
        except:
            pass
    await update.message.reply_text("Admin ထံ စာပို့ပြီးပါပြီ။")

# ====================== ADMIN COMMANDS ======================

async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if len(context.args) < 2:
        await update.message.reply_text("သုံးနည်း: /approve <UserID> <days>")
        return
    try:
        user_id = int(context.args[0])
        days = int(context.args[1])
    except:
        await update.message.reply_text("UserID နဲ့ ရက်အရေအတွက် မှန်ကန်စွာ ရိုက်ပါ။")
        return

    async with engine.connect() as conn:
        result = await conn.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(id=user_id, status="approved")
            conn.add(user)
        
        user.status = "approved"
        user.expires_at = datetime.utcnow() + timedelta(days=days)
        await conn.commit()

    await context.bot.send_message(user_id, f"သင်၏ အသုံးပြုခွင့်ကို ခွင့်ပြုပြီးပါပြီ။ ({days} ရက်)")
    await update.message.reply_text(f"User {user_id} ကို {days} ရက် ခွင့်ပြုပြီး")

async def reject_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if not context.args:
        await update.message.reply_text("သုံးနည်း: /reject <UserID> [အကြောင်းပြချက်]")
        return
    user_id = int(context.args[0])
    reason = " ".join(context.args[1:]) or "အကြောင်းမထူးပါ။"
    
    async with engine.connect() as conn:
        result = await conn.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.status = "rejected"
            user.note = reason
            await conn.commit()
    
    await context.bot.send_message(user_id, f"သင်၏ တောင်းဆိုမှုကို ငြင်းပယ်လိုက်ပါသည်။\nအကြောင်းပြချက်: {reason}")
    await update.message.reply_text(f"User {user_id} ကို ငြင်းပယ်ပြီး")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if not context.args: 
        await update.message.reply_text("သုံးနည်း: /kick <UserID>")
        return
    user_id = int(context.args[0])
    async with engine.connect() as conn:
        await conn.execute(update(User).where(User.id == user_id).values(status="inactive"))
        await conn.commit()
    await context.bot.send_message(user_id, "သင်၏ အသုံးပြုခွင့်ကို ယာယီရပ်ဆိုင်းလိုက်ပါသည်။")
    await update.message.reply_text(f"User {user_id} ကို kick လုပ်ပြီး")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if not context.args: 
        await update.message.reply_text("သုံးနည်း: /ban <UserID> [အကြောင်းပြချက်]")
        return
    user_id = int(context.args[0])
    reason = " ".join(context.args[1:]) or "စည်းကမ်းဖောက်ဖျက်မှု"
    
    async with engine.connect() as conn:
        await conn.execute(update(User).where(User.id == user_id).values(status="banned", banned_reason=reason))
        await conn.commit()
    
    await context.bot.send_message(user_id, f"သင့်ကို Bot မှ အပြီးပိတ်ပင်လိုက်ပါသည်။\nအကြောင်းပြချက်: {reason}")
    await update.message.reply_text(f"User {user_id} ကို အပြီးပိတ်ပင်ပြီး")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if not context.args: 
        await update.message.reply_text("သုံးနည်း: /unban <UserID>")
        return
    user_id = int(context.args[0])
    async with engine.connect() as conn:
        await conn.execute(update(User).where(User.id == user_id).values(status="approved", expires_at=None))
        await conn.commit()
    await context.bot.send_message(user_id, "သင့်ကို ပြန်လည်ဖွင့်ပေးပြီးပါပြီ။")
    await update.message.reply_text(f"User {user_id} ကို ပြန်ဖွင့်ပေးပြီး")

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if len(context.args) < 2:
        await update.message.reply_text("သုံးနည်း: /reply <UserID> <စာသား>")
        return
    user_id = int(context.args[0])
    message = " ".join(context.args[1:])
    await context.bot.send_message(user_id, f"Admin က ပြန်စာပို့လိုက်ပါတယ်:\n\n{message}")
    await update.message.reply_text(f"User {user_id} ထံ စာပို့ပြီး")

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("သုံးနည်း: /broadcast <စာသား>")
        return
    message = " ".join(context.args)
    
    async with engine.connect() as conn:
        result = await conn.execute(select(User.id).where(User.status.in_(["approved", "active"])))
        user_ids = [row[0] for row in result.fetchall()]
    
    await update.message.reply_text(f"Broadcast စတင်နေပါပြီ... ({len(user_ids)} ယောက်)")
    
    success = 0
    for i, uid in enumerate(user_ids):
        try:
            await context.bot.send_message(uid, message)
            success += 1
            if i % 20 == 0:  # Telegram rate limit မဖြစ်အောင်
                await asyncio.sleep(1)
        except:
            pass
    
    await update.message.reply_text(f"Broadcast ပြီးဆုံးပါပြီ။ ရောက်သွားသူ: {success}/{len(user_ids)}")

# Callback handler for inline buttons
async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("Access denied")
        return
    
    data = query.data
    if data.startswith("approve_"):
        user_id = int(data.split("_")[1])
        days = int(data.split("_")[2]) if "_" in data.split("_")[2:] else 30
        # Reuse approve logic
        context.args = [str(user_id), str(days)]
        await approve_user(update, context)
    elif data.startswith("reject_"):
        user_id = int(data.split("_")[1])
        context.args = [str(user_id)]
        await reject_user(update, context)
    elif data.startswith("replyto_"):
        user_id = int(data.split("_")[1])
        await query.message.reply_text(f"ပြန်စာရိုက်ပါ (User {user_id} ထံ):\n/reply {user_id} သင်ရိုက်ချင်တဲ့စာ")
