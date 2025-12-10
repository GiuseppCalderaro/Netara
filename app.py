import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

TOKEN = "7878212761:AAGsDzvKHa4333__o9TJosfeth4-wD5CPO8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou o Netarã 👋")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot iniciado!")
    app.run_polling()


if __name__ == "__main__":
    main()
