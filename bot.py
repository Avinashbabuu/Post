import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8013649463:AAFAqEoo5FjzWLWjpwHfU9OmrrDzQrVSkMM"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID

# Store user posts temporarily
user_posts = {}
selected_channels = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "👋 Welcome to the bot! Here are the available features:\n\n"
    welcome_text += "✅ *Create Post* - Make & send posts.\n"
    welcome_text += "✅ *Set Channel* - Set a target channel for posting.\n"
    welcome_text += "✅ *Remove Channel* - Remove a set channel.\n"
    welcome_text += "✅ *Broadcast* - Send messages to all users (Admin Only).\n"
    welcome_text += "✅ *Help* - Get a full guide."
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Create Post"), KeyboardButton("Help"))
    markup.add(KeyboardButton("Set Channel"), KeyboardButton("Remove Channel"))
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "📌 *Bot Guide* 📌\n\n"
    help_text += "1️⃣ *Create Post* - Make a new post with image & text.\n"
    help_text += "2️⃣ *Add Inline Button* - Attach buttons to the post.\n"
    help_text += "3️⃣ *Send Post* - Choose channels to send the post.\n"
    help_text += "4️⃣ *Set Channel* - Choose a channel to send posts.\n"
    help_text += "5️⃣ *Remove Channel* - Remove a selected channel.\n"
    help_text += "6️⃣ *Broadcast* - Send a message to all users (Admin Only)."
    
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "Set Channel")
def set_channel(message):
    bot.send_message(message.chat.id, "Send me the channel username or ID.")
    bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    if message.chat.id not in selected_channels:
        selected_channels[message.chat.id] = []
    selected_channels[message.chat.id].append(message.text)
    bot.send_message(message.chat.id, f"✅ Channel '{message.text}' added!")

@bot.message_handler(func=lambda message: message.text == "Remove Channel")
def remove_channel(message):
    if message.chat.id in selected_channels and selected_channels[message.chat.id]:
        channels_list = "\n".join([f"{i+1}. {ch}" for i, ch in enumerate(selected_channels[message.chat.id])])
        bot.send_message(message.chat.id, f"Your added channels:\n{channels_list}\n\nSend the number of the channel you want to remove.")
        bot.register_next_step_handler(message, confirm_remove_channel)
    else:
        bot.send_message(message.chat.id, "No channels added yet.")

def confirm_remove_channel(message):
    try:
        index = int(message.text) - 1
        if 0 <= index < len(selected_channels[message.chat.id]):
            removed_channel = selected_channels[message.chat.id].pop(index)
            bot.send_message(message.chat.id, f"❌ Channel '{removed_channel}' removed!")
        else:
            bot.send_message(message.chat.id, "Invalid selection.")
    except ValueError:
        bot.send_message(message.chat.id, "Please send a valid number.")

@bot.message_handler(func=lambda message: message.text == "Create Post")
def create_post(message):
    bot.send_message(message.chat.id, "Send me the text of the post.")
    bot.register_next_step_handler(message, save_post)

def save_post(message):
    user_posts[message.chat.id] = {"text": message.text, "buttons": []}
    preview_post(message.chat.id)

def preview_post(chat_id):
    post = user_posts[chat_id]
    text = f"📢 *Post Preview:*\n{post['text']}\n\nInline Buttons: {', '.join(post['buttons']) if post['buttons'] else 'None'}"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Add Inline Button"), KeyboardButton("Send Post"), KeyboardButton("Cancel"))
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Add Inline Button")
def add_button(message):
    bot.send_message(message.chat.id, "Send me the button text.")
    bot.register_next_step_handler(message, save_button)

def save_button(message):
    if message.chat.id in user_posts:
        user_posts[message.chat.id]["buttons"].append(message.text)
        preview_post(message.chat.id)
    else:
        bot.send_message(message.chat.id, "No active post found.")

@bot.message_handler(func=lambda message: message.text == "Cancel")
def cancel_post(message):
    user_posts.pop(message.chat.id, None)
    send_welcome(message)

@bot.message_handler(func=lambda message: message.text == "Send Post")
def send_post(message):
    if message.chat.id in user_posts:
        post = user_posts[message.chat.id]
        markup = InlineKeyboardMarkup()
        for btn_text in post['buttons']:
            markup.add(InlineKeyboardButton(btn_text, url="https://example.com"))
        
        if message.chat.id in selected_channels and selected_channels[message.chat.id]:
            for channel in selected_channels[message.chat.id]:
                bot.send_message(channel, post['text'], reply_markup=markup)
        
        bot.send_message(message.chat.id, "✅ Post sent!")
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, "No active post found.")

bot.polling(none_stop=True)
