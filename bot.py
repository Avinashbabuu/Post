import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8013649463:AAHBlz-hW0YG6qM05pxQo4csKMye-asG2NY"
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
def send_welcome(message):
    """Send welcome message with buttons"""
    welcome_text = "✨ **Welcome to the Ultimate Posting Bot!** 🚀\n\n"
    welcome_text += "📢 **Effortless Channel Management & Post Creation!**\n"
    welcome_text += "🔹 Create, Preview & Send stylish posts with buttons!\n"
    welcome_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    welcome_text += "🔥 **Experience the fastest posting bot ever!** 🔥"

    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=home_keyboard(message.chat.id))

@bot.message_handler(func=lambda message: message.text == "Help")
def show_help(message):
    """Show help message with bot usage"""
    help_text = "**🤖 Bot Commands & Usage Guide:**\n\n"
    help_text += "📌 *Create Post:* Start a new post (text, photo, video).\n"
    help_text += "📌 *➕ Add Button:* Add inline buttons with links.\n"
    help_text += "📌 *📤 Send Post:* Choose a channel to send your post.\n"
    help_text += "📌 *Set Channel:* Save a channel for posting.\n"
    help_text += "📌 *Remove Channel:* Remove a saved channel.\n"
    help_text += "📌 *Broadcast (Admin Only):* Send messages to all users.\n"
    help_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    help_text += "⚡ **Enjoy effortless posting with smart automation!** ⚡"

    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "Create Post")
def create_post(message):
    """Ask user for post content"""
    bot.send_message(message.chat.id, "Send me the text or media (photo/video) for the post.")
    bot.register_next_step_handler(message, save_post)

def save_post(message):
    """Save user post with text/media"""
    user_id = message.chat.id
    user_posts[user_id] = {
        "text": message.text if message.content_type == "text" else message.caption or "",
        "media": message.photo[-1].file_id if message.content_type == "photo" else None,
        "buttons": []
    }
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Add Button", "📤 Send Post", "❌ Cancel")
    
    bot.send_message(user_id, "✅ Post saved. Now you can add buttons or send it.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "➕ Add Button")
def ask_button_details(message):
    """Ask for button details"""
    bot.send_message(message.chat.id, "Send the button title and link (Format: `Title - URL`).")
    bot.register_next_step_handler(message, save_button)

def save_button(message):
    """Save inline button"""
    user_id = message.chat.id
    try:
        title, link = message.text.split(" - ")
        user_posts[user_id]["buttons"].append((title, link))
        
        bot.send_message(user_id, f"✅ Button **{title}** added!", parse_mode="Markdown")
        preview_post(user_id)  # Show updated preview with button

    except:
        bot.send_message(user_id, "⚠️ Invalid format! Use: `Title - URL`", parse_mode="Markdown")

def preview_post(user_id):
    """Show post preview with inline buttons"""
    post = user_posts[user_id]
    
    markup = InlineKeyboardMarkup()
    for title, link in post["buttons"]:
        markup.add(InlineKeyboardButton(title, url=link))
    
    if post["media"]:
        bot.send_photo(user_id, post["media"], caption=post["text"], reply_markup=markup)
    else:
        bot.send_message(user_id, post["text"], reply_markup=markup)
    
    # Show send post option
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📤 Send Post", "➕ Add More Buttons", "❌ Cancel")
    bot.send_message(user_id, "✅ Post preview updated!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📤 Send Post")
def send_post(message):
    """Show channels to send post"""
    user_id = message.chat.id
    if user_id not in user_posts:
        bot.send_message(user_id, "No active post found.", reply_markup=home_keyboard(user_id))
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for ch in user_channels.get(user_id, []):
        markup.add(KeyboardButton(ch))
    markup.add(KeyboardButton("📢 Send to All"), KeyboardButton("❌ Cancel"))
    bot.send_message(user_id, "📌 Choose where to send the post:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in user_channels.get(message.chat.id, []) or message.text == "📢 Send to All")
def send_to_channel(message):
    """Send post to selected channel(s)"""
    user_id = message.chat.id
    post = user_posts.get(user_id, {})

    markup = InlineKeyboardMarkup()
    for title, link in post["buttons"]:
        markup.add(InlineKeyboardButton(title, url=link))

    for ch in user_channels.get(user_id, []) if message.text == "📢 Send to All" else [message.text]:
        if post["media"]:
            bot.send_photo(ch, post["media"], caption=post["text"], reply_markup=markup)
        else:
            bot.send_message(ch, post["text"], reply_markup=markup)

    bot.send_message(user_id, "✅ Post sent successfully!", reply_markup=home_keyboard(user_id))

bot.polling(none_stop=True)
