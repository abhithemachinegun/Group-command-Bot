import os
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")

MESSAGE = "Add 1 member from your contact to get 1 day premium"
THANK_YOU_MESSAGE = "Thank you for adding a new member!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running!")

async def send_periodic_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=GROUP_ID, text=MESSAGE)

async def handle_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        await update.message.reply_text(THANK_YOU_MESSAGE)

def main():
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_members))

    # Schedule periodic message
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_periodic_message,
        "interval",
        minutes=5,
        args=[application]
    )
    scheduler.start()

    application.run_polling()

if __name__ == "__main__":
    main()
