import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8013649463:AAFAqEoo5FjzWLWjpwHfU9OmrrDzQrVSkMM"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID

# Store user posts temporarily
user_posts = {}
selected_channel = {}
channels = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "\U0001F44B Welcome to the bot! Here are the available features:\n\n"
    welcome_text += "✅ *Create Post* - Make & send posts.\n"
    welcome_text += "✅ *Set Channel* - Set a target channel for posting.\n"
    welcome_text += "✅ *Remove Channel* - Unlink a selected channel.\n"
    welcome_text += "✅ *Broadcast* - Admins can send messages to all users.\n"
    welcome_text += "✅ *Help* - Get a full guide."
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Create Post"), KeyboardButton("Help"))
    markup.add(KeyboardButton("Set Channel"), KeyboardButton("Remove Channel"))
    markup.add(KeyboardButton("Broadcast"))
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "\U0001F4CC *Bot Guide* \U0001F4CC\n\n"
    help_text += "1️⃣ *Create Post* - Make a new post with image & text.\n"
    help_text += "2️⃣ *Add Inline Button* - Attach buttons with text and links.\n"
    help_text += "3️⃣ *Send Post* - Select channels to post your message.\n"
    help_text += "4️⃣ *Set Channel* - Choose a channel for posting.\n"
    help_text += "5️⃣ *Remove Channel* - Remove unwanted channels from the list.\n"
    help_text += "6️⃣ *Broadcast* - Admins can send messages to all users."
    
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "Set Channel")
def set_channel(message):
    bot.send_message(message.chat.id, "Send me the channel username or ID.")
    bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    channels.append(message.text)
    bot.send_message(message.chat.id, f"✅ Channel added: {message.text}")

@bot.message_handler(func=lambda message: message.text == "Remove Channel")
def remove_channel(message):
    if not channels:
        bot.send_message(message.chat.id, "No channels are set.")
        return
    
    text = "Select the number of the channel to remove:\n"
    for i, channel in enumerate(channels, 1):
        text += f"{i}. {channel}\n"
    
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, confirm_remove_channel)

def confirm_remove_channel(message):
    try:
        index = int(message.text) - 1
        removed_channel = channels.pop(index)
        bot.send_message(message.chat.id, f"✅ Removed channel: {removed_channel}")
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
    bot.send_message(message.chat.id, "Post saved. Add a button, send, or cancel.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Add Inline Button")
def add_button(message):
    bot.send_message(message.chat.id, "Send me the button text.")
    bot.register_next_step_handler(message, save_button_text)

def save_button_text(message):
    button_text = message.text
    bot.send_message(message.chat.id, "Send me the button link.")
    bot.register_next_step_handler(message, lambda msg: save_button_link(msg, button_text))

def save_button_link(message, button_text):
    if message.chat.id in user_posts:
        user_posts[message.chat.id]["buttons"].append((button_text, message.text))
        bot.send_message(message.chat.id, f"Button '{button_text}' added!")
    else:
        bot.send_message(message.chat.id, "No active post found.")

@bot.message_handler(func=lambda message: message.text == "Send Post")
def send_post(message):
    if message.chat.id not in user_posts:
        bot.send_message(message.chat.id, "No active post found.")
        return
    
    post = user_posts[message.chat.id]
    markup = InlineKeyboardMarkup()
    for button_text, button_url in post["buttons"]:
        markup.add(InlineKeyboardButton(button_text, url=button_url))
    
    text = "Select a channel to send the post:\n"
    for channel in channels:
        markup.add(InlineKeyboardButton(channel, callback_data=f"send_to:{channel}"))
    markup.add(InlineKeyboardButton("All Channels", callback_data="send_to:all"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("send_to"))
def send_to_channel(call):
    target = call.data.split(":")[1]
    post = user_posts[call.message.chat.id]
    
    markup = InlineKeyboardMarkup()
    for button_text, button_url in post["buttons"]:
        markup.add(InlineKeyboardButton(button_text, url=button_url))
    
    if target == "all":
        for channel in channels:
            bot.send_message(channel, post["text"], reply_markup=markup)
    else:
        bot.send_message(target, post["text"], reply_markup=markup)
    
    bot.send_message(call.message.chat.id, "✅ Post sent successfully!")

@bot.message_handler(func=lambda message: message.text == "Broadcast" and message.chat.id == admin_id)
def broadcast_message(message):
    bot.send_message(message.chat.id, "Send me the message you want to broadcast.")
    bot.register_next_step_handler(message, send_broadcast)

def send_broadcast(message):
    bot.send_message(admin_id, f"Broadcast sent: {message.text}")
    # Implement user broadcast logic here

bot.polling(none_stop=True)
