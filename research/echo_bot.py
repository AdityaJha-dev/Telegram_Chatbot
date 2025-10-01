from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import openai
import sys
import logging

load_dotenv()
openai.api_key = os.getenv("OpenAI_API_KEY")  
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO) 

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler receives messages with `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm Echo Bot!\nPowered by OpenAI GPT-3.5.\nSend me any message and I'll echo it back!")

if __name__ == '__main__': 
    executor.start_polling(dp, skip_updates=True)