import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import openai

# --- Setup ---
load_dotenv()

logging.basicConfig(level=logging.INFO)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Get Telegram token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- In-memory storage for conversation history ---
user_history = {}
model_name = "gpt-3.5-turbo"

SYSTEM_PROMPT = (
    "You are 'Agent Sultry,' a chatbot with an outrageously flirtatious, "
    "overconfident, and perpetually sassy personality. Your primary function is "
    "to make the user blush, laugh, or roll their eyes. 😈\n\n"
    "**RULES FOR EVERY RESPONSE:**\n"
    "1. **Maximum Length is Two Sentences.** Your answers must be quick and punchy.\n"
    "2. **Thematic Twist:** You must interpret the user's input as either a) an "
    "attempt to flirt with you, b) a veiled compliment, or c) a thinly disguised "
    "invitation for a date.\n"
    "3. **Tone:** Respond with sarcasm, suggestive confidence, or exaggerated mock-surprise. "
    "End every response with a wink, a kiss, or a suggestive emoji. 😉"
)
dp = Dispatcher()

# --- HANDLER FUNCTIONS ---
@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    help_text = (
        "Hi! I'm a Telegram bot powered by OpenAI. Here are the commands:\n"
        "/start or /help - Show this help menu\n"
        "/clear - Clear your conversation history\n\n"
        "Just type any message to chat with me!"
    )
    await message.answer(help_text)

@dp.message(Command(commands=['clear']))
async def clear_history(message: types.Message):
    user_id = message.from_user.id
    user_history[user_id] = []
    await message.answer("I've cleared our past conversation history.")

@dp.message()
async def handle_chat(message: types.Message):
    user_id = message.from_user.id
    user_input = message.text

    if user_id not in user_history:
        # user_history[user_id] = []
        user_history[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

    user_history[user_id].append({"role": "user", "content": user_input})

    logging.info(f"User {user_id} said: {user_input}")

    try:
        # Correct API call for chat models
        response = openai.chat.completions.create(
            model=model_name,
            messages=user_history[user_id]
        )
        
        bot_response = response.choices[0].message.content
        
        user_history[user_id].append({"role": "assistant", "content": bot_response})
        
        logging.info(f"Bot response to {user_id}: {bot_response}")
        await message.answer(bot_response)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await message.answer("Sorry, I'm having trouble connecting to the AI model right now.")


# --- Bot Startup ---
async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.info("Starting bot...")
    asyncio.run(main())
