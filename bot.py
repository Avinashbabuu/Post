import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8013649463:AAFL18RrQ7PiVKA-kcFznIilIVzhsNoBEDA"
OWNER_ID = 6484788124  # Apna Telegram ID yaha dale
bot = telebot.TeleBot(TOKEN)

# Dictionary to store user channels and cloned bots
user_channels = {}
cloned_bots = {}
user_posts = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📢 Set Channel", "📝 Create Post")
    markup.add("🛠 Clone Bot", "📖 Help")
    markup.add("📡 Broadcast")
    bot.send_message(
        message.chat.id,
        "👋 Welcome! Yeh bot aapke channel ke liye posts manage karega.\n\nUse the buttons below to navigate.",
        reply_markup=markup
    )

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(
        message.chat.id,
        "Commands:\n📢 Set Channel - Channel set kare\n📝 Create Post - Naya post banaye\n🛠 Clone Bot - Bot clone kare\n📡 Broadcast - Sabke channels me message bheje"
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
    user_posts[message.chat.id] = {"text": "", "photo": "", "buttons": []}
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        caption = message.caption if message.caption else ""
        user_posts[message.chat.id]["photo"] = file_id
        user_posts[message.chat.id]["text"] = caption
    elif message.content_type == 'text':
        user_posts[message.chat.id]["text"] = message.text
    else:
        bot.send_message(message.chat.id, "⚠️ Sirf text ya image bheje.")
        return
    bot.send_message(message.chat.id, "➕ Inline button add karna hai? /addbutton use kare")

@bot.message_handler(commands=['addbutton'])
def add_inline_button(message):
    bot.send_message(message.chat.id, "🔘 Button ka text bheje")
    bot.register_next_step_handler(message, get_button_text)

def get_button_text(message):
    button_text = message.text
    bot.send_message(message.chat.id, "🔗 Button ka link bheje")
    bot.register_next_step_handler(message, lambda msg: save_button(msg, button_text))

def save_button(message, button_text):
    button_url = message.text
    user_posts[message.chat.id]["buttons"].append((button_text, button_url))
    bot.send_message(message.chat.id, "✅ Button add ho gaya! /addbutton use kare aur add karne ke liye ya /sendpost use kare post bhejne ke liye")

@bot.message_handler(commands=['sendpost'])
def send_post(message):
    if message.chat.id not in user_posts:
        bot.send_message(message.chat.id, "⚠️ Pehle post banaye! /createpost")
        return
    post = user_posts[message.chat.id]
    markup = InlineKeyboardMarkup()
    for text, url in post["buttons"]:
        markup.add(InlineKeyboardButton(text, url=url))
    if post["photo"]:
        bot.send_photo(user_channels[message.chat.id], post["photo"], caption=post["text"], reply_markup=markup)
    else:
        bot.send_message(user_channels[message.chat.id], post["text"], reply_markup=markup)
    bot.send_message(message.chat.id, "✅ Post bhej diya gaya hai!")

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
