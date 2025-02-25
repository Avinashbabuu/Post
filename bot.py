import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8013649463:AAFAqEoo5FjzWLWjpwHfU9OmrrDzQrVSkMM"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID

# Store user posts temporarily
user_posts = {}
selected_channel = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "👋 Welcome to the bot! Here are the available features:\n\n"
    welcome_text += "✅ *Create Post* - Make & send posts.\n"
    welcome_text += "✅ *Set Channel* - Set a target channel for posting.\n"
    welcome_text += "✅ *Remove Channel* - Unlink the selected channel.\n"
    welcome_text += "✅ *Broadcast* - Send messages to all users (Admin Only).\n"
    welcome_text += "✅ *Help* - Get a full guide."
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Create Post"), KeyboardButton("Help"))
    markup.add(KeyboardButton("Set Channel"), KeyboardButton("Remove Channel"))
    markup.add(KeyboardButton("Broadcast"))
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "📌 *Bot Guide* 📌\n\n"
    help_text += "1️⃣ *Create Post* - Make a new post with image & text.\n"
    help_text += "2️⃣ *Add Inline Button* - Attach buttons to the post.\n"
    help_text += "3️⃣ *Send Post* - Post it in your channel.\n"
    help_text += "4️⃣ *Set Channel* - Choose a channel to send posts.\n"
    help_text += "5️⃣ *Remove Channel* - Unlink the selected channel.\n"
    help_text += "6️⃣ *Broadcast* - Send a message to all users (Admin Only)."
    
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
        bot.send_message(message.chat.id, "❌ Channel removed successfully.")
    else:
        bot.send_message(message.chat.id, "⚠️ No channel is set.")

@bot.message_handler(func=lambda message: message.text == "Create Post")
def create_post(message):
    bot.send_message(message.chat.id, "Send me the text of the post.")
    bot.register_next_step_handler(message, save_post)

def save_post(message):
    user_posts[message.chat.id] = {"text": message.text, "buttons": []}
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Add Inline Button"), KeyboardButton("Send Post"))
    bot.send_message(message.chat.id, "Post saved. Add a button or send the post.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Add Inline Button")
def add_button(message):
    bot.send_message(message.chat.id, "Send me the button text and URL (Format: Text - URL)")
    bot.register_next_step_handler(message, save_button)

def save_button(message):
    if message.chat.id in user_posts:
        try:
            text, url = message.text.split(" - ")
            user_posts[message.chat.id]["buttons"].append((text, url))
            bot.send_message(message.chat.id, f"✅ Button '{text}' added!")
        except ValueError:
            bot.send_message(message.chat.id, "⚠️ Invalid format. Use: Text - URL")
    else:
        bot.send_message(message.chat.id, "⚠️ No active post found.")

@bot.message_handler(func=lambda message: message.text == "Send Post")
def send_post(message):
    if message.chat.id in user_posts:
        post = user_posts[message.chat.id]
        markup = InlineKeyboardMarkup()
        for text, url in post["buttons"]:
            markup.add(InlineKeyboardButton(text, url=url))
        
        bot.send_message(message.chat.id, post['text'], reply_markup=markup)
        if message.chat.id in selected_channel:
            bot.send_message(selected_channel[message.chat.id], post['text'], reply_markup=markup)
        del user_posts[message.chat.id]
        send_welcome(message)  # Redirect to home
    else:
        bot.send_message(message.chat.id, "⚠️ No active post found.")

@bot.message_handler(func=lambda message: message.text == "Broadcast")
def broadcast_message(message):
    if message.chat.id == admin_id:
        bot.send_message(message.chat.id, "Send me the message you want to broadcast.")
        bot.register_next_step_handler(message, send_broadcast)
    else:
        bot.send_message(message.chat.id, "❌ You are not authorized to use this command.")

def send_broadcast(message):
    bot.send_message(admin_id, f"📢 Broadcast sent: {message.text}")
    # Implement actual broadcast logic here

bot.polling(none_stop=True)
