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
    welcome_text = """✨ **ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ᴘᴏsᴛɪɴɢ ʙᴏᴛ!** 🚀

📢 **ᴇꜰꜰᴏʀᴛʟᴇss ᴄʜᴀɴɴᴇʟ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ & ᴘᴏsᴛ ᴄʀᴇᴀᴛɪᴏɴ!**
━━━━━━━━━━━━━━━━━━━━━
🔹 **/createpost** – ✍️ *ᴄʀᴀꜰᴛ & sᴇɴᴅ ᴇɴɢᴀɢɪɴɢ ᴘᴏsᴛs ᴇꜰꜰᴏʀᴛʟᴇssʟʏ!*
🔹 **/setchannel** – 📌 *sᴇʟᴇᴄᴛ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ꜰᴏʀ ᴘᴏsᴛɪɴɢ!*
🔹 **/removechannel** – ❌ *ᴅᴇʟᴇᴛᴇ ᴀɴʏ ᴀᴅᴅᴇᴅ ᴄʜᴀɴɴᴇʟ!*
🔹 **/help** – 📖 *ɢᴇᴛ ᴀ ꜰᴜʟʟ ɢᴜɪᴅᴇ ᴏɴ ʙᴏᴛ ᴜsᴀɢᴇ!*
━━━━━━━━━━━━━━━━━━━━━
🔥 **ᴇxᴘᴇʀɪᴇɴᴄᴇ ᴛʜᴇ ꜰᴀsᴛᴇsᴛ ᴘᴏsᴛɪɴɢ ʙᴏᴛ ᴇᴠᴇʀ!** 🔥
"""

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Create Post"), KeyboardButton("Help"))
    markup.add(KeyboardButton("Set Channel"), KeyboardButton("Remove Channel"))

    if message.chat.id == admin_id:
        markup.add(KeyboardButton("Broadcast"))

    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """╔═══════════════╗
🚀 **ᴘᴏꜱᴛ ʙᴏᴛ ɢᴜɪᴅᴇ** 🚀
╚═══════════════╝

📝 **ᴄʀᴇᴀᴛᴇ ᴘᴏꜱᴛ**
   ➜ ✍️ *ᴍᴀᴋᴇ ᴀ ꜱᴛʏʟɪꜱʜ ᴘᴏꜱᴛ ᴡɪᴛʜ ɪᴍᴀɢᴇꜱ & ᴛᴇxᴛ!*

🔘 **ᴀᴅᴅ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴꜱ**
   ➜ 🔗 *ᴀᴛᴛᴀᴄʜ ʟɪɴᴋ ʙᴜᴛᴛᴏɴꜱ ᴛᴏ ᴘᴏꜱᴛ!*

📢 **ꜱᴇɴᴅ ᴘᴏꜱᴛ**
   ➜ 🚀 *ᴄʜᴏᴏꜱᴇ ᴄʜᴀɴɴᴇʟ & ᴘᴜʙʟɪꜱʜ ʏᴏᴜʀ ᴘᴏꜱᴛ!*

📌 **ꜱᴇᴛ ᴄʜᴀɴɴᴇʟ**
   ➜ 🎯 *ꜱᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ꜰᴏʀ ꜰᴜᴛᴜʀᴇ ᴘᴏꜱᴛꜱ!*

❌ **ʀᴇᴍᴏᴠᴇ ᴄʜᴀɴɴᴇʟ**
   ➜ 🚫 *ᴅᴇʟᴇᴛᴇ ᴀ ᴄʜᴀɴɴᴇʟ ꜰʀᴏᴍ ᴛʜᴇ ʟɪꜱᴛ!*
━━━━━━━━━━━━━━━━━━━━━
🔥 **ᴍᴀꜱᴛᴇʀ ᴛʜᴇꜱᴇ ꜰᴇᴀᴛᴜʀᴇꜱ & ʀᴏᴄᴋ ʏᴏᴜʀ ᴘᴏꜱᴛɪɴɢ ɢᴀᴍᴇ!** 🔥
"""
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

# Run bot
bot.infinity_polling()
