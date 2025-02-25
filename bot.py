import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8013649463:AAFAqEoo5FjzWLWjpwHfU9OmrrDzQrVSkMM"
bot = telebot.TeleBot(TOKEN)

admin_id = 6484788124  # Replace with your Telegram ID

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "✨ **ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ᴘᴏsᴛɪɴɢ ʙᴏᴛ!** 🚀\n\n"
    welcome_text += "📢 **ᴇꜰꜰᴏʀᴛʟᴇss ᴄʜᴀɴɴᴇʟ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ & ᴘᴏsᴛ ᴄʀᴇᴀᴛɪᴏɴ!**\n"
    welcome_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    welcome_text += "🔹 **/ᴄʀᴇᴀᴛᴇᴘᴏsᴛ** – ✍️ *ᴄʀᴀꜰᴛ & sᴇɴᴅ ᴇɴɢᴀɢɪɴɢ ᴘᴏsᴛs ᴇꜰꜰᴏʀᴛʟᴇssʟʏ!*\n"
    welcome_text += "🔹 **/sᴇᴛᴄʜᴀɴɴᴇʟ** – 📌 *sᴇʟᴇᴄᴛ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ꜰᴏʀ ᴘᴏsᴛɪɴɢ!*\n"
    welcome_text += "🔹 **/ʀᴇᴍᴏᴠᴇᴄʜᴀɴɴᴇʟ** – ❌ *ᴅᴇʟᴇᴛᴇ ᴀɴʏ ᴀᴅᴅᴇᴅ ᴄʜᴀɴɴᴇʟ!*\n"
    welcome_text += "🔹 **/ʜᴇʟᴘ** – 📖 *ɢᴇᴛ ᴀ ꜰᴜʟʟ ɢᴜɪᴅᴇ ᴏɴ ʙᴏᴛ ᴜsᴀɢᴇ!*\n"
    welcome_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    welcome_text += "🔥 **ᴇxᴘᴇʀɪᴇɴᴄᴇ ᴛʜᴇ ꜰᴀsᴛᴇsᴛ ᴘᴏsᴛɪɴɢ ʙᴏᴛ ᴇᴠᴇʀ!** 🔥"

    # Create a keyboard
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Create Post"), KeyboardButton("Help"))
    markup.add(KeyboardButton("Set Channel"), KeyboardButton("Remove Channel"))

    # Only add "Broadcast" button for admin
    if message.chat.id == admin_id:
        markup.add(KeyboardButton("Broadcast"))

    # Send message with keyboard
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['help'])  # Command should be lowercase
def send_help(message):
    help_text = "╔═══════════════╗\n"
    help_text += "  🚀 **ᴘᴏꜱᴛ ʙᴏᴛ ɢᴜɪᴅᴇ** 🚀\n"
    help_text += "╚═══════════════╝\n\n"

    help_text += "📝 **ᴄʀᴇᴀᴛᴇ ᴘᴏꜱᴛ**\n"
    help_text += "   ➜ ✍️ *ᴍᴀᴋᴇ ᴀ ꜱᴛʏʟɪꜱʜ ᴘᴏꜱᴛ ᴡɪᴛʜ ɪᴍᴀɢᴇꜱ & ᴛᴇxᴛ!*\n\n"

    help_text += "🔘 **ᴀᴅᴅ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴꜱ**\n"
    help_text += "   ➜ 🔗 *ᴀᴛᴛᴀᴄʜ ʟɪɴᴋ ʙᴜᴛᴛᴏɴꜱ ᴛᴏ ᴘᴏꜱᴛ!*\n\n"

    help_text += "📢 **ꜱᴇɴᴅ ᴘᴏꜱᴛ**\n"
    help_text += "   ➜ 🚀 *ᴄʜᴏᴏꜱᴇ ᴄʜᴀɴɴᴇʟ & ᴘᴜʙʟɪꜱʜ ʏᴏᴜʀ ᴘᴏꜱᴛ!*\n\n"

    help_text += "📌 **ꜱᴇᴛ ᴄʜᴀɴɴᴇʟ**\n"
    help_text += "   ➜ 🎯 *ꜱᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ꜰᴏʀ ꜰᴜᴛᴜʀᴇ ᴘᴏꜱᴛꜱ!*\n\n"

    help_text += "❌ **ʀᴇᴍᴏᴠᴇ ᴄʜᴀɴɴᴇʟ**\n"
    help_text += "   ➜ 🚫 *ᴅᴇʟᴇᴛᴇ ᴀ ᴄʜᴀɴɴᴇʟ ꜰʀᴏᴍ ᴛʜᴇ ʟɪꜱᴛ!*\n\n"

    help_text += "━━━━━━━━━━━━━━━━━━━━━\n"
    help_text += "🔥 **ᴍᴀꜱᴛᴇʀ ᴛʜᴇꜱᴇ ꜰᴇᴀᴛᴜʀᴇꜱ & ʀᴏᴄᴋ ʏᴏᴜʀ ᴘᴏꜱᴛɪɴɢ ɢᴀᴍᴇ!** 🔥"
    
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
    bot.send_message(message.chat.id, "Send me the text or media (photo/video) for the post.")
    bot.register_next_step_handler(message, save_post)

def save_post(message):
    if message.content_type == "text":
        user_posts[message.chat.id] = {"text": message.text, "media": None, "buttons": []}
    elif message.content_type == "photo":
        file_id = message.photo[-1].file_id  # Get the best quality image
        user_posts[message.chat.id] = {"text": message.caption or "", "media": file_id, "buttons": []}
    elif message.content_type == "video":
        file_id = message.video.file_id
        user_posts[message.chat.id] = {"text": message.caption or "", "media": file_id, "buttons": []}
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
    if message.chat.id in user_posts:
        post = user_posts[message.chat.id]
        chat_id = selected_channel.get(message.chat.id)

        if post["media"]:
            if message.chat.id in selected_channel:
                if post["media"].startswith("AgAC") or post["media"].startswith("BAAC"):  # Check if it's a photo
                    bot.send_photo(chat_id, post["media"], caption=post["text"])
                else:
                    bot.send_video(chat_id, post["media"], caption=post["text"])
            else:
                bot.send_message(message.chat.id, "❌ No channel set. Use 'Set Channel' first.")
        else:
            bot.send_message(chat_id, post["text"])

        bot.send_message(message.chat.id, "✅ Post sent successfully!")
    else:
        bot.send_message(message.chat.id, "No active post found.")
    
    markup = ReplyKeyboardMarkup()
    for ch in added_channels:
        markup.add(KeyboardButton(ch, callback_data=f"send_to:{ch}"))
    markup.add(KeyboardButton("Send to All", callback_data="send_to:all"))
    
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
