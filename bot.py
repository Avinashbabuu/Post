import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8013649463:AAFAqEoo5FjzWLWjpwHfU9OmrrDzQrVSkMM"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID

# Store user posts temporarily
user_posts = {}
selected_channel = {}
added_channels = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "👋 Welcome to the bot! Here are the available features:\n\n"
    welcome_text += "✅ *Create Post* - Make & send posts.\n"
    welcome_text += "✅ *Set Channel* - Set a target channel for posting.\n"
    welcome_text += "✅ *Remove Channel* - Remove a channel from the list.\n"
    welcome_text += "✅ *Broadcast* - (Admin only) Send messages to all users.\n"
    welcome_text += "✅ *Help* - Get a full guide."
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Create Post"), KeyboardButton("Help"))
    markup.add(KeyboardButton("Set Channel"), KeyboardButton("Remove Channel"))
    if message.chat.id == admin_id:
        markup.add(KeyboardButton("Broadcast"))
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "📌 *Bot Guide* 📌\n\n"
    help_text += "1️⃣ *Create Post* - Make a new post with image & text.\n"
    help_text += "2️⃣ *Add Inline Button* - Attach buttons to the post with links.\n"
    help_text += "3️⃣ *Send Post* - Choose a channel and send the post.\n"
    help_text += "4️⃣ *Set Channel* - Choose a channel to send posts.\n"
    help_text += "5️⃣ *Remove Channel* - Remove a selected channel.\n"
    help_text += "6️⃣ *Broadcast* - (Admin only) Send a message to all users.\n"
    
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "Set Channel")
def set_channel(message):
    bot.send_message(message.chat.id, "Send me the channel username or ID.")
    bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    added_channels.append(message.text)
    bot.send_message(message.chat.id, f"✅ Channel added: {message.text}")

@bot.message_handler(func=lambda message: message.text == "Remove Channel")
def remove_channel(message):
    if not added_channels:
        bot.send_message(message.chat.id, "No channels to remove.")
        return
    
    channel_list = "\n".join([f"{i+1}. {ch}" for i, ch in enumerate(added_channels)])
    bot.send_message(message.chat.id, f"Current channels:\n{channel_list}\n\nSend the number of the channel to remove.")
    bot.register_next_step_handler(message, delete_channel)

def delete_channel(message):
    try:
        index = int(message.text) - 1
        removed = added_channels.pop(index)
        bot.send_message(message.chat.id, f"✅ Removed channel: {removed}")
    except:
        bot.send_message(message.chat.id, "Invalid selection.")

@bot.message_handler(func=lambda message: message.text == "Create Post")
def create_post(message):
    bot.send_message(message.chat.id, "Send me the text of the post.")
    bot.register_next_step_handler(message, save_post)

def save_post(message):
    user_posts[message.chat.id] = {"text": message.text, "buttons": []}
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Add Inline Button"), KeyboardButton("Send Post"), KeyboardButton("Cancel"))
    bot.send_message(message.chat.id, f"Preview:\n{message.text}", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Add Inline Button")
def add_button(message):
    bot.send_message(message.chat.id, "Send me the button text.")
    bot.register_next_step_handler(message, save_button_text)

def save_button_text(message):
    button_text = message.text
    bot.send_message(message.chat.id, "Send me the button URL.")
    bot.register_next_step_handler(message, lambda msg: save_button_link(msg, button_text))

def save_button_link(message, button_text):
    if message.chat.id in user_posts:
        user_posts[message.chat.id]["buttons"].append((button_text, message.text))
        bot.send_message(message.chat.id, f"Button '{button_text}' added! Preview:")
        send_post_preview(message.chat.id)
    else:
        bot.send_message(message.chat.id, "No active post found.")

def send_post_preview(chat_id):
    post = user_posts.get(chat_id, {})
    text = post.get("text", "")
    buttons = post.get("buttons", [])
    
    markup = InlineKeyboardMarkup()
    for btn in buttons:
        markup.add(InlineKeyboardButton(btn[0], url=btn[1]))
    
    bot.send_message(chat_id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Send Post")
def send_post(message):
    if not added_channels:
        bot.send_message(message.chat.id, "No channels available. Set a channel first.")
        return
    
    markup = InlineKeyboardMarkup()
    for ch in added_channels:
        markup.add(InlineKeyboardButton(ch, callback_data=f"send_to:{ch}"))
    markup.add(InlineKeyboardButton("Send to All", callback_data="send_to:all"))
    
    bot.send_message(message.chat.id, "Choose where to send the post:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("send_to:"))
def confirm_send(call):
    target = call.data.split(":")[1]
    post = user_posts.get(call.message.chat.id, {})
    text = post.get("text", "")
    buttons = post.get("buttons", [])
    
    markup = InlineKeyboardMarkup()
    for btn in buttons:
        markup.add(InlineKeyboardButton(btn[0], url=btn[1]))
    
    if target == "all":
        for ch in added_channels:
            bot.send_message(ch, text, reply_markup=markup)
    else:
        bot.send_message(target, text, reply_markup=markup)
    
    bot.send_message(call.message.chat.id, "✅ Post sent! Returning to home.")
    send_welcome(call.message)

bot.polling(none_stop=True)
