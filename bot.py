from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import json, os, asyncio

TOKEN = os.getenv("BOT_TOKEN") or "8731943430:AAEQzGgBpDzo6AXlujpDcsWpcrsKXPqlCKQ"
CHANNEL = "@Jumeirahco"
BOT_USERNAME = "Jamra_x_bot"
DATA_FILE = "data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    args = context.args
    if args and args[0]!= user_id and user_id not in data:
        inviter = args[0]
        if inviter in data:
            data[inviter]["invites"] = data[inviter].get("invites",0) + 1
        else:
            data[inviter] = {"invites": 1}
        save_data()
    if user_id not in data:
        data[user_id] = {"invites": 0}
        save_data()
    if not await is_subscribed(update.effective_user.id, context):
        keyboard = [[InlineKeyboardButton("📢 اشترك بقناة Jumeirah", url="https://t.me/Jumeirahco")],[InlineKeyboardButton("✅ تأكيد الاشتراك", callback_data="check_sub")]]
        await update.message.reply_text(f"هلا بيك بقناة Jumeirahco 👇\nحتى تستخدم البوت لازم تشترك بالقناة أولاً", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
    await update.message.reply_text(f"✅ أهلاً بيك!\n📊 دعواتك: {data[user_id].get('invites',0)}\n\n🔗 رابط دعوتك:\n{link}\n\nدز /points لمعرفة نقاطك")

async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    await update.message.reply_text(f"🏆 نقاطك: {data.get(uid, {}).get('invites',0)} دعوة")

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if await is_subscribed(query.from_user.id, context):
        await query.message.delete()
        uid = str(query.from_user.id)
        link = f"https://t.me/{BOT_USERNAME}?start={uid}"
        await context.bot.send_message(query.from_user.id, f"✅ تم الاشتراك!\n🔗 رابطك: {link}")
    else:
        await query.answer("❌ انت ما مشترك بعد!", show_alert=True)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("points", points))
    app.add_handler(CallbackQueryHandler(check_button, pattern="check_sub"))
    print("بوت Jumeirah اشتغل 24 ساعة...")
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
