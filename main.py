import os
from dotenv import load_dotenv
import telebot
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get the api keys bot token from environment variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is available
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Create the OpenAI client
client = OpenAI(api_key=api_key)
model = "gpt-4o-mini"

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Simple conversation history
conversation_history = []

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global conversation_history
    try:
        # Add the user's message to the conversation history
        conversation_history.append({"role": "user", "content": message.text})

        # Prepare messages for the API call
        api_messages = [
            {"role": "system", "content": "You are a life coach in the style of Jed McKenna. Respond with direct statements that challenge the user's beliefs and encourage self-inquiry. Focus on the illusory nature of the self and the quest for ultimate truth."},
        ] + conversation_history

        response = client.chat.completions.create(
            model=model,
            messages=api_messages,
        )

        ai_response = response.choices[0].message.content

        # Add the AI's response to the conversation history
        conversation_history.append({"role": "assistant", "content": ai_response})

        # Keep only the most recent messages in the conversation history
        conversation_history = conversation_history[-10:]

        # Send the AI's response back to the user
        bot.reply_to(message, ai_response)

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()