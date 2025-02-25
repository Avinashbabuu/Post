import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8013649463:AAFAqEoo5FjzWLWjpwHfU9OmrrDzQrVSkMM"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID

# Initialize storage
added_channels = []
selected_channel = {}  # Stores user-selected channels
user_posts = {}  # Stores posts per user

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "✨ **ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴘᴏsᴛɪɴɢ ʙᴏᴛ!** 🚀\n\n"
    welcome_text += "📢 **ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴇᴀsɪʟʏ!**\n"
    welcome_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    welcome_text += "🔹 **/createpost** – ✍️ *ᴄʀᴇᴀᴛᴇ & ᴘᴏꜱᴛ ᴄᴏɴᴛᴇɴᴛ!*\n"
    welcome_text += "🔹 **/setchannel** – 📌 *ᴄʜᴏᴏꜱᴇ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ!*\n"
    welcome_text += "🔹 **/removechannel** – ❌ *ᴅᴇʟᴇᴛᴇ ᴀ ᴄʜᴀɴɴᴇʟ!*\n"
    welcome_text += "🔹 **/help** – 📖 *ᴜsᴀɢᴇ ɢᴜɪᴅᴇ!*\n"
    welcome_text += "━━━━━━━━━━━━━━━━━━━━━\n"

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Create Post"), KeyboardButton("Help"))
    markup.add(KeyboardButton("Set Channel"), KeyboardButton("Remove Channel"))

    if message.chat.id == admin_id:
        markup.add(KeyboardButton("Broadcast"))

    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "🚀 **ᴘᴏꜱᴛ ʙᴏᴛ ɢᴜɪᴅᴇ** 🚀\n\n"
    help_text += "🔹 **Create Post** – *Write and send posts easily!*\n"
    help_text += "🔹 **Set Channel** – *Choose where posts will be sent!*\n"
    help_text += "🔹 **Remove Channel** – *Delete unwanted channels!*\n"
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "Set Channel")
def set_channel(message):
    bot.send_message(message.chat.id, "Send me the channel username or ID (with @).")
    bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    added_channels.append(message.text)
    selected_channel[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"✅ Channel set: {message.text}")

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
    bot.send_message(message.chat.id, "Send me the text or media (photo/video) for the post.")
    bot.register_next_step_handler(message, save_post)

def save_post(message):
    if message.chat.id not in user_posts:
        user_posts[message.chat.id] = {"text": "", "media": None, "buttons": []}

    if message.content_type == "text":
        user_posts[message.chat.id]["text"] = message.text
    elif message.content_type == "photo":
        file_id = message.photo[-1].file_id
        user_posts[message.chat.id]["text"] = message.caption or ""
        user_posts[message.chat.id]["media"] = file_id
    elif message.content_type == "video":
        file_id = message.video.file_id
        user_posts[message.chat.id]["text"] = message.caption or ""
        user_posts[message.chat.id]["media"] = file_id
    else:
        bot.send_message(message.chat.id, "⚠️ Unsupported format. Send text, image, or video.")
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Add Inline Button"), KeyboardButton("Send Post"), KeyboardButton("Cancel"))
    bot.send_message(message.chat.id, "✅ Post saved. Add a button or send it.", reply_markup=markup)

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
    if message.chat.id not in user_posts:
        bot.send_message(message.chat.id, "No active post found.")
        return

    post = user_posts[message.chat.id]
    channel = selected_channel.get(message.chat.id)

    if not channel:
        bot.send_message(message.chat.id, "❌ No channel set. Use 'Set Channel' first.")
        return

    markup = InlineKeyboardMarkup()
    for btn in post["buttons"]:
        markup.add(InlineKeyboardButton(btn[0], url=btn[1]))

    if post["media"]:
        bot.send_photo(channel, post["media"], caption=post["text"], reply_markup=markup)
    else:
        bot.send_message(channel, post["text"], reply_markup=markup)

    bot.send_message(message.chat.id, "✅ Post sent successfully!")

bot.polling(none_stop=True)
