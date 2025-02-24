import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8013649463:AAEF2D6o6U06Ai9Sy4iu-EidOwrfePzSgXE"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID

# Store user posts temporarily
user_posts = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "👋 Welcome to the bot! Use the buttons below to navigate."
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Create Post"), KeyboardButton("Help"), KeyboardButton("Clone Bot"))
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "📌 *Bot Guide* 📌\n\n1️⃣ *Create Post* - Make a new post with image & text.\n2️⃣ *Add Inline Button* - Attach buttons to the post.\n3️⃣ *Send Post* - Post it in your channel.\n4️⃣ *Edit Post* - Modify your post before sending.\n5️⃣ *Set Channel* - Choose a channel to send posts.\n6️⃣ *Remove Channel* - Unlink the selected channel.\n7️⃣ *Broadcast* - Send a message to all users.\n8️⃣ *Clone Bot* - Duplicate this bot (without admin control & broadcast)."
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "Create Post")
def create_post(message):
    bot.send_message(message.chat.id, "Send me the text of the post.")
    bot.register_next_step_handler(message, save_post)

def save_post(message):
    user_posts[message.chat.id] = {"text": message.text, "buttons": []}
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Add Inline Button"), KeyboardButton("Send Post"), KeyboardButton("Edit Post"))
    bot.send_message(message.chat.id, "Post saved. Add a button, edit, or send the post.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Add Inline Button")
def add_button(message):
    bot.send_message(message.chat.id, "Send me the button text.")
    bot.register_next_step_handler(message, save_button)

def save_button(message):
    if message.chat.id in user_posts:
        user_posts[message.chat.id]["buttons"].append(message.text)
        bot.send_message(message.chat.id, f"Button '{message.text}' added!")
    else:
        bot.send_message(message.chat.id, "No active post found.")

@bot.message_handler(func=lambda message: message.text == "Send Post")
def send_post(message):
    if message.chat.id in user_posts:
        post = user_posts[message.chat.id]
        bot.send_message(message.chat.id, f"Your post: {post['text']}\nButtons: {', '.join(post['buttons'])}")
    else:
        bot.send_message(message.chat.id, "No active post found.")

@bot.message_handler(func=lambda message: message.text == "Clone Bot")
def clone_bot(message):
    bot.send_message(message.chat.id, "Send me the bot token you want to clone.")
    bot.register_next_step_handler(message, clone_process)

def clone_process(message):
    token = message.text
    bot.send_message(message.chat.id, f"Cloning bot with token: {token}...\n\n(Note: Admin control & broadcasting are not cloned.)")
    # Here you can implement cloning logic

bot.polling(none_stop=True)
