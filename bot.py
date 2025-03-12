from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# Fetch token and admin ID from Render environment variables
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send me a message, and I'll forward it to the admin.")

def forward_to_admin(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = f"Message from {user.first_name} (@{user.username}):\n\n{update.message.text}"
    context.bot.send_message(chat_id=ADMIN_ID, text=text)

def reply_to_user(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        original_text = update.message.reply_to_message.text
        user_id = int(original_text.split("\n")[0].split(" ")[-1])
        context.bot.send_message(chat_id=user_id, text=update.message.text)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_to_admin))
    dp.add_handler(MessageHandler(Filters.reply, reply_to_user))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
