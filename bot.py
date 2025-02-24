import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8013649463:AAEos0rQfQS6S-6QDpLRPgxTtF7IT2_cQrY"
OWNER_ID = 6484788124  # Apna Telegram ID yaha dale
bot = telebot.TeleBot(TOKEN)

# Dictionary to store user channels and cloned bots
user_channels = {}
cloned_bots = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📢 Set Channel", "📝 Create Post")
    markup.add("🛠 Clone Bot", "📖 Help")
    bot.send_message(
        message.chat.id,
        "👋 Welcome! Yeh bot aapke channel ke liye posts manage karega.\n\nUse the buttons below to navigate.",
        reply_markup=markup
    )

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(
        message.chat.id,
        "Commands:\n📢 Set Channel - Channel set kare\n📝 Create Post - Naya post banaye\n🛠 Clone Bot - Bot clone kare\n📢 Broadcast - Sabke channels me message bheje"
    )

@bot.message_handler(func=lambda message: message.text == "📢 Set Channel")
def set_channel(message):
    bot.send_message(message.chat.id, "Apne channel ka username ya ID bheje (e.g. @MyChannel)")
    bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    user_channels[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"✅ Channel set ho gaya: {message.text}")

@bot.message_handler(func=lambda message: message.text == "📝 Create Post")
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

@bot.message_handler(func=lambda message: message.text == "🛠 Clone Bot")
def clone_bot(message):
    bot.send_message(message.chat.id, "🛠 Apne naye bot ka token bheje.")
    bot.register_next_step_handler(message, process_clone)

def process_clone(message):
    bot_token = message.text
    cloned_bots[message.chat.id] = bot_token
    bot.send_message(message.chat.id, f"✅ Bot cloned successfully with token: {bot_token}")

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.chat.id == OWNER_ID:
        bot.send_message(message.chat.id, "✉️ Broadcast message likhe:")
        bot.register_next_step_handler(message, send_broadcast)
    else:
        bot.send_message(message.chat.id, "❌ Aapko is command ki permission nahi hai.")

def send_broadcast(message):
    for user_id, channel in user_channels.items():
        bot.send_message(channel, message.text)
    bot.send_message(message.chat.id, "✅ Broadcast sent successfully!")

bot.polling(none_stop=True)
