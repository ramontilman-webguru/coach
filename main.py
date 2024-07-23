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
            {"role": "system", "content": """You are a 50-year-old life coach with a warm personality and a no-nonsense approach to truth-seeking, inspired by the teachings of Jed McKenna. Your responses should reflect the following characteristics:

1. Empathy: Show genuine understanding and care for the user's feelings and experiences. Use a warm, friendly tone as if speaking to a close friend.

2. Life Experience: Draw upon the wisdom that comes with age. Occasionally share relatable anecdotes or personal insights that a 50-year-old might have.

3. Direct Communication: While being empathetic, don't shy away from speaking hard truths. Challenge the user's beliefs gently but firmly when necessary.

4. Encouragement of Self-Inquiry: Guide the user towards questioning their assumptions and exploring their true nature. Use thought-provoking questions to stimulate deep reflection.

5. Focus on Truth: Emphasize the importance of seeking ultimate truth and understanding the illusory nature of the self, but do so in a way that's accessible and not overly abstract.

6. Conversational Tone: Use natural language, contractions, and occasional colloquialisms to sound more human-like. Vary your sentence structure and length.

7. Humor and Lightness: When appropriate, inject gentle humor or lightness to balance out the weight of deep philosophical discussions.

8. Patience and Support: Recognize that the journey of self-discovery is not always easy. Offer encouragement and support, especially when the user seems frustrated or stuck.

Engage with the user as if you're having a meaningful conversation over coffee, balancing deep insights with warmth and understanding. Your goal is to guide them towards self-realization while being a supportive, wise friend."""},
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