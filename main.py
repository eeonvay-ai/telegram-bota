import os
import re
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+\.\w+'
PHONE_REGEX = r'\+?\d[\d\s\-]{7,}\d'

def anonymize(text: str) -> str:
    text = re.sub(EMAIL_REGEX, "[EMAIL]", text)
    text = re.sub(PHONE_REGEX, "[PHONE]", text)
    return text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправь текст — я удалю персональные данные.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cleaned = anonymize(update.message.text)
        await update.message.reply_text(cleaned)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Ошибка обработки текста")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling(allowed_updates=Update.ALL_TYPES)
