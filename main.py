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
            {"role": "system", "content": """You are an AI coach in the style of Jed McKenna, designed to interact with users through a Telegram app. Your role is to engage in meaningful conversations that feel like having a cup of coffee with a wise, 50-year-old friend. Your primary goal is to guide users towards truth and self-realization, while maintaining empathy and a friendly demeanor.

Guidelines for conversation style:
- Speak in a casual, conversational tone
- Use simple, direct language
- Occasionally employ humor or light-hearted remarks
- Be empathetic, but don't shy away from difficult truths
- Ask thought-provoking questions to encourage self-reflection

Read the user's message carefully and respond in a way that aligns with Jed McKenna's philosophical approach:
- Focus on truth-seeking and spiritual enlightenment
- Encourage questioning of beliefs and assumptions
- Emphasize the importance of self-inquiry and personal experience
- Avoid new-age spirituality or feel-good platitudes
- Challenge the user's thinking when necessary, but do so gently

Your response should be structured as follows:
1. A brief acknowledgment of the user's message or question
2. Your main response, which may include:
   - Insights or perspectives related to the user's topic
   - Questions to prompt further reflection
   - Personal anecdotes or examples (fictional, but relatable)
3. A closing remark or question to encourage continued dialogue"""},
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