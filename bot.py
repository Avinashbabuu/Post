
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8013649463:AAFAqEoo5FjzWLWjpwHfU9OmrrDzQrVSkMM"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID
user_channels = {}  # Store channels per user
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
@bot.message_handler(func=lambda message: message.text == "Home")
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
@bot.message_handler(func=lambda message: message.text == "Help")
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

@bot.message_handler(commands=['setchannel'])
@bot.message_handler(func=lambda message: message.text == "Set Channel")
def set_channel(message):
    """Ask for channel username or ID"""
    bot.send_message(message.chat.id, "Send me the channel username or ID.")
    bot.register_next_step_handler(message, save_channel, message.chat.id)

def save_channel(message, user_id):
    """Save the added channel for the user"""
    if user_id not in user_channels:
        user_channels[user_id] = []
    user_channels[user_id].append(message.text)
    bot.send_message(user_id, f"✅ Channel added: {message.text}", reply_markup=home_keyboard(user_id))

@bot.message_handler(commands=['removechannel'])
@bot.message_handler(func=lambda message: message.text == "Remove Channel")
def remove_channel(message):
    """List added channels and ask which to remove"""
    user_id = message.chat.id
    if user_id not in user_channels or not user_channels[user_id]:
        bot.send_message(user_id, "No channels to remove.", reply_markup=home_keyboard(user_id))
        return
    
    channel_list = "\n".join([f"{i+1}. {ch}" for i, ch in enumerate(user_channels[user_id])])
    bot.send_message(user_id, f"Current channels:\n{channel_list}\n\nSend the number of the channel to remove.")
    bot.register_next_step_handler(message, delete_channel, user_id)

def delete_channel(message, user_id):
    """Delete the selected channel"""
    try:
        index = int(message.text) - 1
        removed = user_channels[user_id].pop(index)
        bot.send_message(user_id, f"✅ Removed channel: {removed}", reply_markup=home_keyboard(user_id))
    except:
        bot.send_message(user_id, "Invalid selection.", reply_markup=home_keyboard(user_id))

@bot.message_handler(commands=['createpost'])
@bot.message_handler(func=lambda message: message.text == "Create Post")
def create_post(message):
    """Ask user for post content"""
    bot.send_message(message.chat.id, "Send me the text or media (photo/video) for the post.")
    bot.register_next_step_handler(message, save_post)

def save_post(message):
    """Save user post with text/media"""
    user_id = message.chat.id
    user_posts[user_id] = {"text": message.text if message.content_type == "text" else message.caption or "", 
                           "media": message.photo[-1].file_id if message.content_type == "photo" else None, 
                           "buttons": []}
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Add Inline Button", "Send Post", "Cancel")
    bot.send_message(user_id, "✅ Post saved. Add a button or send it.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Add Inline Button")
def add_button(message):
    """Ask for button title and link"""
    bot.send_message(message.chat.id, "Send me the button title and link separated by a comma.\nExample: Google, https://google.com")
    bot.register_next_step_handler(message, save_button)

def save_button(message):
    """Save inline button"""
    try:
        title, link = message.text.split(", ")
        user_id = message.chat.id
        user_posts[user_id]["buttons"].append((title, link))
        bot.send_message(user_id, f"✅ Button '{title}' added!", reply_markup=home_keyboard(user_id))
    except:
        bot.send_message(message.chat.id, "⚠️ Invalid format. Use: Title, Link", reply_markup=home_keyboard(message.chat.id))

@bot.message_handler(func=lambda message: message.text == "Send Post")
def send_post(message):
    """Show channels to send post"""
    user_id = message.chat.id
    if user_id not in user_posts:
        bot.send_message(user_id, "No active post found.", reply_markup=home_keyboard(user_id))
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for ch in user_channels.get(user_id, []):
        markup.add(KeyboardButton(ch))
    markup.add(KeyboardButton("Send to All"), KeyboardButton("Cancel"))
    bot.send_message(user_id, "Choose where to send the post:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in user_channels.get(message.chat.id, []) or message.text == "Send to All")
def send_to_channel(message):
    """Send post to selected channel(s)"""
    user_id = message.chat.id
    post = user_posts.get(user_id, {})

    for ch in user_channels.get(user_id, []) if message.text == "Send to All" else [message.text]:
        bot.send_message(ch, post["text"])

    bot.send_message(user_id, "✅ Post sent successfully!", reply_markup=home_keyboard(user_id))

bot.polling(none_stop=True)
