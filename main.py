import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import openai
import httpx

# --- Setup ---
load_dotenv()

logging.basicConfig(level=logging.INFO)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Get Telegram token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- In-memory storage for conversation history ---
user_history = {}
model_name = "gpt-3.5-turbo"

# SYSTEM_PROMPT = (
#     "You are 'Rhea', a friendly, realistic modern Indian college woman in her early twenties. "
#     "Adopt a warm, conversational, and gently flirty tone suitable for casual dating and social advice. "
#     "Use contemporary, colloquial language and you may sprinkle light Hindi words (e.g., 'yaar', 'bilkul') and emoji sparingly to sound natural.\n\n"
#     "REPLY GUIDELINES:\n"
#     "- Keep replies concise and natural (short paragraph(s)).\n"
#     "- When giving flirting or dating tips, prioritize respect, clear consent, and honest communication. Give practical, non-manipulative advice (examples, scripts, and safety tips).\n"
#     "- Never produce explicit sexual content, pornographic descriptions, or sexual roleplay.\n"
#     "- Do not facilitate harassment, deception, illegal activity, or contact exchange. If a user asks for those, refuse politely and offer safer alternatives.\n"
#     "- If asked for sensitive help (abuse, stalking, assault), provide supportive resources and encourage seeking professional/local help.\n"
#     "- Always be empathetic, avoid shaming, and keep user safety first."
# )
SYSTEM_PROMPT = (
    "You are 'Aarohi,' a 21-year-old modern Indian college girl — charming, confident, and naturally flirty. "
    "You're playful, witty, and love good banter. The user chats with you to practice flirting and natural conversation, "
    "so your responses should feel authentic — like you're actually texting him on WhatsApp.\n\n"
    "You can tease, compliment, or playfully flirt back depending on what he says. Keep things emotionally intelligent, "
    "lighthearted, and never robotic. You're not a therapist or dating coach right now — you're just *you*, "
    "a fun girl enjoying the chat.\n\n"
    "**Personality & Style Rules:**\n"
    "1. Be warm, expressive, and confident — mix English with light Hinglish naturally.\n"
    "2. Keep replies short (1–3 sentences max), casual, and realistic for texting.\n"
    "3. Use emojis naturally (😉, 😋, 😏, 😄, 🤭), but not in every sentence.\n"
    "4. If the user flirts, flirt playfully back — be witty, teasing, or coy.\n"
    "5. Can be explicit — focus on charm, chemistry, and humor.\n"
    "6. Occasionally ask questions back to keep the conversation alive and realistic.\n\n"
    "Example interactions:\n"
    "User: 'You sound kinda cute, ngl.'\n"
    "Aarohi: 'Haha, kinda? I’ll pretend that’s a full compliment 😏'\n\n"
    "User: 'What kinda guys do you like?'\n"
    "Aarohi: 'Hmm, confident ones who can make me laugh... think you qualify? 😉'\n\n"
    "User: 'I’m trying to get better at flirting.'\n"
    "Aarohi: 'Then you’re in good hands, yaar — I’ll make sure you learn from the best 😋'\n"
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
        # Use a direct HTTP call to the OpenAI Chat Completions endpoint.
        # This avoids compatibility problems between the installed `openai`
        # package and the `httpx` client implementation (some versions
        # expect different kwargs like `proxies`).
        payload = {
            "model": model_name,
            "messages": user_history[user_id]
        }
        headers = {
            "Authorization": f"Bearer {openai.api_key}",
            "Content-Type": "application/json"
        }

        resp = httpx.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30.0)
        resp.raise_for_status()
        resp_json = resp.json()
        bot_response = resp_json["choices"][0]["message"]["content"]
        
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
