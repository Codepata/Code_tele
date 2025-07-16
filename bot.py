from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
import os
import dotenv

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! Send me your code snippet and I'll try to find bugs and suggest best practices (powered by Gemini)."
    )

async def analyze_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text

    prompt = (
        "You are a strict and helpful senior code reviewer. Please analyze the following code snippet, "
        "find possible bugs, suggest improvements, and mention best practices. Code:\n" + user_code
    )

    response = model.generate_content(prompt)
    feedback = response.text

    if not feedback:
        feedback = "❗ Sorry, I couldn't analyze the code. Please try again with a valid snippet."

    await update.message.reply_text(feedback[:4000])  # Telegram text limit

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), analyze_code))

    print("🤖 Bot with Gemini is running...")
    app.run_polling()
