import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

# Load token securely from environment variables
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Bot token is missing! Set it as an environment variable.")

bot = telebot.TeleBot(TOKEN)

# Define admin IDs as a list for multiple admins support
ADMIN_IDS = [6484788124]  # Add more IDs if needed

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "✨ **ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ᴘᴏsᴛɪɴɢ ʙᴏᴛ!** 🚀\n\n"
    welcome_text += "📢 **ᴇꜰꜰᴏʀᴛʟᴇss ᴄʜᴀɴɴᴇʟ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ & ᴘᴏsᴛ ᴄʀᴇᴀᴛɪᴏɴ!**\n"
    welcome_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    welcome_text += "🔹 **/createpost** – ✍️ *Create & send engaging posts!*\n"
    welcome_text += "🔹 **/setchannel** – 📌 *Select the channel for posting!*\n"
    welcome_text += "🔹 **/removechannel** – ❌ *Delete any added channel!*\n"
    welcome_text += "🔹 **/help** – 📖 *Get a full guide on bot usage!*\n"
    welcome_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    welcome_text += "🔥 **Experience the fastest posting bot ever!** 🔥"

    # Create a keyboard with bottom buttons
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📢 Create Post"), KeyboardButton("📌 Set Channel"))
    markup.add(KeyboardButton("❌ Remove Channel"), KeyboardButton("📖 Help"))

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "📖 **Bot Usage Guide**:
"
    help_text += "/start - Start the bot
"
    help_text += "/createpost - Create and send posts
"
    help_text += "/setchannel - Set a posting channel
"
    help_text += "/removechannel - Remove a channel
"
    help_text += "/help - Get this help message
"
    bot.send_message(message.chat.id, help_text)

# Error handling
@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.send_message(message.chat.id, "❌ Unknown command! Type /help for available commands.")

# Start bot polling with error handling
if __name__ == "__main__":
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        print(f"Error: {e}")
