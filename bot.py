import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8013649463:AAHJHS-KKCZrNP3VaSibuV_qp8sMd7kgf5E"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID

# Store user posts temporarily
user_posts = {}
selected_channel = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "👋 *Welcome to the bot!* \n\n🚀 *Features:*\n"
    welcome_text += "1️⃣ *Create Post* - Make & send posts.\n"
    welcome_text += "2️⃣ *Set/Remove Channel* - Manage your target channel.\n"
    welcome_text += "3️⃣ *Broadcast* - Send messages to all channels.\n"
    welcome_text += "4️⃣ *Clone Bot* - Create your own version of this bot.\n"
    welcome_text += "5️⃣ *Help* - Get a step-by-step guide."
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Create Post"), KeyboardButton("Help"))
    markup.add(KeyboardButton("Set Channel"), KeyboardButton("Remove Channel"))
    markup.add(KeyboardButton("Broadcast"), KeyboardButton("Clone Bot"))
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "📌 *Bot Guide:*\n\n"
    help_text += "🔹 *Create Post* - Create a post with text & images.\n"
    help_text += "🔹 *Add Inline Button* - Attach buttons to your post.\n"
    help_text += "🔹 *Send Post* - Post it in your selected channel.\n"
    help_text += "🔹 *Edit Post* - Modify your post before sending.\n"
    help_text += "🔹 *Set Channel* - Choose a channel for posting.\n"
    help_text += "🔹 *Remove Channel* - Unlink the selected channel.\n"
    help_text += "🔹 *Broadcast* - Send messages to all channels.\n"
    help_text += "🔹 *Clone Bot* - Duplicate this bot (without admin control & broadcast).\n"
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "Set Channel")
def set_channel(message):
    bot.send_message(message.chat.id, "Send me the channel username or ID.")
    bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    selected_channel[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"✅ Channel set to: {message.text}")

@bot.message_handler(func=lambda message: message.text == "Remove Channel")
def remove_channel(message):
    if message.chat.id in selected_channel:
        del selected_channel[message.chat.id]
        bot.send_message(message.chat.id, "❌ Channel removed.")
    else:
        bot.send_message(message.chat.id, "⚠️ No channel is set.")

@bot.message_handler(func=lambda message: message.text == "Create Post")
def create_post(message):
    bot.send_message(message.chat.id, "Send me the text of the post.")
    bot.register_next_step_handler(message, save_post)

def save_post(message):
    user_posts[message.chat.id] = {"text": message.text, "buttons": []}
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Add Inline Button"), KeyboardButton("Send Post"), KeyboardButton("Edit Post"))
    bot.send_message(message.chat.id, "Post saved. You can add a button, edit, or send the post.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Add Inline Button")
def add_button(message):
    bot.send_message(message.chat.id, "Send me the button text.")
    bot.register_next_step_handler(message, save_button)

def save_button(message):
    if message.chat.id in user_posts:
        user_posts[message.chat.id]["buttons"].append(message.text)
        bot.send_message(message.chat.id, f"✅ Button '{message.text}' added!")
    else:
        bot.send_message(message.chat.id, "⚠️ No active post found.")

@bot.message_handler(func=lambda message: message.text == "Send Post")
def send_post(message):
    if message.chat.id in user_posts:
        post = user_posts[message.chat.id]
        bot.send_message(message.chat.id, f"📢 *Your Post:*\n{post['text']}\n🔘 Buttons: {', '.join(post['buttons'])}", parse_mode="Markdown")
        if message.chat.id in selected_channel:
            bot.send_message(selected_channel[message.chat.id], post['text'])
    else:
        bot.send_message(message.chat.id, "⚠️ No active post found.")

@bot.message_handler(func=lambda message: message.text == "Clone Bot")
def clone_bot(message):
    bot.send_message(message.chat.id, "🛠 *Clone Guide:*\n1. Send your bot token.\n2. Bot will be cloned with posting features.\n3. No admin control or broadcasting.", parse_mode="Markdown")
    bot.register_next_step_handler(message, clone_process)

def clone_process(message):
    token = message.text
    bot.send_message(message.chat.id, f"🔄 Cloning bot with token: {token}...\n\n(Note: Admin control & broadcasting are not cloned.)")
    # Implement cloning logic here

@bot.message_handler(func=lambda message: message.text == "Broadcast")
def broadcast_message(message):
    bot.send_message(message.chat.id, "📢 Send me the message you want to broadcast.")
    bot.register_next_step_handler(message, send_broadcast)

def send_broadcast(message):
    bot.send_message(admin_id, f"🚀 Broadcast sent: {message.text}")
    # Implement broadcast logic here

bot.polling(none_stop=True)
