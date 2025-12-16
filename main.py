import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes, 
    MessageHandler,
    CallbackQueryHandler,
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


async def clique_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "pedir_localizacao":
        await query.message.reply_text(
            "Apikmoko onî makataw arpotome awekenî 📍",
            reply_markup=botao_localizacao()
        )

    elif query.data == "ajuda":
        await query.message.reply_text(
            "Enko onî ekatîmtopo, ero ahcamhoke ahce wa ciira ekenî yentopo celular yaka:"
        )
        await query.message.reply_text(
            "https://youtu.be/9gfjPUVnlE0",
            disable_web_page_preview=True
        )

        await query.message.reply_text(
            "Pona, apikmoko 📍 arpopoko ekenî yentopo!",
            reply_markup=botao_localizacao()
        )


async def receber_localizacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location

    context.user_data["lat"] = location.latitude
    context.user_data["lon"] = location.longitude

    await update.message.reply_text(
        "📍 Localização recebida!",
        reply_markup=ReplyKeyboardRemove()
    )

    await update.message.reply_text(
        "Ahce wai mepora?",
        reply_markup=menu_locais()
    )


def menu_inicial():
    botoes = [
        [InlineKeyboardButton("📍 Arpopoko ekenî yentopo", callback_data="pedir_localizacao")],
        [InlineKeyboardButton("❓ Awakrono maxe mai", callback_data="ajuda")]
    ]
    return InlineKeyboardMarkup(botoes)


def menu_locais():
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


def botao_localizacao():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📍 Arpopoko ekenî yentopo", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )



def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)^hai$'), hai))
    app.add_handler(CallbackQueryHandler(clique_menu))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, receber_localizacao))

    print("Bot iniciado!")
    app.run_polling()


if __name__ == "__main__":
    main()