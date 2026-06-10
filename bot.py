from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8500343306:AAE1XJ9s7lFmR87cO_7HHWJHSP56E924ews"

import json
import os

if os.path.exists("scores.json"):
    with open("scores.json", "r", encoding="utf-8") as f:
        players = json.load(f)
else:
    players = {}

questions = [
    {
        "q": "Какой герой может украсть ультимейт?",
        "options": ["Лейла", "Валентина", "Сабер", "Тигрил"],
        "correct": 1
    },
    {
        "q": "Какая роль берёт Лорда?",
        "options": ["Маг", "Лесник", "Танк", "Стрелок"],
        "correct": 1
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Начать викторину", callback_data="start")],
        [InlineKeyboardButton("🏆 Рейтинг", callback_data="rating")]
    ]

    text = "🎮 MLBB Quiz Bot\n👑 Создатель: Нодирбек"

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "start":
        players[user_id] = {"score": 0, "q": 0, "name": query.from_user.first_name}
        await send_question(query, user_id)

    elif query.data == "rating":
        text = "🏆 Рейтинг:\n"
        for p in players.values():
            text += f"{p['name']} — {p['score']}\n"
        await query.message.reply_text(text)

    elif query.data.startswith("a_"):
        answer = int(query.data.split("_")[1])
        q = players[user_id]["q"]

        if answer == questions[q]["correct"]:
            players[user_id]["score"] += 1

        players[user_id]["q"] += 1

        if players[user_id]["q"] >= len(questions):
            score = players[user_id]["score"]
            await query.message.reply_text(f"Финиш! Твой счёт: {score}")
        else:
            await send_question(query, user_id)


async def send_question(query, user_id):
    q_num = players[user_id]["q"]
    q = questions[q_num]

    keyboard = []
    for i, opt in enumerate(q["options"]):
        keyboard.append([InlineKeyboardButton(opt, callback_data=f"a_{i}")])

    await query.message.reply_text(q["q"], reply_markup=InlineKeyboardMarkup(keyboard))


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot started")
app.run_polling()
