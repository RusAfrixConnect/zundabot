from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7250640210:AAEWw1Zmi_jJv6KvTLBM4E3A_74L3WpwuQ0"

# Devises avec drapeaux
DEVIS = {
    "RUB": "🇷🇺",
    "EUR": "🇪🇺",
    "USD": "🇺🇸",
    "CFA": "🇨🇮",
    "THB": "🇹🇭",
    "KRW": "🇰🇷",
    "ZND": "💠 Zunda",
}

# Wallet: {user_id: {devise: solde, ...}, ...}
wallets = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Кошелёк", callback_data="wallet")],
        [InlineKeyboardButton("Купить", callback_data="buy")],
        [InlineKeyboardButton("Продать", callback_data="sell")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать в ZundaBot! Выберите опцию:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if user_id not in wallets:
        wallets[user_id] = {devise: 0 for devise in DEVIS}

    if data == "wallet":
        # Afficher solde
        text = "👜 Твой кошелёк:\n"
        for devise, flag in DEVIS.items():
            text += f"{flag} {devise}: {wallets[user_id][devise]}\n"
        await query.edit_message_text(text=text)
    
    elif data == "buy":
        keyboard = [[InlineKeyboardButton(f"{flag} {devise}", callback_data=f"buy_{devise}")] for devise, flag in DEVIS.items()]
        keyboard.append([InlineKeyboardButton("Назад", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите валюту для покупки:", reply_markup=reply_markup)

    elif data == "sell":
        keyboard = [[InlineKeyboardButton(f"{flag} {devise}", callback_data=f"sell_{devise}")] for devise, flag in DEVIS.items()]
        keyboard.append([InlineKeyboardButton("Назад", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите валюту для продажи:", reply_markup=reply_markup)

    elif data == "start":
        await start(update, context)

    elif data.startswith("buy_"):
        devise = data.split("_")[1]
        wallets[user_id][devise] += 10  # Par exemple, on ajoute 10 unités pour simuler l'achat
        await query.edit_message_text(f"✅ Вы успешно купили 10 {devise} {DEVIS[devise]}!")

    elif data.startswith("sell_"):
        devise = data.split("_")[1]
        if wallets[user_id][devise] >= 10:
            wallets[user_id][devise] -= 10  # On enlève 10 unités pour simuler la vente
            await query.edit_message_text(f"✅ Вы успешно продали 10 {devise} {DEVIS[devise]}!")
        else:
            await query.edit_message_text(f"❌ Недостаточно {devise} для продажи! Ваш баланс: {wallets[user_id][devise]}")

    else:
        await query.edit_message_text("Неизвестная команда.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()

