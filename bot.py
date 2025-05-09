# bot.py

from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import re
from config import BOT_TOKEN, REPLACE_USERNAME, REPLACE_LINK
import os

USERNAME_PATTERN = re.compile(r'@\w+')
LINK_PATTERN = re.compile(r'https?://\S+')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text
        new_text = USERNAME_PATTERN.sub(REPLACE_USERNAME, text)
        new_text = LINK_PATTERN.sub(REPLACE_LINK, new_text)
        await update.message.reply_text(new_text)

    elif update.message and update.message.document:
        file = await update.message.document.get_file()
        file_path = f'downloads/{update.message.document.file_name}'
        await file.download_to_drive(file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        content = USERNAME_PATTERN.sub(REPLACE_USERNAME, content)
        content = LINK_PATTERN.sub(REPLACE_LINK, content)

        new_file_path = f'downloads/edited_{update.message.document.file_name}'
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        await update.message.reply_document(document=InputFile(new_file_path))

async def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.Document.TEXT, handle_message))
    print("Bot is running...")
    await app.run_polling()
