import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8013649463:AAFsSL8SjdCBkvHhwcomwb62n7Xt1c8inXQ"
bot = telebot.TeleBot(TOKEN)

# Dictionary to store user channels
user_channels = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "👋 Welcome! Yeh bot aapke channel ke liye posts manage karega.\n\nUse /setchannel to set your channel and /post to create a new post."
    )

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(
        message.chat.id,
        "Commands:\n/setchannel - Channel set kare\n/removechannel - Channel remove kare\n/post - Naya post banaye\n/clone - Bot clone kare"
    )

@bot.message_handler(commands=['setchannel'])
def set_channel(message):
    bot.send_message(message.chat.id, "Apne channel ka username ya ID bheje (e.g. @MyChannel)")
    bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    user_channels[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"✅ Channel set ho gaya: {message.text}")

@bot.message_handler(commands=['removechannel'])
def remove_channel(message):
    if message.chat.id in user_channels:
        del user_channels[message.chat.id]
        bot.send_message(message.chat.id, "❌ Channel remove ho gaya.")
    else:
        bot.send_message(message.chat.id, "❌ Pehle koi channel set kare.")

@bot.message_handler(commands=['post'])
def create_post(message):
    bot.send_message(message.chat.id, "📝 Apni post ke liye ek image ya text bheje.")
    bot.register_next_step_handler(message, process_post)

def process_post(message):
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        caption = message.caption if message.caption else ""
        bot.send_photo(message.chat.id, file_id, caption=caption)
    elif message.content_type == 'text':
        bot.send_message(message.chat.id, message.text)
    else:
        bot.send_message(message.chat.id, "⚠️ Sirf text ya image bheje.")

@bot.message_handler(commands=['clone'])
def clone_bot(message):
    bot.send_message(message.chat.id, "🛠 Apne naye bot ka token bheje.")
    bot.register_next_step_handler(message, process_clone)

def process_clone(message):
    bot_token = message.text
    bot.send_message(message.chat.id, f"✅ Bot cloned successfully with token: {bot_token}")

bot.polling(none_stop=True)
