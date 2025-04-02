import telebot

TOKEN = "7554670936:AAFAuC_i2_5VpiniZMTY8ZNpocwTI_RgNNo"
bot = telebot.TeleBot(TOKEN)

responses = {
    "aye aye captain": "Wrong treasure, pirate... Flip the color of the sheet.",
    "a storm is coming pirate": "STORM{1s_th1s_th3_r34l_fl4g?}"
}

@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    response = responses.get(message.text.lower(), "Sorry, I don't understand that message.")
    bot.send_message(message.chat.id, response)

bot.polling()