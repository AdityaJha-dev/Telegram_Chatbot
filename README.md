# Telegram AI Chatbot

An asynchronous Telegram chatbot built with aiogram that integrates OpenAI’s API to generate AI-driven responses to user messages. The project demonstrates building a production-style Telegram bot with async handling, environment-based configuration, and external API integration.

## Overview
This project implements a Telegram chatbot that listens for incoming user messages and generates responses using an OpenAI language model. It uses long polling with aiogram and is structured to handle errors, logging, and configuration cleanly.

The bot is designed as a foundation for AI-powered conversational assistants on Telegram.

## Features
- Asynchronous Telegram bot using aiogram
- Integration with OpenAI API for AI-generated responses
- Environment variable–based configuration
- Logging and basic error handling
- Modular structure for easy extension

## Tech Stack
- Python
- aiogram
- Langchain
- Gen AI
- OpenAI API
- asyncio

## Project Structure
├── main.py                         # Main bot logic and event loop

├── test.py                         # Testing and experimentation

├── requirements.txt                # Python dependencies

├── system_prompt_examples.txt      # Prompt configuration examples

├── research/
└── echo_bot.py                 # Reference / experimental bot

├── LICENSE

└── README.md


## Setup Instructions

### 1. Create a Telegram bot
- Open Telegram and search for @BotFather
- Create a new bot and obtain the Bot Token

### 2. Clone the repository
git clone https://github.com/<your-username>/Telegram_Chatbot.git  
cd Telegram_Chatbot  

### 3. Create and activate a virtual environment
python -m venv venv  
source venv/bin/activate  

### 4. Install dependencies
pip install -r requirements.txt  

### 5. Configure environment variables
Create a `.env` file in the root directory and add:
TELEGRAM_BOT_TOKEN=your_telegram_bot_token  
OPENAI_API_KEY=your_openai_api_key  

### 6. Run the bot
python main.py  

The bot will start polling and responding to messages on Telegram.

## Usage
- Start a chat with the bot on Telegram
- Send a message to receive an AI-generated response
- Logs are printed to the console for debugging and monitoring

## Notes
- API keys must never be committed to version control
- The project uses long polling; webhook deployment can be added
- Designed for learning, experimentation, and extension

## Future Improvements
- Conversation memory and context handling
- Command-based configuration
- Rate limiting and request batching
- Deployment with Docker and webhooks

## License
This project is licensed under the MIT License.

