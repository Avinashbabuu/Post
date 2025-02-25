import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8013649463:AAFAqEoo5FjzWLWjpwHfU9OmrrDzQrVSkMM"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID

# Store user posts temporarily
user_posts = {}
selected_channels = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "👋 Welcome to the bot! Here are the available features:\n\n"
    welcome_text += "✅ *Create Post* - Make & send posts.\n"
    welcome_text += "✅ *Set Channel* - Set a target channel for posting.\n"
    welcome_text += "✅ *Remove Channel* - Remove a linked channel.\n"
    welcome_text += "✅ *Broadcast* - Send messages to all users (Admin only).\n"
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
    help_text += "3️⃣ *Send Post* - Choose channels to send your post.\n"
    help_text += "4️⃣ *Set Channel* - Choose a channel to send posts.\n"
    help_text += "5️⃣ *Remove Channel* - Remove linked channels.\n"
    help_text += "6️⃣ *Broadcast* - Send a message to all users (Admin only)."
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "Set Channel")
def set_channel(message):
    bot.send_message(message.chat.id, "Send me the channel username or ID.")
    bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    selected_channels.append(message.text)
    bot.send_message(message.chat.id, f"✅ Channel added: {message.text}")

@bot.message_handler(func=lambda message: message.text == "Remove Channel")
def remove_channel(message):
    if not selected_channels:
        bot.send_message(message.chat.id, "No channels added.")
        return
    
    text = "Select a channel to remove:\n"
    buttons = []
    for index, channel in enumerate(selected_channels, start=1):
        text += f"{index}. {channel}\n"
        buttons.append(InlineKeyboardButton(channel, callback_data=f"remove_{index-1}"))
    
    markup = InlineKeyboardMarkup()
    markup.add(*buttons)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_"))
def handle_remove_channel(call):
    index = int(call.data.split("_")[1])
    removed_channel = selected_channels.pop(index)
    bot.answer_callback_query(call.id, f"Removed {removed_channel}")
    bot.send_message(call.message.chat.id, f"❌ Removed channel: {removed_channel}")

@bot.message_handler(func=lambda message: message.text == "Create Post")
def create_post(message):
    bot.send_message(message.chat.id, "Send me the text of the post.")
    bot.register_next_step_handler(message, save_post)

def save_post(message):
    user_posts[message.chat.id] = {"text": message.text, "buttons": []}
    show_post_preview(message.chat.id)

def show_post_preview(chat_id):
    post = user_posts.get(chat_id)
    if not post:
        return
    
    text = f"📢 *Post Preview:*\n{post['text']}"
    buttons = [InlineKeyboardButton("Add Inline Button", callback_data="add_button"),
               InlineKeyboardButton("Send Post", callback_data="send_post"),
               InlineKeyboardButton("Cancel", callback_data="cancel_post")]
    
    markup = InlineKeyboardMarkup()
    markup.add(*buttons)
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "add_button")
def add_button(call):
    bot.send_message(call.message.chat.id, "Send me the button text.")
    bot.register_next_step_handler(call.message, save_button)

def save_button(message):
    if message.chat.id in user_posts:
        user_posts[message.chat.id]["buttons"].append(message.text)
        show_post_preview(message.chat.id)
    else:
        bot.send_message(message.chat.id, "No active post found.")

@bot.callback_query_handler(func=lambda call: call.data == "send_post")
def send_post(call):
    chat_id = call.message.chat.id
    if chat_id not in user_posts:
        bot.send_message(chat_id, "No active post found.")
        return
    
    if not selected_channels:
        bot.send_message(chat_id, "No channels added. Use 'Set Channel' to add one.")
        return
    
    text = "Select the channel to send the post:\n"
    buttons = [InlineKeyboardButton(channel, callback_data=f"sendto_{channel}") for channel in selected_channels]
    buttons.append(InlineKeyboardButton("All", callback_data="sendto_all"))
    markup = InlineKeyboardMarkup()
    markup.add(*buttons)
    bot.send_message(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("sendto_"))
def handle_send_to_channel(call):
    chat_id = call.message.chat.id
    if chat_id not in user_posts:
        return
    
    post = user_posts[chat_id]
    target = call.data.split("sendto_")[1]
    
    if target == "all":
        for channel in selected_channels:
            bot.send_message(channel, post["text"])
    else:
        bot.send_message(target, post["text"])
    
    bot.send_message(chat_id, "✅ Post sent successfully!")
    send_welcome(call.message)

@bot.message_handler(func=lambda message: message.text == "Broadcast" and message.chat.id == admin_id)
def broadcast_message(message):
    bot.send_message(message.chat.id, "Send me the message you want to broadcast.")
    bot.register_next_step_handler(message, send_broadcast)

def send_broadcast(message):
    bot.send_message(admin_id, f"Broadcast sent: {message.text}")
    # Implement broadcast logic here

bot.polling(none_stop=True)
