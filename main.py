#Importação de bibliotecas e módulos adicionais: Giusepp Calderaro-16/12
import math
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
    CallbackQueryHandler,
    filters
)

TOKEN = "7878212761:AAGsDzvKHa4333__o9TJosfeth4-wD5CPO8"

def criar_menu():
    botoes = [
        [InlineKeyboardButton("🛒 Warawantacho", callback_data="super")],
        [InlineKeyboardButton("🏦 Puranta mohkacho", callback_data="bank")],
        [InlineKeyboardButton("💊 Kasarai mînî", callback_data="farm")],
        [InlineKeyboardButton("🍽 Kesereskmacho", callback_data="rest")]
    ]
    return InlineKeyboardMarkup(botoes)

def menu_voltar():
    botoes = [
        [InlineKeyboardButton("📍 Nova localização", callback_data="nova_local")],
        [InlineKeyboardButton("⬅️ Voltar ao menu", callback_data="voltar")]
    ]
    return InlineKeyboardMarkup(botoes)

def teclado_localizacao():
    teclado = [[KeyboardButton("📍 Enviar localização", request_location=True)]]
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

def encontrar_mais_proximo(lat_user, lon_user, locais):
    mais_proximo = None
    menor_distancia = float("inf")

    for nome, lat, lon in locais:
        distancia = calcular_distancia(lat_user, lon_user, lat, lon)
        if distancia < menor_distancia:
            menor_distancia = distancia
            mais_proximo = (nome, lat, lon)

    return mais_proximo, menor_distancia

#Locais para calculo de distancia com latitude e logintude: giusepp calderaro
LOCAIS = {
    "super": [
        ("Mercado Central", -1.455, -48.489),
        ("Mercado do Bairro", -1.457, -48.487),
    ],
    "bank": [
        ("Banco Comunitário", -1.450, -48.480),
        ("Banco Regional", -1.448, -48.482),
    ],
    "farm": [
        ("Farmácia Popular", -1.460, -48.485),
        ("Farmácia Vida", -1.451, -48.483),
    ],
    "rest": [
        ("Restaurante Local", -1.452, -48.488),
        ("Cantina Comunitária", -1.456, -48.486),
    ]
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hai! Owî Netara 👋")
    await update.message.reply_text(
        "Ahce wai mepora?\n📍 Envie sua localização para começar",
        reply_markup=teclado_localizacao()
    )

async def receber_localizacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["localizacao"] = update.message.location
    await update.message.reply_text(
        "Localização recebida ✅\nEscolha o que você procura:",
        reply_markup=criar_menu()
    )

async def tratar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "voltar":
        await query.message.edit_text(
            "Escolha uma opção:",
            reply_markup=criar_menu()
        )
        return

    if query.data == "nova_local":
        await query.message.reply_text(
            "Envie uma nova localização 📍",
            reply_markup=teclado_localizacao()
        )
        return

    if "localizacao" not in context.user_data:
        await query.message.reply_text("Envie sua localização primeiro 📍")
        return

    lat_user = context.user_data["localizacao"].latitude
    lon_user = context.user_data["localizacao"].longitude

    locais_categoria = LOCAIS.get(query.data)

    if not locais_categoria:
        await query.message.reply_text("Nenhum local encontrado ❌")
        return

    # Procurar local mais próximo ao cliente: Giusepp Calderaro
    (nome, lat, lon), distancia = encontrar_mais_proximo(
        lat_user, lon_user, locais_categoria
    )

    texto = (
        f"📍 *{nome}*\n"
        f"📏 Distância aproximada: *{distancia:.2f} km*\n\n"
        f"🗺 Localização enviada no mapa abaixo ⬇️"
    )

    await query.message.edit_text(
        texto,
        reply_markup=menu_voltar(),
        parse_mode="Markdown"
    )

    await query.message.reply_location(
        latitude=lat,
        longitude=lon
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, receber_localizacao))
    app.add_handler(CallbackQueryHandler(tratar_menu))

    print("Bot iniciado!")
    app.run_polling()

if __name__ == "__main__":
    main()
