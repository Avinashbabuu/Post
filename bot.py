import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8013649463:AAFAqEoo5FjzWLWjpwHfU9OmrrDzQrVSkMM"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID
added_channels = []  # Store added channels
user_posts = {}  # Store user posts

def home_keyboard(user_id):
    """Home keyboard layout"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Create Post"), KeyboardButton("Help"))
    markup.add(KeyboardButton("Set Channel"), KeyboardButton("Remove Channel"))
    
    if user_id == admin_id:
        markup.add(KeyboardButton("Broadcast"))
    
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Send welcome message with buttons"""
    welcome_text = "✨ **Welcome to the Ultimate Posting Bot!** 🚀\n\n"
    welcome_text += "📢 **Effortless Channel Management & Post Creation!**\n"
    welcome_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    welcome_text += "🔹 **/createpost** – ✍️ *Craft & send engaging posts!*\n"
    welcome_text += "🔹 **/setchannel** – 📌 *Select the channel for posting!*\n"
    welcome_text += "🔹 **/removechannel** – ❌ *Delete added channels!*\n"
    welcome_text += "🔹 **/help** – 📖 *Full guide on bot usage!*\n"
    welcome_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    welcome_text += "🔥 **Experience the fastest posting bot ever!** 🔥"

    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=home_keyboard(message.chat.id))

@bot.message_handler(commands=['help'])
def send_help(message):
    """Send help message"""
    help_text = "🚀 **Post Bot Guide** 🚀\n\n"
    help_text += "📝 **Create Post** - ✍️ Make a stylish post with images & text!\n"
    help_text += "🔘 **Add Inline Buttons** - 🔗 Attach link buttons to post!\n"
    help_text += "📢 **Send Post** - 🚀 Choose channel & publish your post!\n"
    help_text += "📌 **Set Channel** - 🎯 Select a channel for future posts!\n"
    help_text += "❌ **Remove Channel** - 🚫 Delete a channel from the list!\n"
    help_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    help_text += "🔥 Master these features & rock your posting game! 🔥"

    bot.send_message(message.chat.id, help_text, parse_mode="Markdown", reply_markup=home_keyboard(message.chat.id))

@bot.message_handler(func=lambda message: message.text == "Set Channel")
def set_channel(message):
    """Ask for channel username or ID"""
    bot.send_message(message.chat.id, "Send me the channel username or ID.")
    bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    """Save the added channel"""
    added_channels.append(message.text)
    bot.send_message(message.chat.id, f"✅ Channel added: {message.text}", reply_markup=home_keyboard(message.chat.id))

@bot.message_handler(func=lambda message: message.text == "Remove Channel")
def remove_channel(message):
    """List added channels and ask which to remove"""
    if not added_channels:
        bot.send_message(message.chat.id, "No channels to remove.", reply_markup=home_keyboard(message.chat.id))
        return
    
    channel_list = "\n".join([f"{i+1}. {ch}" for i, ch in enumerate(added_channels)])
    bot.send_message(message.chat.id, f"Current channels:\n{channel_list}\n\nSend the number of the channel to remove.")
    bot.register_next_step_handler(message, delete_channel)

def delete_channel(message):
    """Delete the selected channel"""
    try:
        index = int(message.text) - 1
        removed = added_channels.pop(index)
        bot.send_message(message.chat.id, f"✅ Removed channel: {removed}", reply_markup=home_keyboard(message.chat.id))
    except:
        bot.send_message(message.chat.id, "Invalid selection.", reply_markup=home_keyboard(message.chat.id))

@bot.message_handler(func=lambda message: message.text == "Create Post")
def create_post(message):
    """Ask user for post content"""
    bot.send_message(message.chat.id, "Send me the text or media (photo/video) for the post.")
    bot.register_next_step_handler(message, save_post)

def save_post(message):
    """Save user post with text/media"""
    if message.content_type == "text":
        user_posts[message.chat.id] = {"text": message.text, "media": None, "buttons": []}
    elif message.content_type == "photo":
        file_id = message.photo[-1].file_id
        user_posts[message.chat.id] = {"text": message.caption or "", "media": file_id, "buttons": []}
    elif message.content_type == "video":
        file_id = message.video.file_id
        user_posts[message.chat.id] = {"text": message.caption or "", "media": file_id, "buttons": []}
    else:
        bot.send_message(message.chat.id, "⚠️ Unsupported format. Send text, image, or video.", reply_markup=home_keyboard(message.chat.id))
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Add Inline Button"), KeyboardButton("Send Post"), KeyboardButton("Cancel"))
    bot.send_message(message.chat.id, "✅ Post saved. Add a button or send it.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Cancel")
def cancel_action(message):
    """Cancel and go back to home"""
    bot.send_message(message.chat.id, "❌ Action canceled.", reply_markup=home_keyboard(message.chat.id))

@bot.message_handler(func=lambda message: message.text == "Send Post")
def send_post(message):
    """Show channels to send post"""
    if message.chat.id in user_posts:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for ch in added_channels:
            markup.add(KeyboardButton(ch))
        markup.add(KeyboardButton("Send to All"), KeyboardButton("Cancel"))
        bot.send_message(message.chat.id, "Choose where to send the post:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "No active post found.", reply_markup=home_keyboard(message.chat.id))

@bot.message_handler(func=lambda message: message.text in added_channels or message.text == "Send to All")
def send_to_channel(message):
    """Send post to selected channel(s)"""
    post = user_posts.get(message.chat.id, {})
    if not post:
        bot.send_message(message.chat.id, "No active post found.", reply_markup=home_keyboard(message.chat.id))
        return
    
    if message.text == "Send to All":
        targets = added_channels
    else:
        targets = [message.text]

    for ch in targets:
        if post["media"]:
            bot.send_photo(ch, post["media"], caption=post["text"])
        else:
            bot.send_message(ch, post["text"])

    bot.send_message(message.chat.id, "✅ Post sent successfully!", reply_markup=home_keyboard(message.chat.id))

bot.polling(none_stop=True)
