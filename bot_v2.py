import logging
import os
import random
import unicodedata

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from quiz_data import QUIZ_QUESTIONS

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

QUESTIONS_PER_QUIZ = 5


def normalize(text):
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cat="Yayi"
    questions=[q for q in QUIZ_QUESTIONS if q.get('category')==cat] 

    context.chat_data["game"] = {
        "active": True,
        "current_question_index": 0,
        "questions": random.sample(questions, QUESTIONS_PER_QUIZ),
        "scores": {},
        "answered": False,
        "current_answer": None
    }

    await send_question(update, context)


async def send_question(update, context):

    game = context.chat_data["game"]

    index = game["current_question_index"]
    question_data = game["questions"][index]

    game["current_answer"] = normalize(question_data["answers"][0])
    game["answered"] = False

    question_text = (
        f"❓ Question {index+1}/{QUESTIONS_PER_QUIZ}\n\n"
        f"{question_data['question']}\n\n"
        f"💬 Write the answer in the chat!"
    )

    await update.effective_chat.send_message(question_text)


async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):

    game = context.chat_data.get("game")

    if not game or not game["active"]:
        return

    if game["answered"]:
        return

    user_message = normalize(update.message.text)
    correct_answer = game["current_answer"]

    if user_message != correct_answer:
        return

    game["answered"] = True

    user = update.message.from_user
    user_id = user.id
    name = user.first_name

    scores = game["scores"]

    if user_id not in scores:
        scores[user_id] = {
            "name": name,
            "points": 0
        }

    scores[user_id]["points"] += 1

    await update.message.reply_text(
        f"🏆 {name} answered correctly!"
    )

    await show_live_ranking(update, context)

    await next_question(update, context)


async def show_live_ranking(update, context):

    scores = context.chat_data["game"]["scores"]

    ranking = sorted(
        scores.values(),
        key=lambda x: x["points"],
        reverse=True
    )

    text = "📊 Current Ranking\n\n"

    for i, player in enumerate(ranking[:5], start=1):
        text += f"{i}. {player['name']} — {player['points']} pts\n"

    await update.effective_chat.send_message(text)


async def next_question(update, context):

    game = context.chat_data["game"]

    game["current_question_index"] += 1

    if game["current_question_index"] >= QUESTIONS_PER_QUIZ:

        await show_final_ranking(update, context)
        game["active"] = False
        return

    await send_question(update, context)


async def show_final_ranking(update, context):

    scores = context.chat_data["game"]["scores"]

    ranking = sorted(
        scores.values(),
        key=lambda x: x["points"],
        reverse=True
    )

    text = "🏆 FINAL RESULTS\n\n"

    medals = ["🥇", "🥈", "🥉"]

    for i, player in enumerate(ranking):

        medal = medals[i] if i < 3 else " "

        text += f"{medal} {player['name']} — {player['points']} pts\n"

    await update.effective_chat.send_message(text)


def main():

    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    application.add_handler(CommandHandler("quiz", quiz))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess)
    )

    application.run_polling()


if __name__ == "__main__":
    main()
