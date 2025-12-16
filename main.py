import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes, 
    MessageHandler,
    filters
)

TOKEN = "7878212761:AAGsDzvKHa4333__o9TJosfeth4-wD5CPO8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hai! Owî Netara 👋",
        reply_markup=menu_inicial()
    )

async def hai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


def menu_inicial():
    botoes = [
        [InlineKeyboardButton("📍 Arpopoko ekenî yentopo", callback_data="pedir_localizacao")],
        [InlineKeyboardButton("❓ Awakrono maxe mai", callback_data="ajuda")]
    ]
    return InlineKeyboardMarkup(botoes)


def criar_menu():
    botoes = [
        [InlineKeyboardButton("🛒 Warawantacho", callback_data="super")],
        [InlineKeyboardButton("🏦 Puranta mohkacho", callback_data="bank")],
        [InlineKeyboardButton("💊 Kasarai mînî", callback_data="farm")],
        [InlineKeyboardButton("🍽 Kesereskmacho", callback_data="rest")]
    ]
    return InlineKeyboardMarkup(botoes)

def pedir_localizacao():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📍 Enviar Localização", request_location=True)]],
        one_time_keyboard=True,
        resize_keyboard=True
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)^hai$'), hai))
    app.add_handler(CommandHandler("start", start))

    print("Bot iniciado!")
    app.run_polling()


if __name__ == "__main__":
    main()