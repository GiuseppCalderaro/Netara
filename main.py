import math
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

#Locais para calculo de distancia com latitude e logintude: giusepp calderaro
LOCAIS = {
    "super": [
        ("Mercantil e Açougue O Barateiro", -1.753598, -55.856369),
        ("Santer 3", -1.7547744998567902, -55.85472341848487),
        ("Atacadão Eco", -1.7618465213001782, -55.86370487085367),
    ],
    "bank": [
        ("Banco do Brasil", -1.7655606814000302, -55.86984729287881),
        ("Banpará", -1.7668824006979742, -55.869033249861204),
        ("Bradesco", -1.7667152836195947, -55.867286748340966),
    ],
    "farm": [
        ("Sanfarma", -1.7544264414912054, -55.8567937836081),
        ("Drogarias Ultra Popular", -1.7555832761989438, -55.85766077504346),
        ("Drogarias Ultra Popular", -1.7675464814242734, -55.86937839865242),
        ("Vita Farma 24h", -1.757026408341188, -55.85914746512182),
    ],
    "rest": [
        ("Restaurante Local", -1.452, -48.488),
        ("Cantina Comunitária", -1.456, -48.486),
    ]
}


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


def botao_localizacao():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📍 Arpopoko ekenî yentopo", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def menu_voltar():
    botoes = [
        #[InlineKeyboardButton("📍 Anarî ekenî", callback_data="nova_local")],
        [InlineKeyboardButton("⬅️ Etîramaki yihcitopo pona", callback_data="menu_locais")]
    ]
    return InlineKeyboardMarkup(botoes)


def teclado_localizacao():
    teclado = [[KeyboardButton("📍Arpopoko ekenî yentopo", request_location=True)]]
    return ReplyKeyboardMarkup(teclado, resize_keyboard=True, one_time_keyboard=True)

def calcular_distancia(lat1, lon1, lat2, lon2):
    # Fórmula para calcular distancia: Giusepp Calderaro
    R = 6371  # raio da Terra para calcular a distancia: Giusepp Calderaro
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def encontrar_mais_proximo(lat_user, lon_user, locais, limite=3):
    resultados = []

    for nome, lat, lon in locais:
        distancia = calcular_distancia(lat_user, lon_user, lat, lon)
        resultados.append((nome, lat, lon, distancia))

    resultados.sort(key=lambda x: x[3])
    return resultados[:limite]


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
    context.user_data["localizacao"] = update.message.location

    await update.message.reply_text(
        "📍 Ekenî wenwo ha!",
        reply_markup=ReplyKeyboardRemove()
    )

    await update.message.reply_text(
        "Ahce wai mepora?",
        reply_markup=menu_locais()
    )


async def tratar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu_locais":
        await query.message.reply_text(
            "Ahce wai mepora?",
            reply_markup=menu_locais()
        )
        return

    if query.data == "nova_local":
        await query.message.reply_text(
            "Envie uma nova localização 📍",
            reply_markup=teclado_localizacao()
        )
        return


    if "localizacao" not in context.user_data:
        await query.message.reply_text("Primeiro envie sua localização 📍")
        return

    lat_user = context.user_data["localizacao"].latitude
    lon_user = context.user_data["localizacao"].longitude

    locais_categoria = LOCAIS.get(query.data)

    if not locais_categoria:
        await query.message.reply_text("Ekenî exihra ❌")
        return

    locais_proximos = encontrar_mais_proximo(
        lat_user,
        lon_user,
        locais_categoria,
        limite=3
    )

    if not locais_proximos:
        await query.message.reply_text("Ekenî exihra ❌")
        return


    await query.message.edit_text(
        "📍 *Morotono ekenî komo onî*",
        parse_mode="Markdown"
    )

    for nome, lat, lon, dist in locais_proximos:
        await query.message.reply_text(
            f"📍 *{nome}*\n📏 On wicakî moxenonî: *{dist:.2f} km*",
            parse_mode="Markdown"
        )

        await query.message.reply_location(
            latitude=lat,
            longitude=lon
        )

    await query.message.reply_text(
        "Awetîrama xe mai mepora katî anarî hara?",
        reply_markup=menu_voltar()
    )



def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)^hai$'), hai))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, receber_localizacao))
    app.add_handler(
        CallbackQueryHandler(
            clique_menu,
            pattern="^(pedir_localizacao|ajuda)$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            tratar_menu,
            pattern="^(super|bank|farm|rest|menu_locais|nova_local)$"
        )
    )

    print("Bot iniciado!")
    app.run_polling()


if __name__ == "__main__":
    main()